import time
from selenium.webdriver.common.by import By
import pandas

class DataScraping:
    def __init__(self, driver):
        self.driver = driver
        self.product_price = {}

    def get_information(self, url, all_products):
        self.driver.get(url)
        time.sleep(5)
        products = self.driver.find_elements(By.CSS_SELECTOR, ".ljBjjo")
        product_list = []
        for product in products:
            product_list.append(product.text)
        new_list = "".join(product_list)
        new_list = new_list.split("\n")

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

