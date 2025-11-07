import pandas

class DataProcessing:
    def __init__(self):
        self.all_products = []
        self.all_prices = []
        self.url_addresses = []
    def get_all_products(self):
        file = pandas.read_csv("static/productPrice.csv")  # All products that have been added
        products = file["product_name"].tolist()
        self.all_products = []
        for product in products:
            product = product.replace("�", "ä")
            self.all_products.append(product)
        return self.all_products
    def get_all_prices(self):
        file = pandas.read_csv("static/productPrice.csv")  # All products that have been added
        self.all_prices = file["price"].tolist()
        return self.all_prices
    def get_url_addresses(self):
        file = pandas.read_csv("static/URLlist.csv")
        self.url_addresses = file["URL"].tolist()
        return self.url_addresses

