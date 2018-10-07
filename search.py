import requests
import json
import time
from tcgplayerinfo import *

def search(bearer, product_name, cat_name=""):

    cat_array = []
    with open('cats.json') as cat_file:
        categories = json.loads(cat_file.read())
        for key in categories:
            cat_array.append([key, categories[key]])

    output_IDs = []
    search_item = product_name # name of product
    cat = cat_name # name of category
    bearer_token = "bearer {0}".format(bearer)
    done = False
    found_in_cat = False

    for cat_item in cat_array:
        if (cat == cat_item[0] or cat == cat_item[1]) and not done:
            done = True
            found_in_cat = True

            #time.sleep(.05)
            url = "http://api.tcgplayer.com/catalog/categories/" + str(cat_item[1]) + "/search"

            headers = {
                "Accept": "application/json" ,
                "Authorization": bearer_token ,
            }

            body = {
                "sort": "MinPrice DESC",
                "limit": 10,
                "offset": 0,
                "filters": [
                    {
                        "name": "ProductName",
                        "values": [ search_item ]
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=body)
            #response = requests.post(url, data=body, headers=headers)

            data = response.json()
            #print(data)

            error_list = data["errors"]  # seperate the list of errors from the rest of the json data

            if error_list.__len__() == 0:  # if there are no errors, continue
                for i in range(len(data["results"])):
                    output_IDs.append(data["results"][i])

            else:  # otherwise throw errors
                raise Exception(error_list[0])  # in theory this would raise all the errors, but i'm too lazy to do that

            #print(json.dumps(data, sort_keys=True,
            #      indent=2, separators=(',', ': ')))

    catagories = [55, 4, 5, 46, 56, 31, 33, 16, 43, 44, 51, 6, 32, 18, 28, 27,
                  23, 7, 47, 24, 17, 29, 19, 8, 34, 48, 1, 30, 9, 53, 21, 38,
                  15, 35, 3, 49, 10, 26, 11, 50, 14, 52, 22, 37, 57, 25, 54, 40,
                  39, 41, 42, 45, 20, 12, 13, 2, 36]

    if not done:
        for cat_num in catagories:
            found_in_cat = False

            #time.sleep(.05)
            url = "http://api.tcgplayer.com/catalog/categories/" + str(cat_num) + "/search"

            headers = {
                "Accept": "application/json" ,
                "Authorization": bearer_token ,
            }

            body = {
                "sort": "MinPrice DESC",
                "limit": 10,
                "offset": 0,
                "filters": [
                    {
                        "name": "product_name",
                        "values": [ product_name ]
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=body)
            #response = requests.post(url, data=body, headers=headers)

            data = response.json()

            error_list = data["errors"]  # seperate the list of errors from the rest of the json data

            if len(error_list) == 0:  # if there are no errors, continue
                for result in data["results"]:
                    output_IDs.append(result)

            else:  # otherwise throw errors
                raise Exception(error_list[0])  # in theory this would raise all the erros, but i'm too lazy to do that

    try:    # 1 = Gift card
        output_IDs.remove(1)
    except: # Gift card not found
        pass

    return output_IDs, found_in_cat

def get_data(prod_ID):
    item = Item(prod_ID)
    item.set_iv(item.get_json_data())
    return item.product_name + ":\n" + item.product_URL
