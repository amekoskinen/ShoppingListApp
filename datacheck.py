import requests

response = requests.get("https://www.s-kaupat.fi/tuotteet/hedelmat-ja-vihannekset-1/vihannekset/kurkut")
test_text = response.text

test = test_text.split(" ")
index = test.index('data-test-id="product-card"')

class_checked = "."+test[index-1][:-1]
print(index)
print(test[index-1])

print(class_checked)
