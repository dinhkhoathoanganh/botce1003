#version Yummly debugged 10/12
import telepot #pip install telepot, ... googlemaps, ... openpyxl
from telepot.loop import MessageLoop
import time
import datetime
import random
from credentialshhanh import *
from foodapi import *
from keyboard import keyboard
from chat_history import chat_history
from xl import xl
from preferences import pref
from gpstrack import *
'''
Intruction: type eatntu to restart the bot
'''
bot = telepot.Bot('406130496:AAFNc17PwDi7mmsYVAg2bYBtsc1LR1OlqVg')
result_list ={}
chat_id_list =[]

#Recipe Info headings for API CALL
headers_puppy = {0: "Puppy's Recipe directions", 1: "Puppy's Ingredients", 2: "Puppy's Image"}
headers_food2fork = {0: "Food2fork's Recipe directions", 1: "Food2fork's Image", 2: "Food2fork's Ingredients and Nutrition Facts", 3: "Food2fork's Rating"}
headers_yummly = ["Yummly's Recipe directions", "Yummly's Image", "Yummly's Ingredients", "Time needed (seconds)", "Yummly's Rating (out of 4)"]

#List types of food (only for Yummly)
type_options =['American', 'Italian', 'Asian', 'Mexican', 'French', 'Southwestern', 'Barbecue', 'Indian', 'Chinese', 'English', 'Mediterranean', 'Greek', 'Spanish', 'German', 'Thai', 'Moroccan', 'Irish', 'Japanese', 'Cuban', 'Hawaiin', 'Swedish', 'Hungarian', 'Portugese']
diet_options =['Pescetarian', 'Vegan', 'Vegetarian']

#The location, latitude and longtitude of Food locations are pre-set to avoid users's spamming the direction. In addition, it will save no. of API Call from Google Maps in subsequent operations
canteen_location_list = google_maps.excel_to_list("PlaceID.xlsx", "placeid")

#Global vaiables for Main that needed to be modified in multiple functions
class check :
    keyin = []
    recipeindex = 9999999999
    user_location = ''
    ingredient = ''
    
def voting_ad(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	data = [0]*6 + [1]*2 + [2]*2

	if (random.choice(data) == 1):
		print("1")
		bot.sendMessage(chat_id, '☕ WHEAT a second… Vote for team ChipsMORE! if you like our bot!!!')
	elif (random.choice(data)) == 2:
		print("2")
		bot.sendMessage(chat_id, 'By the way, CHIPZ in a VOTE for team ChipsMORE! (｡◕‿◕｡)')
	print("@@")


#Cases for messages received
def on_chat_message(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 
 #If the message is the location user sent
 if content_type == 'location' :
  get_user_location(chat_id, msg)
  if  chat_history.lastest_message0(chat_id) == "search for direction":
  	print(chat_history.lastest_message0(chat_id), "0000", chat_history.lastest_message1(chat_id))
  	keyboard.inlinequery(chat_id , canteen_location_list + ["Canteen nearest me!"], ' Choose your canteen ! ')
  elif chat_history.lastest_message0(chat_id) == "How to get there?":
  	print(chat_history.lastest_message0(chat_id), "0001", chat_history.lastest_message1(chat_id))
  	get_direction(chat_id, "to " + pref.canteen_name[chat_id])
  else:
  	print(chat_history.lastest_message0(chat_id), chat_history.lastest_message2(chat_id), "0002", chat_history.lastest_message1(chat_id))

  pass
 
 #If the message is the chat text
 elif content_type == 'text' :    
  chat_history.write_data(chat_id, msg['text'].lower())
  #Check edge cases when the user type spam messages
  if (keyboard.correction(msg['text']) not in ["Eatntu" , "/eatntu" , "Eat Ntu" , "Eat Out" , "/eatout" , "/eatin" , "Eat In" , "Dish Name" , "Ingredient" , "Give location ?", "How to get there?", "Search For Direction", "/searchfordirection", "Canteen nearest me!", "/searchdirection" , "/start","/mydisheslist", "My Dishes List","Food Type"] and chat_history.lastest_message1(chat_id)  not in ["dish name" , "ingredient"]) and chat_history.lastest_message2(chat_id)  not in ["ingredient"] or keyboard.correction(msg['text']) == False :
     bot.sendMessage(chat_id , "Oops you have typed in the wrong syntax . Please type 'eatntu' to restart")
  #Response for /start
  if keyboard.correction(msg['text']) == '/start' :
      bot.sendMessage(chat_id , " Hello and welcome to @eat_NTUbot ! Let's eat the whole NTU together , I mean , eat the food in NTU . Now to start , please type '/eatntu' or 'Eat NTU' !")
  #Response for /eatNTU with its recognisable variations    
  if keyboard.correction(msg['text'])  == 'Eatntu' or keyboard.correction(msg['text']) == 'Eat Ntu' or msg['text'] == '/eatntu':
     keyboard.customkeyboard3('Eat Out' , 'Eat In ', 'Search For Direction', "let's see what u want to do", chat_id)
     #Message to ask for voting
     voting_ad(msg)

###### EAT IN #####
  #Response for /eatin with its recognisable variations 
  if keyboard.correction(msg['text']) == 'Eat In' or msg['text'] == "/eatin" :
     keyboard.customkeyboard3('Dish Name' , 'Ingredient' , "Food Type", "What do you want to search the recipe by?",chat_id)
  
  #Response when the user want to search recipes by dish name with its recognisable variations 
  if keyboard.correction(msg['text']) =='Dish Name' :
     keyboard.remove_custom(chat_id)
     bot.sendMessage(chat_id, 'Key in the dish name:')
  
  #Response when the user want to search recipes by ingredients with its recognisable variations 
  if keyboard.correction(msg['text']) =='Ingredient' :
     keyboard.remove_custom(chat_id)
     bot.sendMessage(chat_id, 'Key in the ingredients, seperated by comas :')
  #Response after user keys in the ingredients he/she wants
  if chat_history.lastest_message1(chat_id) =='ingredient':
     bot.sendMessage(chat_id, 'Key in the ingredients you DONT WANT, seperated by comas (Psst.. if you dont have this, type Nil):')
  
  #Response when the user want to search recipes by food type with its recognisable variations
  if keyboard.correction(msg['text']) =='Food Type':
     keyboard.remove_custom(chat_id)
     keyboard.inlinequery(chat_id, type_options + diet_options, 'Which food type are you looking for?')
  
  #Search for recipe with dish name's keywords
  if chat_history.lastest_message1(chat_id) =='dish name' :
     food_api.new_id(chat_id,chat_id_list)
     #Search based on Yummly search (in case of the API Call Limit reaches, we will switch to Food2Fork)
     checker = food_api.yummly_search(chat_id,chat_id_list,results_list,msg['text'].lower(), None, None, None)
     recipe_handler(checker, chat_id)
  
  #Search for recipe with ingredient's keywords (register ingredients wanted) 
  if chat_history.lastest_message1(chat_id) =='ingredient' :
  	 check.ingredient = msg['text']

  #Search for recipe with ingredient's keywords (register ingredients NOT wanted)  
  #Search based on Yummly search (in case of the API Call Limit reaches, we will switch to Recipe Puppy) - Recipe Puppy does not have excluded ingredients feature so we will disable this part
  if chat_history.lastest_message2(chat_id) =='ingredient' :
     food_api.new_id(chat_id,chat_id_list)
     print("##in ", check.ingredient) #checkpoint
     print("##noning ", msg['text']) #checkpoint

     #If the user do not want to exclude any ingredients
     if keyboard.correction(msg['text']) == 'Nil':
      msg['text'] = " "
      print("##noning ", msg['text']) #checkpoint

     checker = food_api.yummly_ing_search(chat_id,chat_id_list,results_list, None, check.ingredient, msg['text'], None)
     recipe_handler(checker, chat_id)

  #Print out the lastest list of dishes searched by the user
  if keyboard.correction(msg['text']) == 'My Dishes List' or msg['text'] == '/mydisheslist' :      
      keyboard.inlinequery10(chat_id , check.keyin, "Here are your last list of recipes ! (again)")
  
  #Response for /eatout with its recognisable variations 
  if keyboard.correction(msg['text']) == 'Eat Out' or msg['text'] == "/eatout" :
      pref.user_type[chat_id] = ''
      pref.canteen[chat_id] = ''
      pref.canteen_name[chat_id] = ''
      pref.stall[chat_id] = ''
      pref.food_type[chat_id] = ''
      keyboard.inlinequery(chat_id, ['A random dish','A Food Type','A Canteen'], 'What do you want to search?')
  
  #Response for /searchfordirection with its recognisable variations 
  if keyboard.correction(msg['text']) == 'Search For Direction' or msg['text'] == "/searchfordirection":
      keyboard.location(chat_id)
       
  databasefile = open('database.txt','a')
  databasefile.writelines(str(chat_id) + ' : ' + msg['text'] + ' : ' + str(datetime.datetime.now()) + '\n')
  databasefile.close()

#Allow users to search individual info of each dish in the result list. To minimize API Call per search, we save the entire search result of each user in the collated dictionary results_list. 
#When the user need pieces of info, we do not need to perform another API call but to fetch it in results_list. 
#The dictionary is stored in the program itself in stead of writing in an external file so as to speed up the read and write process.     
def recipe_handler(checker, from_id):
  if keyboard.check_error(checker, from_id) == 0:
    check.keyin = food_api.search_chat_id(from_id,results_list,1)
    keyboard.inlinequery10(from_id , check.keyin, "Here are most relevant the recipes ! (Hint: you can go back to this message if you want to find out more about other dishes; or type /mydisheslist)")  
  
  #Edge case when the API Call return an error. Notify the user (No result from the search, API Call limit reached, Other external errors...)
  else:        
    bot.sendMessage(from_id , keyboard.check_error(checker, from_id))

def get_user_location(from_id, msg):
  bot.sendMessage(from_id, "Thanks for sharing your location ☺")
  check.user_location = str(msg['location']['latitude']) + "," + str(msg['location']['longitude'])

def get_direction(from_id, canteen_name):
     destination = google_maps.canteen_latlng("PlaceID.xlsx", "placeid", canteen_name)
     google_maps.new_id(from_id, chat_id_list_dir)
     #Find direction with Google Maps API and print out the direction instructions + estimated distance
     checker = google_maps.direction(from_id, chat_id_list_dir, results_list_dir, check.user_location, destination)
     if keyboard.check_error(checker, from_id) == 0:
     	instructions = google_maps.direction_instructions(from_id, results_list_dir)
     	distance = google_maps.calculate_distance(from_id, results_list_dir)
     	bot.sendMessage(from_id,"Here are the instructions " + canteen_name + ":")
     	if isinstance(instructions, list): #check for []
     		bot.sendMessage(from_id , '\n'.join(str(x) for x in instructions)) 
     	else:
     		bot.sendMessage(from_id , ' '.join(str(x) for x in instructions))     
     	bot.sendMessage(from_id,"Estimated distance: "+ str(distance))     #Send the statics map snapshot of the location using Google Maps API
     	google_maps.get_photo(destination)
     	bot.sendPhoto(chat_id=from_id, photo=open('phototestt1.jpeg', 'rb'))
     	bot.sendMessage(from_id,"Hope you won't get lost! Type 'eatNTU' restart")

     else:
     	bot.sendMessage(from_id , keyboard.check_error(checker, from_id)) 

#Cases for query received
def on_callback_query(msg): 
 query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
 
  #Record chat history
 chat_history.write_data(from_id,query_data)
 databasefile = open('database.txt','a')
 databasefile.writelines(str(from_id) + ' : ' + query_data + ' : ' + str(datetime.datetime.now()) + '\n')
 databasefile.close()

 #If the query data is in the food type list (When the user chooses to search by food type)
 for i in type_options + diet_options:
      if query_data == i:
        food_api.new_id(from_id, chat_id_list)
        checker = food_api.yummly_type_match(from_id, chat_id_list, results_list, query_data)
        recipe_handler(checker, from_id)
        pass

 #If the query data is in the list of dishes searched by the user
 for i in check.keyin :
     if query_data == i :
        check.recipeindex = keyboard.list_order( i , check.keyin)
        keyboard.inlinequery10(from_id , list(headers_yummly) , " What do u want to see about " + i + "?" )
        pass

 #If the query data is in the list of info for food API 
 for i in headers_yummly:
  if query_data == i :
    data_index = keyboard.list_order(query_data, headers_yummly)
    checker = food_api.search_chat_id(from_id, results_list, 2, check.recipeindex-1, data_index)
    print(query_data)
    if keyboard.check_error(checker, from_id) == 0:
      if isinstance(checker, list): #Check for first []
      	if isinstance(checker[0], list): #check for second []
      		bot.sendMessage(from_id , i + ": " + ', '.join(str(x) for x in checker[0]))
      	
      	else:
      		bot.sendMessage(from_id , i + ": " +' '.join(str(x) for x in checker))
      else:
      	bot.sendMessage(from_id , i + ": " +checker)
    else:
      bot.sendMessage(from_id , keyboard.check_error(checker, from_id)) 
    pass

###### DIRECTION #####
 #When user wants to find direction to a certain food location
 for i in canteen_location_list :
     if query_data == i :
     	 get_direction(from_id, query_data)
     pass   
 #Sort the food locations from nearest to furthest in straight-line distance in relation to the user's current location
 #We used straight-line distance instead of Google Maps's route distance in order to save significant number of API Call 
 #(Google API has limited API call rate, so this function will be more reliable when the users traffic is high)
 if query_data == "Canteen nearest me!":
  	keyboard.inlinequery(from_id, google_maps.sort_nearby_place(check.user_location, "PlaceID.xlsx", "placeid"), "Food places listed from nearest to furthest for you...")
  	pass
 if query_data == "How to get there?":
 	keyboard.location(from_id)

###### EAT OUT #####
 wb = xl.load_wb('Canteen Restaurant List.xlsx')
#USER CHOOSES A RANDOM DISH
 if query_data == 'A random dish' or query_data == 'Re-random a dish':
  canteen_name = str(random.choice(xl.sheets(wb)))
  canteen = wb[canteen_name]
  dish_name = str(random.choice(xl.column(canteen, 'D')))
  price = str(xl.cor_content(canteen,'D','E', dish_name))
  stall = str(xl.stall(canteen, 'D', 'C', dish_name))  
  dish_msg = "✌ Join 'ChipsMORE! the Explorer' to eat " + dish_name +', for $'+price+' at '+stall +' in '+ canteen_name
  if canteen_name == 'Cafes and Eateries':
      keyboard.inlinequery(from_id , ['Re-random a dish'], dish_msg)
  else:
      keyboard.inlinequery(from_id, ['How to get there?', 'Re-random a dish'], dish_msg)
      pref.canteen_name[from_id] = canteen_name

  bot.sendMessage(from_id, "Or.. if you are satisfied, type 'eatntu' to restart")
#USER CHOOSES A Favorite Food Type
 if query_data == 'A Food Type':
     pref.user_type[from_id] = 'A Food Type'
     print("inlinequery: ", query_data)
     keyboard.inlinequery(from_id, xl.all_columns(wb, 'B'), 'Choose your food type:')

 if (query_data in xl.all_columns(wb, 'B')) and pref.user_type[from_id] == 'A Food Type':
     pref.food_type[from_id] = query_data
     keyboard.inlinequery(from_id, xl.stall_and_sheet(wb, 'B', 'C', pref.food_type[from_id]), 'Here are the stalls')
 if query_data in xl.stall_and_sheet(wb, 'B', 'C', pref.food_type[from_id]):
     print(query_data.split)
     pref.stall[from_id] = query_data.split(' in ')[0]
     pref.canteen_name[from_id] = query_data.split(' in ')[1]
     pref.canteen[from_id] = wb[pref.canteen_name[from_id]]
     if pref.canteen_name[from_id] == 'Cafes and Eateries':
     	keyboard.inlinequery(from_id, ['All dishes', 'Healthier choices'], 'You did choose '+ query_data)
     else:
     	keyboard.inlinequery(from_id, ['All dishes', 'Healthier choices', 'How to get there?'], 'You did choose '+ query_data)
    
#USER CHOOSES A CANTEEN
 if query_data == 'A Canteen':
     pref.user_type[from_id] = 'A Canteen'
     keyboard.inlinequery(from_id, xl.sheets(wb), 'Choose one:')
 if (query_data in xl.sheets(wb)) and (pref.user_type[from_id] == 'A Canteen'):
     pref.canteen_name[from_id] = str(query_data)
     pref.canteen[from_id] = xl.load_ws(wb, str(query_data))
     keyboard.inlinequery(from_id, xl.column(pref.canteen[from_id], 'C'), 'You did choose '+ pref.canteen_name[from_id] +', choose a stall')
 if (query_data in xl.column(pref.canteen[from_id], 'C')) and (pref.user_type[from_id] == 'A Canteen'):
     pref.stall[from_id] = str(query_data)
     if pref.canteen_name[from_id] == 'Cafes and Eateries':
     	keyboard.inlinequery(from_id, ['All dishes', 'Healthier choices'], 'You did choose '+ query_data)
     else:
     	keyboard.inlinequery(from_id, ['All dishes', 'Healthier choices', 'How to get there?'], 'You did choose '+ query_data)
 if query_data == 'All dishes':
     row1 = xl.row(pref.canteen[from_id], 'C', pref.stall[from_id])
     print("#####", row1)
     row2 = xl.next_row(pref.canteen[from_id], 'C', 'E', pref.stall[from_id])
     print("#####",row2)
     message_out = ''
     for i in range(row1, row2):
         message_out = message_out + str("★ " + pref.canteen[from_id]['D'][i].value) + ', $' + str(pref.canteen[from_id]['E'][i].value) + '\n'
     bot.sendMessage(from_id, message_out)
     bot.sendMessage(from_id, 'Type "eatntu" to restart')
 if query_data == 'Healthier choices':
     row1 = xl.row(pref.canteen[from_id], 'C', pref.stall[from_id])
     print(row1)
     row2 = xl.next_row(pref.canteen[from_id], 'C', 'E', pref.stall[from_id])
     print(row2)
     message_out = ''
     for i in range(row1, row2):
         if pref.canteen[from_id]['F'][i].value != None:
             message_out = message_out + str("★ " + pref.canteen[from_id]['D'][i].value) + '\n'
     if message_out == '':
      bot.sendMessage(from_id, 'Sorry, this stall has no healthier choice.')
     else:
      bot.sendMessage(from_id, message_out)
     bot.sendMessage(from_id, 'Type "eatntu" to restart')

     
 print('Callback Query:', query_id, from_id, query_data)
 bot.answerCallbackQuery(query_id, text='Got it...')

     
    
 


MessageLoop(bot, {'chat': on_chat_message, 
                  'callback_query': on_callback_query}).run_as_thread()


print ('Listening')
while 1 :
    time.sleep(1) 
