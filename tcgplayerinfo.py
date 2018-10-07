import requests
import json
import datetime

class Item():
    def __init__(self, bearer, prod_ID):
        #set up basic info needed to get json data
        self.product_ID = prod_ID
        self.url = "http://api.tcgplayer.com/catalog/products/{0}".format(self.product_ID)

        self.bearer_token = "bearer {0}".format(bearer)

        self.headers = {
            "Accept": "application/json" ,
            "Authorization": self.bearer_token
        }

        data = self.get_json_data()
        self.set_iv(data)

    def get_json_data(self):
        response = requests.get(self.url, headers=self.headers)

        data = json.loads(response.text) #save json data as a dictionary for parsing

        error_list = data["errors"] #seperate the list of errors from the rest of the json data

        if len(error_list) == 0: #if there are no errors, continue
            return data["results"][0]

        else:                       #otherwise throw errors
            raise Exception(error_list[0]) #in theory this would raise all the erros, but i'm too lazy to do that

    def set_iv(self, data):
        self.image_url = data["image"]
        self.modified_date = datetime.datetime.strptime(data["modifiedOn"].split('.')[0], '%Y-%m-%dT%H:%M:%S')
        self.product_name = data["productName"]
        self.clean_product_name = data["cleanProductName"]
        self.product_URL = data["url"]

    def __str__(self):
        return ("{0.image_url}" +
                "\n{0.modified_date}" +
                "\n{0.product_name}" +
                "\n{0.clean_product_name}" +
                "\n{0.product_URL}").format(self)
