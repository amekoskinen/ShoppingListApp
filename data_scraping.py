import time
from selenium.webdriver.common.by import By
import pandas
from datacheck import check_class, clean_data

class DataScraping:
    def __init__(self, driver):
        self.driver = driver
        self.product_price = {}
        self.class_checked = check_class()

    def get_information(self, url, all_products):
        self.driver.get(url)
        time.sleep(5)
        products = self.driver.find_elements(By.CSS_SELECTOR, self.class_checked)
        product_list = []
        for product in products:
            product_list.append(product.text)
        if product_list == []:
            new_list = product_list
        else:
            new_list = "".join(product_list)
            new_list = clean_data(new_list)
            new_list = new_list.split("\n")
        print(new_list)

        for item in new_list:
            if item in all_products:
                index = new_list.index(item)
                price_found = False
                for i in range(len(new_list)-index):
                    if new_list[index+i].endswith("€") and not price_found:
                        price = new_list[index+i].replace(",",".")
                        self.product_price[item] = price
                        price_found =True
        return self.product_price

