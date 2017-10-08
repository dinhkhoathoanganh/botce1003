import telepot
from telepot.loop import MessageLoop
import time
from credentialshhanh import *
from foodapi import *
from keyboard import keyboard
from chat_history import chat_history
from xl import xl
'''
Intruction: type eatntu to restart the bot
'''
bot = telepot.Bot('449387239:AAEEseg7LHllpcAAKc_gfzEKV-VRC3CQrsU')
result_list ={}
chat_id_list =[]

headers_puppy = {0: "Puppy's Recipe directions", 1: "Puppy's Ingredients", 2: "Puppy's Image"}
headers_food2fork = {0: "Food2fork's Recipe directions", 1: "Food2fork's Image", 2: "Food2fork's Ingredients and Nutrition Facts", 3: "Food2fork's Rating"}
headers_yummly = {0: "Yummly's Recipe directions", 1: "Yummly's Image", 2: "Yummly's Ingredients", 3: "Time needed (seconds)", 4: "Flavours", 5: "Yummly's Rating"}

class check :
    keyin = []
    recipeindexdn = 9999999999
    keydn = []
    recipeindexin = 9999999999
    

def on_chat_message(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 chat_history.write_data(chat_id,msg['text'].lower())
 if keyboard.correction(msg['text']) == False :
     
     
     bot.sendMessage(chat_id , "Oops you have typed in the wrong syntax . Please type 'eatntu' to restart")
    
 
 if (keyboard.correction(msg['text']) not in ["Eatntu" , "/eatntu" , "Eat Ntu" , "Eat Out" , "/eatout" , "/eatin" , "Eat In" , "Dish Name" , "Ingredient"] and chat_history.lastest_message1(chat_id)  not in ["dish name" , "ingredient"]) : 
     bot.sendMessage(chat_id , "Oops you have typed in the wrong syntax . Please type 'eatntu' to restart")
 if keyboard.correction(msg['text'])  == 'Eatntu' or keyboard.correction(msg['text']) == 'Eat Ntu' or msg['text'] == '/eatntu':
     keyboard.customkeyboard('Eat Out' , 'Eat In ' , "let's see what u want to do", chat_id)
 elif keyboard.correction(msg['text']) == 'Eat In' :
     keyboard.customkeyboard('Dish Name' , 'Ingredient' , "What do you want to search?",chat_id)
 elif keyboard.correction(msg['text']) =='Dish Name' :
     keyboard.remove_custom(chat_id)
     bot.sendMessage(chat_id, 'Key in the dish name:')
 elif keyboard.correction(msg['text']) =='Ingredient' :
     keyboard.remove_custom(chat_id)
     bot.sendMessage(chat_id, 'Key in the ingredients , seperated by comas :')
 
 if chat_history.lastest_message1(chat_id) =='dish name' :
     
     
     
     food_api.new_id(chat_id,chat_id_list)

     checker = food_api.food2fork_search(chat_id,chat_id_list,results_list,msg['text'])

     if keyboard.check_error(checker, chat_id) == 0:
        check.keydn = food_api.search_chat_id(chat_id,results_list,1)
        keyboard.inlinequery(chat_id , check.keydn, "Here are the recipes !")
     else:
         
          bot.sendMessage(chat_id , keyboard.check_error(checker, chat_id)[0] )
     
 if chat_history.lastest_message1(chat_id) =='ingredient' :
     food_api.new_id(chat_id,chat_id_list)
     
     checker = food_api.puppy_search(chat_id,chat_id_list,results_list,msg['text'])
     print("!!a ")
     if keyboard.check_error(checker, chat_id) == 0:
        print("!!c ", keyboard.check_error(checker, chat_id))
        check.keyin = food_api.search_chat_id(chat_id,results_list,1)
        keyboard.inlinequery(chat_id , check.keyin, "Here are the recipes !")

     else:
       
        bot.sendMessage(chat_id , keyboard.check_error(checker, chat_id)[0] )
    



     
     
     
 

     
     
     
     

     
     
 
     
     
     
     
  

 




def on_callback_query(msg): 
 query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
 for i in check.keydn :
     if query_data == i :
        
        check.recipeindexdn = keyboard.list_order( i , check.keydn)
        recipe_index = check.recipeindexdn
        keyboard.inlinequery(from_id , list(headers_food2fork.values()) , " What do u want to see about " + i + "?" )
 for i in check.keyin :
     if query_data == i :
        
        check.recipeindexin = keyboard.list_order( i , check.keyin)
        recipe_index = check.recipeindexin
        keyboard.inlinequery(from_id , list(headers_puppy.values()), " What do u want to see about " + i + "?" )
 
 if query_data in  list(headers_food2fork.values()) :
    
     data_index = keyboard.list_order(query_data ,list(headers_food2fork.values()))
     checker = food_api.search_chat_id(from_id, results_list, 2, check.recipeindexdn, data_index)

     if keyboard.check_error(checker, from_id) == 0:
        bot.sendMessage(from_id ,food_api.search_chat_id(from_id, results_list, 2, check.recipeindexdn, data_index))
     else:
         bot.sendMessage(from_id , keyboard.check_error(checker, from_id)[0] ) 
        
     # check.keydn = []
     # check.recipeindexdn = 0
         
 if query_data in  list(headers_puppy.values()):
     data_index = keyboard.list_order(query_data ,list(headers_puppy.values()))

     print("@@ ", data_index) #checkpoint
     print("@@ ", check.recipeindexin) #checkpoint

     checker = food_api.search_chat_id(from_id, results_list, 2, check.recipeindexin, data_index)
     
     if keyboard.check_error(checker, from_id) == 0:
        bot.sendMessage(from_id ,food_api.search_chat_id(from_id, results_list, 2, check.recipeindexin, data_index))
     else:
        bot.sendMessage(from_id , keyboard.check_error(checker, from_id)[0] )

     
        
 
     
     
 print('Callback Query:', query_id, from_id, query_data)
 bot.answerCallbackQuery(query_id, text='Got it')
 


MessageLoop(bot, {'chat': on_chat_message, 
                  'callback_query': on_callback_query}).run_as_thread()


print ('Listening')
while 1 :
    time.sleep(10) 
