from flask_bootstrap import Bootstrap5
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
import os
from flask import Flask, render_template, redirect, url_for, request
import pandas
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from data_scraping import DataScraping
from wtforms import StringField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
Bootstrap5(app)

class AddItemForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_link = StringField('Link', validators=[DataRequired()])
    submit = SubmitField("Submit")

file = pandas.read_csv("static/productPrice.csv") #All products that have been added
products = file["product_name"].tolist()
all_products = []
all_prices = file["price"].tolist()
for product in products:
    product = product.replace("�","ä")
    all_products.append(product)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
user_data_dir = os.path.join(os.getcwd(), "Chromess  Profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

total_price = float(0.00)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check_prices")
def check_prices():
    file = pandas.read_csv("static/productPrice.csv")  # All products that have been added
    products = file["product_name"].tolist()
    all_products = []
    for product in products:
        product = product.replace("�", "ä")
        all_products.append(product)
    driver = WebDriver(options=chrome_options)
    data_scraping = DataScraping(driver)
    file = pandas.read_csv("static/URLlist.csv")
    url_addresses = file["URL"].tolist()
    for url in url_addresses:
        all_products_data = data_scraping.get_information(url,all_products)
    driver.quit()

    all_names = []
    all_prices = []
    for key, value in all_products_data.items():
        all_names.append(key)
        all_prices.append(value)
    dict = {'product_name': all_names, 'price': all_prices}
    df = pandas.DataFrame(dict)
    df.to_csv("static/productPrice.csv",index=False)

    return render_template("prices.html", prices=all_products_data)

@app.route("/shopping_cart")
def shopping_cart():
    file = pandas.read_csv("static/productPrice.csv")  # All products that have been added
    products = file["product_name"].tolist()
    all_products = []
    for product in products:
        product = product.replace("�", "ä")
        all_products.append(product)
    df = pandas.read_csv("static/productPrice.csv", usecols=['product_name', 'price', 'quantity'])
    result = df.to_dict(orient='records')
    return render_template("shoppingCart.html", products = result, total_items=len(result), total_price = total_price)

@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        product_name = request.form.get("product_name")
        product_link = request.form.get("product_link")
        name_dict = {'product_name': product_name}
        link_dict = {'URL': product_link}
        df = pandas.DataFrame(name_dict, index=[1])
        df.to_csv("static/productPrice.csv", mode="a", index=False, header=False)
        df = pandas.DataFrame(link_dict,index=[0])
        df.to_csv("static/URLlist.csv", mode="a", index=False, header=False)
    return render_template("addItem.html", form=form)

@app.route("/calculate_total", methods=["GET","POST"])
def calculate_total():
    total_price = 0
    df = pandas.read_csv("static/productPrice.csv")
    for i in range(len(all_prices)):
        quantity = request.form.get(f"q{i}")
        df.loc[i, 'quantity'] = quantity
        df.to_csv("static/productPrice.csv", index=False)
        amount = int(quantity)*float(all_prices[i][0:-2])
        total_price = total_price+amount
    df = pandas.read_csv("static/productPrice.csv", usecols=['product_name', 'price', 'quantity'])
    result = df.to_dict(orient='records')
    return render_template("shoppingCart.html", products=result, total_items=len(result), total_price=total_price)

if __name__ == "__main__":
    app.run(debug=True)






