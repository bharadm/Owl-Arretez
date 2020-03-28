import configparser as ConfigParser
import sys
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains



configParser = ConfigParser.RawConfigParser()
configFilePath = 'E:\Codecs\pyprojects\Owl-Arretez\extras\data-config.txt'
configParser.read(configFilePath)

# general_part
driver_location = configParser.get("general", "webdriver")

driver = webdriver.Chrome(driver_location)

url_list = []
# Get the product ASIN and href links
def get_list_of_urls():
    driver.get(configParser.get("general", "a-url"))
    count = 1
    asin_xpath = configParser.get("general", "asin-id")
    href_xpath = configParser.get("general", "href-url")
    for div_count in range(1, 5):
        url_pair = {"ASIN":"", "URL": ""}
        
        url_pair["ASIN"] = driver.find_element_by_xpath(asin_xpath.replace("#", str(div_count))).get_attribute('data-asin')
        url_pair["URL"] = driver.find_element_by_xpath(href_xpath.replace("#", str(div_count))).get_attribute('href')

        # url_pair["ASIN"] = div_items.getAttribute("data-asin")
        # url_pair["URL"] = driver.find_element_by_xpath(configParser.get("general", "href-url").replace("#", count))
        if "ssoredirect" not in url_pair["URL"]:
            url_list.append(url_pair)
    
    return url_list

product_collection_list = []
# Open each URL and get properties
def open_product_by_href(url_list):
    for product_item in url_list:
        try:
            product_collection = {"ProductID" : "", "ProductName" : "", "ProductPrice" : "", "ProductCartDescription" : "", "ProductShortDescription" : "",
                    "ProductLongDescription" : "", "ProductImage" : "", "ProductImage1" : "", "ProductImage2" : "", "ProductImage3" : "",
                    "ProductCategoryId" : "", "ProductUpdateDate" : ""}
            driver.get(product_item["URL"])
            time.sleep(2.5)
            product_collection["ProductID"] = product_item["ASIN"]
            product_collection["ProductName"] = driver.find_element_by_xpath(configParser.get("product-details","p-title")).text
            
            product_collection["ProductShortDescription"] = product_short_description(configParser.get("product-details","p-short-des"))
            product_collection["ProductLongDescription"] = product_long_description(configParser.get("product-details","p-long-des"))
            product_collection["ProductQNA"] = product_q_n_a(configParser.get("product-details","p-qna"))
            product_collection["ProductImage"] = product_image_path(configParser.get("image-path", "image1"))
            product_collection["ProductImage1"] = product_image_path(configParser.get("image-path", "image2"))
            product_collection["ProductImage2"] = product_image_path(configParser.get("image-path", "image3"))
            product_collection["ProductImage3"] = product_image_path(configParser.get("image-path", "image4"))
            product_collection["ProductUpdateDate"] = driver.find_element_by_xpath(configParser.get("product-details", "p-data-a")).text
            
            product_collection_list.append(product_collection)

        except Exception as e:
            print (str(e))
            break
    
    print (product_collection_list)

def product_short_description(p_short_des):
    features_bullets = []
    li_length = len(driver.find_element_by_xpath(p_short_des).find_elements_by_tag_name('li'))
    li_item = configParser.get("product-details", "p-short-des-li")
    for li_count in range(1, li_length+1):
        features_bullets.append(driver.find_element_by_xpath(li_item.replace("#",str(li_count))).text)
    
    return {"features": features_bullets}

def product_long_description(p_long_des_xpath):
    description = {}
    total_count = len(driver.find_element_by_xpath(p_long_des_xpath).find_elements_by_tag_name('tr'))
    p_long_des_tr = configParser.get("product-details", "p-long-des-tr")
    for count in range(1, total_count+1):
        description[driver.find_element_by_xpath(p_long_des_tr.replace('#', str(count)).replace('^^', '1')).text] =\
        driver.find_element_by_xpath(p_long_des_tr.replace('#', str(count)).replace('^^', '2')).text

    return description

def product_q_n_a(p_qna):
    qna_list = []
    qna_col_list = []
    qna_col = {}
    # Action to move to QNA
    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element_by_id("cf-ask-cel")).perform()
    time.sleep(2)
    # Loads QNA
    try:
        total_count = len(driver.find_element_by_xpath(p_qna).find_elements_by_xpath('//div[contains(@class, "a-fixed-left-grid") and contains(@class, "a-spacing-base")]'))/2
    except:
        return []
    p_qna_before_q = configParser.get("product-details","p-qna-before-q")
    for count in range(1, total_count+1):
        qna_list.append(driver.find_element_by_xpath(p_qna_before_q.replace("#", str(count))).find_element_by_tag_name('div').get_attribute('id'))
        
    # X Path variables
    p_qna_q = configParser.get("product-details","p-qna-q")
    p_qna_text = configParser.get("product-details","p-qna-text")
    p_qna_long_text = configParser.get("product-details","p-qna-longtext")

    for count in range(1, total_count+1):
        qna_col = {}
        qna_col["question"] = driver.find_element_by_xpath(p_qna_q.replace('#', str(qna_list[count-1]))).text
        
        if hasXpath(p_qna_text.replace("#", str(count))):
            qna_col["answer"] = driver.find_element_by_xpath(p_qna_text.replace("#", str(count))).text
        elif hasXpath(p_qna_long_text.replace("#", str(count))):
            qna_col["answer"] = driver.find_element_by_xpath(p_qna_long_text.replace("#", str(count))).text

        qna_col_list.append(qna_col)
    
    return qna_col_list

def hasXpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False

def product_image_path(image_xpath):
    try:
        return driver.find_element_by_xpath(image_xpath).get_attribute('src')
    except:
        return ""

# Working here
try:
    url_asin_list = get_list_of_urls()
    open_product_by_href(url_asin_list[:5])
    driver.quit()
except Exception as e:
    print (str(e))

