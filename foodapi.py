##Search engine based on Food2Fork https://food2fork.com/about/api and Recipe Puppy http://www.recipepuppy.com/about/api/
##NOTE!!!! Food2Fork has limited total call before this api key expires ;( 5000 calls; Recipe puppy is free

import requests
import json
import re

from credentialshhanh import *

##Set up excel file
food2fork_file = "ffproducts.csv"
puppy_file = "ppproducts.csv"


##Select the search mode
def search_selection(choice):
    if choice == 1:
        query = input("Key in the dishname: ")
        food2fork_search(query)
    elif choice == 2:
        ingredients = input("Key in the ingredients you want, separated by comas: ")

##### NOTE: include in option Yes/No button in the bot for the below
        # not_ingredients = input("Key in the ingredients you DONT want, separated by comas: ")

        # if not_ingredients != "":
        #     not_ingredients = re.sub("[\\\\/:*?"<>|  ]", ",", not_ingredients)
        #     not_ingredients = not_ingredients.replace(",,",",")
        #     not_ingredients = not_ingredients.replace(",",",-")
        #     ingredients = ingredients + ",-" + not_ingredients

        #print (ingredients)
        puppy_search(ingredients)

## API Call function
def fetch_data(search_payload, url):
    search_req = requests.get(url, params=search_payload)
    print(search_req)
    if search_req.status_code == requests.codes.ok:
        data = search_req.json()
        print(data)
        return data
    elif search_req.status_code == 403:
        print("Exceed rate limit!")
        exit()
    else:
        print("Error!")
        exit()

# #Write data fetched from food2fork to excel file
# def food2fork_to_csv(data):
#     f1 = open(food2fork_file, "w") #open excel file
#     headers = "recipes, ranking, publisher_url, source_url, image_url\n"
#     f1.write(headers)
#     for item in data["recipes"]:
#         f1.write(item["title"].strip()  + "," + str(item["social_rank"]) + "," + item["publisher_url"] + "," + item["source_url"] + "," + item["image_url"] + "\n")
#     f1.close()
# #Write data fetched from recipe puppy to excel file
# def puppy_to_csv(data):
#     f2 = open(puppy_file, "w")
#     headers = "recipes, source_url, image_url\n"
#     f2.write(headers)
#     for item in data["results"]:
#         print(item)
#         f2.write(item["title"].strip() + "," + item["href"] + ","  + item["thumbnail"] + "\n")
#     f2.close()

def puppy_to_csv(data): #array
    f2 = open(puppy_file, "w")
    headers = "recipes, source_url, image_url\n"
    f2.write(headers)
    for item in data["results"]:
        print(item)
        f2.write(item["title"].strip() + "," + item["href"] + ","  + item["thumbnail"] + "\n")
    f2.close()

##Edge case no data found
def data_check(data, mode):
    if ((mode == 1) and (data["count"] == 0)) or ((mode == 2) and data["results"] == []):
        print("What an odd combination! Is there a typo?!")
        return 0
    else: 
        return 1

##Call food2fork for data
def food2fork_search(query, sort=None, page=None):
    query = re.findall(r"[\w']+", query)

    search_payload = {"key":food2fork_key, "q":query, "sort":sort, "page":page}
    data = fetch_data(search_payload, food2fork_url)
    if data_check(data, 1) == 1:
        food2fork_to_csv(data)
    
##Call recipe puppy for data
def puppy_search(ingredients, query=None, page=None):
    ingredients = re.findall(r"[\w']+", ingredients)

    search_payload = {"q":query, "i":ingredients, "page":page}
    data = fetch_data(search_payload, puppy_url)
    if data_check(data, 2) == 1:
        puppy_to_csv(data)

def main():
    choice = int(input(("Do you want to search by dish name - 1 or ingredients - 2 ? ")))
    search_selection(choice)
    

    print("Done!")

if __name__ == "__main__":
    main()