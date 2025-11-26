from flask_bootstrap import Bootstrap5
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
import pandas
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from data_scraping import DataScraping
from data_processing import DataProcessing
from wtforms import StringField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
Bootstrap5(app)

class AddItemForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_link = StringField('Link', validators=[DataRequired()])
    submit = SubmitField("Submit")
class Additional(FlaskForm):
    product = StringField('Product', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField("Add")

data_processing = DataProcessing()
all_products = data_processing.get_all_products()
all_prices = data_processing.get_all_prices()
total_price = float(0.00)
additional_items = []
additional_prices = []
add_prices = []
amounts = []

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
user_data_dir = os.path.join(os.getcwd(), "Chromess  Profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check_prices")
def check_prices():
    all_products = data_processing.get_all_products()
    driver = WebDriver(options=chrome_options)
    data_scraping = DataScraping(driver)
    url_addresses = data_processing.get_url_addresses()
    for url in url_addresses:
        all_products_data = data_scraping.get_information(url,all_products)
    driver.quit()
    all_names = []
    all_prices = []
    for key, value in all_products_data.items():
        all_names.append(key)
        all_prices.append(value)
    dict = {'product_name': all_names, 'price': all_prices, 'quantity': 1}
    df = pandas.DataFrame(dict)
    df.to_csv("static/productPrice.csv",index=False)

    return redirect(url_for('shopping_cart'))

@app.route("/shopping_cart", methods=["GET","POST"])
def shopping_cart():
    form = Additional()
    df = pandas.read_csv("static/productPrice.csv", usecols=['product_name', 'price', 'quantity'])
    result = df.to_dict(orient='records')

    if request.method=="POST" and form.validate_on_submit:
        price = float(request.form["price"])
        price_styled = f"{price:.2f} €"
        additional_prices.append(price)
        add_prices.append(price_styled)
        additional_items.append(request.form["product"])
        return render_template(
            "_additionals.html",
            additional_prices= additional_prices,
            additional_items = additional_items,
            add_prices = add_prices,
            add_items =len(additional_items)
        )


    return render_template(
        "shoppingCart.html",
        products=result,
        total_items=len(result),
        total_price=total_price,
        amounts=amounts,
        form=form,
        additional_prices=additional_prices,
        additional_items=additional_items,
        add_items=len(additional_items),
        add_prices = add_prices,
        )

@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        product_name = request.form.get("product_name")
        product_link = request.form.get("product_link")
        name_dict = {'product_name': product_name, 'price': "", 'quantity': 1}
        link_dict = {'URL': product_link}
        df = pandas.DataFrame(name_dict, index=[1])
        df.to_csv("static/productPrice.csv", mode="a", index=False, header=False)
        df = pandas.DataFrame(link_dict,index=[0])
        df.to_csv("static/URLlist.csv", mode="a", index=False, header=False)
        form.product_name.data = ""
        form.product_link.data = ""
        redirect(url_for('add_item'))
    return render_template("addItem.html", form=form)

@app.route("/calculate_total", methods=["GET", "POST"])
def calculate_total():
    form = Additional()
    df = pandas.read_csv("static/productPrice.csv")
    all_products = data_processing.get_all_products()
    all_prices = data_processing.get_all_prices()

    amounts = []
    total_price = 0

    for i in range(len(all_products)):
        quantity = request.form.get(f"q{i}")
        try:
            qty = int(quantity) if quantity else 0
            price = float(all_prices[i].replace(" €", ""))
            amount = qty * price
        except ValueError:
            qty = 0
            price = float(all_prices[i].replace(" €", ""))
            amount = price

        df.loc[i, "quantity"] = qty
        amounts.append(amount)
        total_price += amount
    final_price = total_price
    for i in range(len(additional_prices)):
        final_price = final_price+additional_prices[i]
    final_price = f"{final_price:.2f}"
    df.to_csv("static/productPrice.csv", index=False)

    total_price = f"{total_price:.2f}"
    result = df[["product_name", "price", "quantity"]].to_dict(orient="records")

    prices = [float(r["price"].replace(" €", "")) for r in result]
    amount_prices = [f"{a:.2f} €" for a in amounts]

    return render_template(
        "shoppingCart.html",
        products=result,
        total_items=len(result),
        total_price=total_price,
        final_price=final_price,
        amounts=amounts,
        prices=prices,
        amount_prices=amount_prices,
        form=form,
        additional_prices=additional_prices,
        additional_items=additional_items,
        add_items=len(additional_items),
        add_prices = add_prices
    )

if __name__ == "__main__":
    app.run(debug=True)






