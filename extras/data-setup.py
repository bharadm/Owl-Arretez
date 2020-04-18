from backports import configparser
import sys
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import sqlite3
import psycopg2

class AmazonOperation:

    def __init__(self):
        self.cf_variable = configparser.ConfigParser()
        self.cf_variable.read('E:\Codecs\pyprojects\Owl-Arretez\extras\data-config.txt')
        chrome_options = Options()
        self.web_location = self.cf_variable["general"]["webdriver"]
        chrome_options.add_argument("--start-maximized")
        #chrome_options.add_argument('headless');

        self.driver = webdriver.Chrome(self.web_location, options= chrome_options)
    
    # Get the product ASIN and href links
    def get_list_of_urls(self):

        page_url = self.cf_variable.get("general", "a-url")
        asin_xpath = self.cf_variable.get("general", "asin-id")
        href_xpath = self.cf_variable.get("general", "href-url")
        thumb_xpath = self.cf_variable.get("general", "item-thumb")
        url_list = []
        for item in ['mobiles', 'laptop', 'camera']:
            for page_count in range(1,2):
                print (page_url.replace('#', str(page_count)).replace('item',str(item)))
                self.driver.get(page_url.replace('#', str(page_count)).replace('item',str(item)))
                count = 1
                # actions = ActionChains(self.driver)
                # actions.move_to_element(self.driver.find_element_by_id("rhf-container")).perform()
                time.sleep(6)
                self.driver.delete_all_cookies()
                for div_count in range(1, 3):
                    try:
                        print ("Fetching data started...")
                        url_pair = {"ASIN" : "", "URL": "", "ProductThumb" : ""}
                        #print (asin_xpath.replace("#", str(div_count)))
                        element = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.XPATH, asin_xpath.replace("#", str(div_count)))))
                        url_pair["ASIN"] = self.driver.find_element_by_xpath(asin_xpath.replace("#", str(div_count))).get_attribute('data-asin')
                        url_pair["URL"] = self.driver.find_element_by_xpath(href_xpath.replace("#", str(div_count))).get_attribute('href')
                        url_pair["ProductThumb"] = self.driver.find_element_by_xpath(thumb_xpath.replace("#", str(div_count))).get_attribute('src')

                        #print (url_pair)            
                        if "ssoredirect" not in url_pair["URL"]:
                            url_list.append(url_pair)
                    except Exception as e:
                        print ("Exception occured", e)
                        pass
            return url_list
    
    def open_product_by_href(self, url_list):
        product_collection_list = []
        for product_item in url_list:
            try:
                product_collection = {"ProductId" : "", "ProductName" : "", "ProductPrice" : "", "ProductCartDesc" : "", "ProductShortDesc" : "",
                        "ProductLongDesc" : "", "ProductQNA" : "", "ProductImage" : "", "ProductImage1" : "", "ProductImage2" : "", "ProductImage3" : "",
                        "ProductCategoryId" : "", "ProductUpdateDate" : "", "ProductThumb" : ""}
                self.driver.get(product_item["URL"])
                time.sleep(4)
                product_collection["ProductId"] = str(product_item["ASIN"])
                product_collection["ProductName"] = self.driver.find_element_by_xpath(self.cf_variable.get("product-details","p-title")).text
                product_collection["ProductShortDesc"] = str(self.product_short_description(self.cf_variable.get("product-details","p-short-des")))
                product_collection["ProductLongDesc"] = str(self.product_long_description(self.cf_variable.get("product-details","p-long-des")))
                product_collection["ProductQNA"] = str(self.product_q_n_a(self.cf_variable.get("product-details","p-qna")))
                product_collection = self.product_image_path(product_collection, self.cf_variable.get("image-path", "image"))
                #print (product_collection)
                product_collection["ProductUpdateDate"] = str(self.driver.find_element_by_xpath(self.cf_variable.get("product-details", "p-data-a")).text)
                
                product_collection["ProductThumb"] = product_item["ProductThumb"]
                if self.hasId(self.cf_variable.get("product-details", "p-prod-des")):
                    product_collection["ProductCartDesc"] = str(self.driver.find_element_by_id(self.cf_variable.get("product-details", "p-prod-des")).find_element_by_tag_name('p').text)
                
                product_collection["ProductUserReviews"] = str(self.product_u_n_reviews(self.cf_variable.get("product-details", "p-user-reviews")))
                product_collection_list.append(product_collection)

                time.sleep(8)
                
            except Exception as e:
                print (str(e), product_collection)
                self.driver.quit()   

        self.driver.quit()   
        return product_collection_list

    def product_short_description(self, p_short_des):
        features_bullets = []
        li_length = len(self.driver.find_element_by_xpath(p_short_des).find_elements_by_tag_name('li'))
        li_item = self.cf_variable.get("product-details", "p-short-des-li")
        for li_count in range(1, li_length+1):
            features_bullets.append(self.driver.find_element_by_xpath(li_item.replace("#",str(li_count))).text)
        
        return {"features": features_bullets}
    
    def product_long_description(self, p_long_des_xpath):
        description = {}
        total_count = len(self.driver.find_element_by_xpath(p_long_des_xpath).find_elements_by_tag_name('tr'))
        p_long_des_tr = self.cf_variable.get("product-details", "p-long-des-tr")
        for count in range(1, total_count+1):
            description[self.driver.find_element_by_xpath(p_long_des_tr.replace('#', str(count)).replace('^^', '1')).text] =\
            self.driver.find_element_by_xpath(p_long_des_tr.replace('#', str(count)).replace('^^', '2')).text

        return description
    
    def product_q_n_a(self, p_qna):
        qna_list = []
        qna_col_list = []
        qna_col = {}
        # Action to move to QNA
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_id("cf-ask-cel")).perform()
        time.sleep(2)
        # Loads QNA
        try:
            total_count = int(len(self.driver.find_element_by_xpath(p_qna).find_elements_by_xpath('//div[contains(@class, "a-fixed-left-grid") and contains(@class, "a-spacing-base")]'))/2)
        except:
            return []
        p_qna_before_q = self.cf_variable.get("product-details","p-qna-before-q")
        for count in range(1, total_count+1):
            qna_list.append(self.driver.find_element_by_xpath(p_qna_before_q.replace("#", str(count))).find_element_by_tag_name('div').get_attribute('id'))
            
        # X Path variables
        p_qna_q = self.cf_variable.get("product-details","p-qna-q")
        p_qna_text = self.cf_variable.get("product-details","p-qna-text")
        p_qna_long_text = self.cf_variable.get("product-details","p-qna-longtext")

        for count in range(1, int(total_count+1)):
            qna_col = {}
            qna_col["question"] = self.driver.find_element_by_xpath(p_qna_q.replace('#', str(qna_list[count-1]))).text
            
            if self.hasXpath(p_qna_text.replace("#", str(count))):
                qna_col["answer"] = self.driver.find_element_by_xpath(p_qna_text.replace("#", str(count))).text
            elif self.hasXpath(p_qna_long_text.replace("#", str(count))):
                qna_col["answer"] = self.driver.find_element_by_xpath(p_qna_long_text.replace("#", str(count))).text

            qna_col_list.append(qna_col)
        
        return qna_col_list
    
    def hasXpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
            return True
        except:
            return False
    
    def hasId(self, id):
        try:
            self.driver.find_element_by_id(id)
            return True
        except:
            return False
    
    def product_image_path(self, product_collection, image_xpath):
        value = 0
        image_ids = []
        for image_item in self.driver.find_elements_by_css_selector('li.a-spacing-small.item.imageThumbnail.a-declarative'):
            image_ids.append("//*[@id=\""+image_item.find_element_by_css_selector('span>span').get_attribute('id')+"-announce\"]/img")

        for image_xpath_item in image_ids:
            try:
                img_value = str(self.driver.find_element_by_xpath(image_xpath_item).get_attribute('src'))
                if "play-icon" not in img_value and value<5:
                    product_collection["ProductImage"+str(value if (value!=0) else '')] = img_value.replace(str(38),str(280)).replace(str(50),str(300))
                    value = value + 1
            except Exception as e:
                print (e)
                pass
        
        return product_collection
        

    def product_u_n_reviews(self, p_user_div_path):
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_id("reviewsMedley")).perform()
        time.sleep(2)
        user_ids = []
        for items in self.driver.find_element_by_xpath(p_user_div_path).find_elements_by_tag_name('div'):
            if "customer_review-" in items.get_attribute('id'):
                user_ids.append(str(items.get_attribute('id')))

        p_user_list = []
        
        for div_items in user_ids:
            p_user = {"user" : "", "userreview" : "", "userhelpful": "", "userrating" : ""}
            person_id = div_items
            p_user["user"] = self.driver.find_element_by_xpath("//*[@id=\""+person_id+"\"]/div[1]/a/div[2]/span").text
            p_user["userreview"] = self.driver.find_element_by_xpath("//*[@id=\""+person_id+"\"]/div[4]/span/div/div[1]/span").text
            p_user["userhelpful"] = self.driver.find_element_by_xpath("//*[@id=\""+person_id+"\"]/div[2]/a[1]/i/span").text
            if self.hasXpath("//*[@id=\""+person_id+"\"]/div[5]/span[1]/div[1]/span"):
                p_user["userrating"] = self.driver.find_element_by_xpath("//*[@id=\""+person_id+"\"]/div[5]/span[1]/div[1]/span").text
            else:
                p_user["userrating"] = self.driver.find_element_by_xpath("//*[@id=\""+person_id+"\"]/div[7]/span[1]/div[1]/span").text
                
            #print (p_user)
            p_user_list.append(p_user)
       
        return p_user_list

class Database:

    def __init__(self):
        #If localdb
        #self.conn = sqlite3.connect('E:\Codecs\pyprojects\Owl-Arretez\extras\owl.db')
        # If postGreSql
        self.conn = psycopg2.connect("dbname=owl user=postgres password=1234 host=localhost")
        self.cursor = self.conn.cursor()
        print ("connection established.. ")

    def insert_into_table(self, table_name, dict_value):
        try:
            with self.conn as conn:
                temp_dict = {}
                column_names = " ,".join(dict_value.keys())
                values_names = " ,".join(dict_value.values())
                self.cursor.execute('INSERT INTO {} ({}) VALUES ({}) ;'.format(table_name, column_names, values_names))
                self.cursor.commit()
                return "Insertion success"
        except:
            return "Insertion failure"
        
    def insert_into_table_many(self, table_name, list_dict_value):
        try:
            with self.conn as conn:
                values_list = []
                #If PostGreSQL
                column_names = "\""+"\",\"".join(list_dict_value[0].keys())+"\""
                #If local db
                # column_names = ", ".join(list_dict_value[0].keys())
                
                #If PostGreSQL
                placeholder = ",%s "*len(list_dict_value[0].keys())
                placeholder = placeholder[1:]

                #If local db
                # placeholder = ",? "*len(list_dict_value[0].keys())
                # placeholder = placeholder[1:]
                
                for list_item in list_dict_value:
                    values_list.append(tuple(list_item.values()))
                self.cursor.executemany("INSERT INTO {} ({}) VALUES ({}) ".format(table_name, column_names, placeholder), values_list)
                self.conn.commit()
                return "Multiple Insertion success"
        except Exception as e:
            print (str(e))
            return "Multiple Insertion failure"

# Working here
try:
    ao = AmazonOperation()
    url_asin_list = ao.get_list_of_urls()
    amazon_data = ao.open_product_by_href(url_asin_list)
    try:
        db = Database()
        print (db.insert_into_table_many("public.common_product", amazon_data))
    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into mobile table {}".format(error))

except Exception as e:
    print (str(e))

