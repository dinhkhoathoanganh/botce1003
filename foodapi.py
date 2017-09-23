#Search engine based on Food2Fork https://food2fork.com/about/api and Recipe Puppy http://www.recipepuppy.com/about/api/
#NOTE!!!! Food2Fork has limited total call before this api key expires ;( 5000 calls; Recipe puppy is free

import requests
import json

#Food2fork API key
food2fork_api = 'd6ec9ede5565ccaf1417242d82d1f537'

#Set up excel file
filename = "products.csv"
f = open(filename, "w") #open excel file

#Select the search mode
def search_selection(choice):
    if choice == 1:
        query = input("Key in the dishname: ")
        food2fork_search(query)
    elif choice == 2:
        query = input("Key in the ingredients list, separated by comas: ")
        puppy_search(query)

#Write data fetched from food2fork to excel file
def food2fork_to_csv(data):
    headers = "recipes, ranking, publisher_url, source_url, image_url\n"
    f.write(headers)
    for item in data['recipes']:
        f.write(item['title'].replace(",","|")  + "," + str(item['social_rank']) + "," + item['publisher_url'] + "," + item['source_url'] + "," + item['image_url'] + "\n")

#Write data fetched from recipe puppy to excel file
def puppy_to_csv(data):
    headers = "recipes, source_url, image_url\n"
    f.write(headers)
    for item in data['results']:
        f.write(item['title'].replace(",","|")  + "," + item['href'] + ","  + item['thumbnail'] + "\n")

#Edge case no data found
def data_check(data, mode):
    if ((mode == 1) and (data['count'] == 0)) or ((mode == 2) and data['results'] == []):
        print("No data found! Is there a typo?!")
        return 0
    else: 
        return 1

#Call food2fork for data
def food2fork_search(query):
    api_key = food2fork_api
    url = 'http://food2fork.com/api/search?key=' + api_key
    key_words = query.replace(' ', '%20')
    final_url = url + "&q=" + key_words
    json_obj = requests.get(final_url)
    data = json_obj.json()
##    print(data)
    if data_check(data, 1) == 1:
        food2fork_to_csv(data)

#Call recipe puppy for data
def puppy_search(query):
##    ingrd_list = query.split(",")
    url = 'http://www.recipepuppy.com/api/?i='
    key_words = query.replace(' ', ',')
    final_url = url + key_words
##    print('hey! ' + final_url)
    json_obj = requests.get(final_url)
    data = json_obj.json()
    print(data)
    if data_check(data, 2) == 1:
        puppy_to_csv(data)

def main():
    choice = int(input(("Do you want to search by dish name - 1 or ingredients - 2 ? ")))
    search_selection(choice)
    
    f.close() # Close excel file
    print('Done!')

main()

# requests.get('http://food2fork.com/api/search?key=d6ec9ede5565ccaf1417242d82d1f537&q=shredded%20chicken')
#r = requests.get('http://food2fork.com/api/search?key=d6ec9ede5565ccaf1417242d82d1f537&q=shredded%20chicken')
#r.json()
#food2fork_search('shredded chicken')
