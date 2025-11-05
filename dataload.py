import pandas

my_dict = {'Kotimaista kurkku': '0.88 €', 'Coop miniluumutomaatti 250g': '1.39 €', 'Kotimaista jääsalaatti 100g Suomi': '1.39 €', 'H&H Tuominen sipuli': '0.17 €', 'H&H Tuominen yleisperuna harjattu': '0.08 €', 'Kotimaista 300g juureskuutiot': '1.69 €', 'Oululainen Pullava Dallaspitko 400g': '3.39 €'}

all_names=[]
all_prices=[]
for key, value in my_dict.items():
    all_names.append(key)
    all_prices.append(value)
dict= {'product_name': names, 'price': prices}
df = pandas.DataFrame(dict)
df.to_csv("static/productTest.csv")