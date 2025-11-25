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
        products = self.driver.find_elements(By.CSS_SELECTOR, ".joHiJE")
        product_list = []
        for product in products:
            product_list.append(product.text)
        if product_list == []:
            new_list = product_list
        else:
            new_list = "".join(product_list)
            new_list = new_list.replace("SuomiCoop", "Suomi\nCoop")
            new_list = new_list.replace("gK","g\nK")
            new_list = new_list.replace("oO","o\nO")
            new_list = new_list.replace("gV","g\nV")
            new_list = new_list.replace("eC","e\nC")
            new_list = new_list.replace("aG","a\nG")
            new_list = new_list.replace("gG","g\nG")
            new_list = new_list.replace("iG","i\nG")
            new_list = new_list.replace("nK","n\nK")
            new_list = new_list.replace("lV","l\nV")
            new_list = new_list.replace("gF", "g\nF")
            new_list = new_list.replace("iC", "i\nC")
            new_list = new_list.replace(", ","\n")
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

