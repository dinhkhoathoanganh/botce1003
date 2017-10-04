#version for bot

import requests
import json
import re

from credentialshhanh import *
from dishtype import *

results_list = {}
chat_id_list = []

class food_api(object):
    #Global variable for the class

    no_result = "What an odd combination! Is there a typo?!"

    #List (2): Info for each recipe name - differs in various API platform
    headers_puppy = {0: "title", 1: "href", 2: "ingredients", 3: "thumbnail"}
    headers_food2fork = {0: "publisher", 1: "f2f_url", 2: "title", 3: "source_url", 4: "recipe_id", 5: "image_url", 6: "social_rank", 7: "publisher_url"}
    headers_yummly = {0: "ingredients", 1: "id", 2: "smallImageURLs", 3: "recipeName", 4: "totalTimeInSeconds", 5: "flavours", 6: "rating", 7: "course"}

    recipe_item_yummly = headers_yummly[3]
    api_item_yummly = "matches"
    recipe_item_puppy = headers_puppy[0]
    api_item_puppy = "results"
    recipe_item_food2fork = headers_food2fork[2]
    api_item_food2fork = "recipes"

    #Register new user on the results_list
    def new_id(chat_id, chat_id_list):
        chat_id_list = food_api.check_overlapping_id(chat_id, chat_id_list, results_list)
        # print(chat_id_list) #checkpoint
        chat_id_list.append(chat_id)
        return chat_id_list

    #Make sure that one user can only make one API call at any time
    def check_overlapping_id(chat_id, chat_id_list, results_list):
        for i in chat_id_list:
            if i == chat_id:
                print("Your old search is deleted.")
                chat_id_list, results_list = food_api.delete_id(chat_id, chat_id_list, results_list)
        return chat_id_list

    #Delete old API call of the user (if one has)
    def delete_id(chat_id, chat_id_list, results_list):
        chat_id_list.remove(chat_id)
        del results_list[chat_id]
        return (chat_id_list, results_list)


    ## API Call function
    def fetch_data(search_payload, url):
        search_req = requests.get(url, params=search_payload)
        
        # print(search_req) #checkpoint
        
        if search_req.status_code == requests.codes.ok:
            data = search_req.json()
            
            # print(data) #checkpoint
            
            return data
        elif search_req.status_code == (403 or 409):
            print("Exceed rate limit! Contact your admin")
            exit()
        
        else:
            print("Error!")
            exit()

    #Function to indicate which API platform the search is sourced from 
    def check_api_platform(platform_indicator):
        if platform_indicator == "yummly":
            api_item, recipe_item = food_api.api_item_yummly, food_api.recipe_item_yummly
        elif platform_indicator == "food2fork":
            api_item, recipe_item = food_api.api_item_food2fork, food_api.recipe_item_food2fork
        elif platform_indicator == "puppy":
            api_item, recipe_item = food_api.api_item_puppy, food_api.recipe_item_puppy

    #extract relevant data from the API call
    def search_chat_id(chat_id, results_list, mode, recipe_index=None, data_index=0): 
        #check api platform used for each chat_id search
        indicator = results_list[chat_id][0]

        if indicator == "yummly":
            heading, api_item, recipe_item = food_api.headers_yummly[data_index], food_api.api_item_yummly, food_api.recipe_item_yummly
        elif indicator == "food2fork":
            heading, api_item, recipe_item = food_api.headers_food2fork[data_index], food_api.api_item_food2fork, food_api.recipe_item_food2fork
        elif indicator == "puppy":
            heading, api_item, recipe_item = food_api.headers_puppy[data_index], food_api.api_item_puppy, food_api.recipe_item_puppy
        else:
            print(food_api.no_result)
            return
        
        # print("########", results_list) #checkpoint

        #mode 1 = list all recipe names found from the API call
        if mode == 1:
            output_list = []

            if results_list[chat_id] != food_api.no_result:
                for item in results_list[chat_id][1][api_item]:
                    output_list.append(item[recipe_item].strip())
                return output_list
            else:
                print(food_api.no_result)

        #mode 2 = list details according to the choossen recipe name
        elif mode == 2:

            output_list = [results_list[chat_id][1][api_item][recipe_index][heading]]

            return output_list
        else:
            print('Out of range!')
            exit()

    #Edge case no data found
    def data_check(data, mode):
        if ((mode == 1) and (data["count"] == 0)) or ((mode == 2) and data["results"] == []) or ((mode == 3) and data["totalMatchCount"] == 0):
            print(food_api.no_result)
            return 0
        else: 
            return 1

    #API Call food2fork for data
    def food2fork_search(chat_id, chat_id_list, results_list, query, sort=None, page=None):
        query = re.findall(r"[\w']+", query)

        search_payload = {"key":food2fork_key, "q":query, "sort":sort, "page":page}
        data = food_api.fetch_data(search_payload, food2fork_url)

        if food_api.data_check(data, 1) == 1:
            results_list[chat_id] = ["food2fork", data]
        else:
            results_list[chat_id] = food_api.no_result

        return results_list
        
    ##API Call recipe puppy for data
    def puppy_search(chat_id, chat_id_list, results_list, ingredients, query=None, page=None):

        ingredients = re.findall(r"[\w']+", ingredients)

        search_payload = {"q":query, "i":ingredients, "page":page}
        data = food_api.fetch_data(search_payload, puppy_url)
        if food_api.data_check(data, 2) == 1:
            results_list[chat_id] = ["puppy", data]
        else:
            results_list[chat_id] = food_api.no_result

        return results_list

    ##API Call recipe yummly for data
    def yummly_search(chat_id, chat_id_list, results_list, query, ingredients, non_ingredients, cuisine, diet=None, time=None):
        if ingredients != None:
            ingredients = re.findall(r"[\w']+", ingredients)
            non_ingredients = re.findall(r"[\w']+", non_ingredients)
            print(ingredients)
            print(non_ingredients)  

        search_payload = {"_app_id":yummly_id, "_app_key":yummly_key, "q":query, "allowedIngredient[]":ingredients, "allowedDiet[]":diet, "excludedIngredient[]":non_ingredients, "allowedCuisine[]":cuisine, "maxTotalTimeInSeconds":time}
        # print("search_payload: ", search_payload) #checkpoint
        data = food_api.fetch_data(search_payload, yummly_url)
        if food_api.data_check(data, 3) == 1:
            results_list[chat_id] = ["yummly", data]
        else:
            results_list[chat_id] = food_api.no_result

        return results_list

    #API Call recipe yummly for data (3rd branch - search according to food type)
    def yummly_type_match(chat_id, chat_id_list, results_list, search_type):
        if search_type in dish:
            food_type = dish[search_type]
            food_api.yummly_search(chat_id, chat_id_list, results_list, None,None,None,food_type)
        elif search_type in diet:
            diet_type = diet[search_type]
            food_api.yummly_search(chat_id, chat_id_list, results_list, None,None,None,None,diet_type)
        else:
            print("Please choose something from the list!")
            exit()

    # #bot connector
    # def keyword_to_list_recipe_info():
    #     pass
    #     new_id(chat_id, chat_id_list)
        


############### END OF CLASS ######################
        
##Select the search mode (for debugging on python)
def search_selection(choice, chat_id_list):

    if choice == 1:
        chat_id = int(input("input chat_id: "))
        query = input("Key in the dishname: ")
        food_api.new_id(chat_id, chat_id_list)

        food_api.food2fork_search(chat_id, chat_id_list, results_list, query)


    elif choice == 2:
        chat_id = int(input("input chat_id: "))
        ingredients = input("Key in the ingredients you want, separated by comas: ")

        food_api.new_id(chat_id, chat_id_list)

        food_api.puppy_search(chat_id, chat_id_list, results_list, ingredients)
#############

    elif choice == 3:
        chat_id = int(input("input chat_id: "))
        query = input("Key in the keyword: ")

        food_api.new_id(chat_id, chat_id_list)
        food_api.yummly_search(chat_id, chat_id_list, results_list, query,None,None,None)
    
    elif choice == 4:
        print(dish)
        print(diet)
        chat_id = int(input("input chat_id: "))
        search_type = input("Choose your type: ")

        food_api.new_id(chat_id, chat_id_list)
        food_api.yummly_type_match(chat_id, chat_id_list, results_list, search_type)
    elif choice == 5:
        chat_id = int(input("input chat_id: "))
        ingredients = input("Key in the ingredients you want, separated by comas: ")
        non_ingredients = input("Key in the ingredients you DON'T want, separated by comas: ")

        food_api.new_id(chat_id, chat_id_list)
        food_api.yummly_search(chat_id, chat_id_list, results_list, None,ingredients,non_ingredients,None)


#############
    elif choice == 6:
        mode = int(input("mode 1 = list all recipes; mode 2 = list details according to recipe: "))
        if mode == 1:
            chat_id = int(input("input chat_id you want to search: "))
            
            resultshaha = food_api.search_chat_id(chat_id, results_list, mode)

            # print("Your result! ", resultshaha) #checkpoint

        elif mode == 2:
            chat_id = int(input("input chat_id you want to search: "))
            
            # print(food_api.headers_puppy) #checkpoint
            recipe_index = int(input("input recipe_index you want to search: "))
            data_index = int(input("input data_index you want to search: "))
            
            resultshaha = food_api.search_chat_id(chat_id, results_list, mode, recipe_index, data_index)

            print("Your result! ", resultshaha) #checkpoint


def main():
    termm = True
    while termm == True:
        print("chat_id_list: ", chat_id_list) #checkpoint
        
        choice = int(input(("Do you want to search by dish name(f2f) - 1 or ingredients(puppy) - 2  or dish name(yu) - 3 or dish type(yu) - 4 or ingredients(yu) - 5 or search result -6? ")))
        search_selection(choice, chat_id_list)
        print("Done! Press X to exit")

        if input() == 'X':
            termm = False
        else: 
            termm = True

if __name__ == "__main__":
    main()