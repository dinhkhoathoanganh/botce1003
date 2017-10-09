#version Yummly debugged 10/8
import telepot #pip install telepot, ... googlemaps, ... openpyxl
from telepot.loop import MessageLoop
import time
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

#headings
headers_puppy = {0: "Puppy's Recipe directions", 1: "Puppy's Ingredients", 2: "Puppy's Image"}
headers_food2fork = {0: "Food2fork's Recipe directions", 1: "Food2fork's Image", 2: "Food2fork's Ingredients and Nutrition Facts", 3: "Food2fork's Rating"}
headers_yummly = ["Yummly's Recipe directions", "Yummly's Image", "Yummly's Ingredients", "Time needed (seconds)", "Yummly's Rating (out of 4)"]

#list types of food
type_options =['American', 'Italian', 'Asian', 'Mexican', 'French', 'Southwestern', 'Barbecue', 'Indian', 'Chinese', 'English', 'Mediterranean', 'Greek', 'Spanish', 'German', 'Thai', 'Moroccan', 'Irish', 'Japanese', 'Cuban', 'Hawaiin', 'Swedish', 'Hungarian', 'Portugese']
diet_options =['Pescetarian', 'Vegan', 'Vegetarian']

#global vaiables for Main
class check :
    keyin = []
    recipeindex = 9999999999
    user_location = ''
    ingredient = ''
    canteen_location_list = google_maps.excel_to_list("PlaceID.xlsx", "placeid")
    

def on_chat_message(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 if content_type == 'location' :
  bot.sendMessage(chat_id, "Thanks for sharing your location :)")
  check.user_location = str(msg['location']['latitude']) + "," + str(msg['location']['longitude'])
  print("@@@ ", check.user_location, "@@ ", check.canteen_location_list) #checkpoint
  keyboard.inlinequery(chat_id , check.canteen_location_list , ' Choose your canteen ! ')
  
  
 elif content_type == 'text' :    
  chat_history.write_data(chat_id, msg['text'].lower())
  
  if (keyboard.correction(msg['text']) not in ["Eatntu" , "/eatntu" , "Eat Ntu" , "Eat Out" , "/eatout" , "/eatin" , "Eat In" , "Dish Name" , "Ingredient" , "Give location ?","Search For Direction", "/searchdirection" , "/start","/mydisheslist", "My Dishes List","Food Type"] and chat_history.lastest_message1(chat_id)  not in ["dish name" , "ingredient"]) and chat_history.lastest_message2(chat_id)  not in ["ingredient"] or keyboard.correction(msg['text']) == False :
     bot.sendMessage(chat_id , "Oops you have typed in the wrong syntax . Please type 'eatntu' to restart")
  if keyboard.correction(msg['text']) == '/start' :
      bot.sendMessage(chat_id , " Hello and welcome to @eat_NTUbot ! Let's eat the whole NTU together , I mean , eat the food in NTU . Now to start , please type '/eatntu' or 'Eat NTU' !")
      
  if keyboard.correction(msg['text'])  == 'Eatntu' or keyboard.correction(msg['text']) == 'Eat Ntu' or msg['text'] == '/eatntu':
     keyboard.customkeyboard3('Eat Out' , 'Eat In ', 'Search For Direction', "let's see what u want to do", chat_id)
  if keyboard.correction(msg['text']) == 'Eat In' :
     keyboard.customkeyboard3('Dish Name' , 'Ingredient' , "Food Type", "What do you want to search the recipe by?",chat_id)
  if keyboard.correction(msg['text']) =='Dish Name' :
     keyboard.remove_custom(chat_id)
     bot.sendMessage(chat_id, 'Key in the dish name:')
  if keyboard.correction(msg['text']) =='Ingredient' :
     keyboard.remove_custom(chat_id)
     bot.sendMessage(chat_id, 'Key in the ingredients , seperated by comas :')
  if chat_history.lastest_message1(chat_id) =='ingredient':
     bot.sendMessage(chat_id, 'Key in the ingredients you DONT WANT, seperated by comas (Psst.. if you dont have this, type Nil):')
  if keyboard.correction(msg['text']) =='Food Type':
     keyboard.remove_custom(chat_id)
     keyboard.inlinequery(chat_id, type_options + diet_options, 'Which food type are you looking for?')
 
  if chat_history.lastest_message1(chat_id) =='dish name' :
     
     food_api.new_id(chat_id,chat_id_list)

     checker = food_api.yummly_search(chat_id,chat_id_list,results_list,msg['text'], None, None, None)
     recipe_handler(checker, chat_id)
     
  if chat_history.lastest_message1(chat_id) =='ingredient' :
  	 check.ingredient = msg['text']
  	 print("##ing ", msg['text']) #checkpoint

  if chat_history.lastest_message2(chat_id) =='ingredient' :
     food_api.new_id(chat_id,chat_id_list)
     print("##in ", check.ingredient) #checkpoint
     print("##noning ", msg['text']) #checkpoint

     if keyboard.correction(msg['text']) == 'Nil':
      msg['text'] = " "
      print("##noning ", msg['text']) #checkpoint
     checker = food_api.yummly_search(chat_id,chat_id_list,results_list, None, check.ingredient, msg['text'], None)
     recipe_handler(checker, chat_id)


  if keyboard.correction(msg['text']) == 'My Dishes List' or msg['text'] == '/mydisheslist' :      
      keyboard.inlinequery10(chat_id , check.keyin, "Here are the recipes ! (again)")
  if keyboard.correction(msg['text']) == 'Eat Out' or msg['text'] == "/eatout" :
      pref.user_type[chat_id] = ''
      pref.canteen[chat_id] = ''
      pref.canteen_name[chat_id] = ''
      pref.stall[chat_id] = ''
      pref.food_type[chat_id] = ''
      keyboard.inlinequery(chat_id, ['A random dish','A Food Type','A Canteen'], 'What do you want to search?')
  if keyboard.correction(msg['text']) == 'Search For Direction' :
      keyboard.location(chat_id)
       
      
      
def recipe_handler(checker, from_id):
  if keyboard.check_error(checker, from_id) == 0:
    print("#@@ ") #checkpoint
    check.keyin = food_api.search_chat_id(from_id,results_list,1)
    keyboard.inlinequery10(from_id , check.keyin, "Here are the recipes ! (Hint: you can go back to this message if you want to find out more about other dishes; or type /mydisheslist)")  

  else:
    print("#@ ") #checkpoint
         
    bot.sendMessage(from_id , keyboard.check_error(checker, from_id)[0] )

def on_callback_query(msg): 
 query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
 
 #If the query data is in the food type list
 for i in type_options + diet_options:
      if query_data == i:
        print("## ", query_data)
        food_api.new_id(from_id, chat_id_list)
        checker = food_api.yummly_type_match(from_id, chat_id_list, results_list, query_data)
        recipe_handler(checker, from_id)
        break

 #If the query data is in my dishes list
 for i in check.keyin :
     if query_data == i :
        check.recipeindex = keyboard.list_order( i , check.keyin)
        keyboard.inlinequery10(from_id , list(headers_yummly) , " What do u want to see about " + i + "?" )
        break
 for i in check.canteen_location_list :
     if query_data == i :
         destination = google_maps.canteen_latlng("PlaceID.xlsx", "placeid", query_data)
         google_maps.new_id(from_id, chat_id_list_dir)

         print("userr location: ", check.user_location) #checkpoint
         print("dest: ", destination) #checkpoint


         google_maps.direction(from_id, chat_id_list_dir, results_list_dir, check.user_location, destination)
         instructions = google_maps.direction_instructions(from_id, results_list_dir)
         distance = google_maps.calculate_distance(from_id, results_list_dir)
         bot.sendMessage(from_id,"Here are the instructions: ")
         if isinstance(instructions, list): #check for []
          bot.sendMessage(from_id , '\n'.join(str(x) for x in instructions)) 
         else:
          bot.sendMessage(from_id , ' '.join(str(x) for x in instructions))

         bot.sendMessage(from_id,"Estimated distance: "+ str(distance))

         #send photo
         google_maps.get_photo(destination)
         bot.sendPhoto(chat_id=from_id, photo=open('phototestt1.jpeg', 'rb'))
         bot.sendMessage(from_id,"Hope you won't get lost! Type eatNTU restart")

         break 

 #If the query data is in the list of info for food API 
 for i in headers_yummly:
  if query_data == i :
    data_index = keyboard.list_order(query_data, headers_yummly)
    checker = food_api.search_chat_id(from_id, results_list, 2, check.recipeindex-1, data_index)
    print("@@@ ", check.recipeindex) #checkpoint
    print(query_data)
    if keyboard.check_error(checker, from_id) == 0:
      print("### ", check.recipeindex) #checkpoint
      print_result = food_api.search_chat_id(from_id, results_list, 2, check.recipeindex, data_index)
      print("?### ", print_result) #checkpoint
      if isinstance(print_result, list): #Check for first []
      	if isinstance(print_result[0], list): #check for second []
      		print("list~!")
      		bot.sendMessage(from_id , ', '.join(str(x) for x in print_result[0]))
      	
      	else:
      		bot.sendMessage(from_id , ' '.join(str(x) for x in print_result))
      else:
      	bot.sendMessage(from_id , print_result)
    else:
      bot.sendMessage(from_id , keyboard.check_error(checker, from_id)[0] ) 
       
     # check.keydn = []
     # check.recipeindex = 0

 chat_history.write_data(from_id,query_data)
 databasefile = open('database.txt','a')
 databasefile.writelines(str(chat_history.database))
 databasefile.close()
 

 wb = xl.load_wb('Canteen Restaurant List.xlsx')
#USER CHOOSES A RANDOM DISH
 if query_data == 'A random dish' or query_data == 'Re-random a dish':
     
    canteen_name = str(random.choice(xl.sheets(wb)))
    canteen = wb[canteen_name]
    dish_name = str(random.choice(xl.column(canteen, 'D')))
    price = str(xl.cor_content(canteen,'D','E', dish_name).value)
    stall = str(xl.stall(canteen, 'D', 'C', dish_name))
    bot.sendMessage(from_id, dish_name +', '+price+' at '+stall +' in '+ canteen_name)
    keyboard.inlinequery(from_id , ['Re-random a dish'] , 'Type "eatntu" to restart' )
#USER CHOOSES A Favorite Food Type
 if query_data == 'A Food Type':
     pref.user_type[from_id] = 'A Food Type'
     keyboard.inlinequery(from_id, xl.all_columns(wb, 'B'), 'Choose:')

 if (query_data in xl.all_columns(wb, 'B')) and pref.user_type[from_id] == 'A Food Type':
     pref.food_type[from_id] = query_data
     keyboard.inlinequery(from_id, xl.stall_and_sheet(wb, 'B', 'C', pref.food_type[from_id]), 'Here are the stalls')
 if query_data in xl.stall_and_sheet(wb, 'B', 'C', pref.food_type[from_id]):
     print(query_data.split)
     pref.stall[from_id] = query_data.split(' in ')[0]
     pref.canteen_name[from_id] = query_data.split(' in ')[1]
     pref.canteen[from_id] = wb[pref.canteen_name[from_id]]
     keyboard.inlinequery(from_id, ['All dishes', 'Healthier choices'], 'You did choose '+ query_data)
    
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
     keyboard.inlinequery(from_id, ['All dishes', 'Healthier choices'], 'You did choose '+ pref.stall[from_id]+'.')
 if query_data == 'All dishes':
     row1 = xl.row(pref.canteen[from_id], 'C', pref.stall[from_id])
     print(row1)
     row2 = xl.next_row(pref.canteen[from_id], 'C', pref.stall[from_id])
     print(row2)
     message_out = ''
     for i in range(row1, row2-2):
         message_out = message_out + str(pref.canteen[from_id]['D'][i].value) + ', ' + str(pref.canteen[from_id]['E'][i].value) + '\n'
     bot.sendMessage(from_id, message_out)
     bot.sendMessage(from_id, 'Type "eatntu" to restart')
 if query_data == 'Healthier choices':
     row1 = xl.row(pref.canteen[from_id], 'C', pref.stall[from_id])
     print(row2)
     row2 = xl.next_row(pref.canteen[from_id], 'C', pref.stall[from_id])
     print(row2)
     message_out = ''
     for i in range(row1, row2-2):
         if pref.canteen[from_id]['F'][i].value != None:
             message_out = message_out + str(pref.canteen[from_id]['D'][i].value) + ', '
     bot.sendMessage(from_id, message_out)
     bot.sendMessage(from_id, 'Type "eatntu" to restart')
     
     
             
         
     
     
     
     
     
         
     
     
 
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     

     
 print('Callback Query:', query_id, from_id, query_data)
 bot.answerCallbackQuery(query_id, text='Got it')
 


MessageLoop(bot, {'chat': on_chat_message, 
                  'callback_query': on_callback_query}).run_as_thread()


print ('Listening')
while 1 :
    time.sleep(10) 
