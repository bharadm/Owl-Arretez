try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser

from bs4 import BeautifulSoup as bs
from selenium import webdriver

configParser = ConfigParser.RawConfigParser()
configFilePath = 'data-config.txt'
configParser.read(configFilePath)

# general_part
driver_location = configParser.get("general", "driver_location")

driver = webdriver.Chrome(driver_location)

url_list = []
# Get the product ASIN and href links
def get_list_of_urls():
    driver.get()
    count = 1
    for div_items in driver.find_element_by_xpath().find_elements_by_tag_name('div'):
        url_pair = {"ASIN":"", "URL": ""}
        url_pair["ASIN"] = div_items["data-asin"]
        url_pair["URL"] = configParser.get("general", "href-url").replace("#", count)

        url_list.append(url_pair)
    
    return url_list

product_collection = {"ProductID" : "", "ProductName" : "", "ProductPrice" : "", "ProductCartDescription" : "", "ProductShortDescription" : "",
                    "ProductLongDescription" : "", "ProductImage" : "", "ProductImage1" : "", "ProductImage2" : "", "ProductImage3" : "",
                    "ProductCategoryId" : "", "ProductUpdateDate" : ""}
# Open each URL and get properties
def open_product_by_href(url_list):
    for product_item in url_list:
        driver.get(product_item["URL"])
        product_collection["ProductID"] = product_item["ASIN"]
        product_collection["ProductName"] = driver.find_element_by_xpath("p-title")
        product_collection["ProductShortDescription"] = driver.find_element_by_xpath("p-short-des")
        product_collection["ProductLongDescription"] = product_long_description(driver.find_element_by_xpath("p-long-des"))
        product_collection["ProductQNA"] = product_q_n_a("p-qna")

def product_long_description(p_long_des_xpath):
    description = {}
    total_count = len(driver.find_element_by_xpath(p_long_des_xpath).find_elements_by_tag_name('tr'))
    p_long_des_tr = ""
    for count in range(total_count):
        description[driver.find_element_by_xpath(p_long_des_tr.replace('#', count+1).replace('*', '1')).text] = driver.find_element_by_xpath(p_long_des_tr.replace('#', count+1).replace('*', '2')).text

    return description

def product_q_n_a(p_qna):
    qna_list = []
    qna_col_list = []
    qna_col = {}
    total_count = len(driver.find_element_by_xpath(p_qna).find_elements_by_tag_name('div'))
    p_qna_before_q = ""
    for count in range(total_count):
        qna_list.append(driver.find_element_by_xpath(p_qna_before_q.replace("#", count+1)).find_element_by_tag_name('div').get_attribute('id'))

    # X Path variables
    p_qna_q = ""
    p_qna_text = ""
    p_qna_long_text = ""

    for count in range(total_count):
        qna_col["question"] = driver.find_element_by_xpath(p_qna_q.replace('#', qna_list[count])).value
        
        if hasXpath(p_qna_text.replace("#", count + 1 )):
            qna_col["answer"] = driver.find_element_by_xpath(p_qna_text.replace("#", count + 1)).value
        elif hasXpath(p_qna_long_text.replace("#", count + 1 )):
            qna_col["answer"] = driver.find_element_by_xpath(p_qna_long_text.replace("#", count + 1)).value

        qna_col_list.append(qna_col)
    
    return qna_col_list

def hasXpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False