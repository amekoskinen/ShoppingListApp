import requests

def check_class():
    response = requests.get("https://www.s-kaupat.fi/tuotteet/hedelmat-ja-vihannekset-1/vihannekset/kurkut")
    test_text = response.text

    test = test_text.split(" ")
    index = test.index('data-test-id="product-card"')

    class_checked = "."+test[index-1][:-1]

    return class_checked

def clean_data(new_list):
    new_list = new_list.replace("SuomiCoop", "Suomi\nCoop")
    new_list = new_list.replace("gK", "g\nK")
    new_list = new_list.replace("oO", "o\nO")
    new_list = new_list.replace("gV", "g\nV")
    new_list = new_list.replace("eC", "e\nC")
    new_list = new_list.replace("aG", "a\nG")
    new_list = new_list.replace("gG", "g\nG")
    new_list = new_list.replace("iG", "i\nG")
    new_list = new_list.replace("nK", "n\nK")
    new_list = new_list.replace("lV", "l\nV")
    new_list = new_list.replace("gF", "g\nF")
    new_list = new_list.replace("iC", "i\nC")
    new_list = new_list.replace(", ", "\n")
    new_list = new_list.replace("  ", " ")
    new_list = new_list.replace("a2", "a\n2")
    new_list = new_list.replace("iB", "i\nB")
    new_list = new_list.replace("aW", "a\nW")
    new_list = new_list.replace("lC", "l\nC")
    new_list = new_list.replace("gA", "g\nA")
    new_list = new_list.replace("0K", "0\nK")
    new_list = new_list.replace("5K", "5\nK")
    new_list = new_list.replace("LK", "L\nK")
    new_list = new_list.replace("lW", "l\nW")
    new_list = new_list.replace("gX", "g\nX")
    new_list = new_list.replace("lO", "l\nO")
    return new_list