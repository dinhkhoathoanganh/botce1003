import telepot
from telepot.loop import MessageLoop
import time
import random
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
 chat_history.write_data(chat_id, msg['text'].lower())
 
 if (keyboard.correction(msg['text']) not in ["Eatntu" , "/eatntu" , "Eat Ntu" , "Eat Out" , "/eatout" , "/eatin" , "Eat In" , "Dish Name" , "Ingredient"] and chat_history.lastest_message1(chat_id)  not in ["dish name" , "ingredient"]) or keyboard.correction(msg['text']) == False : 
     bot.sendMessage(chat_id , "Oops you have typed in the wrong syntax . Please type 'eatntu' to restart")
 if keyboard.correction(msg['text'])  == 'Eatntu' or keyboard.correction(msg['text']) == 'Eat Ntu' or msg['text'] == '/eatntu':
     keyboard.customkeyboard('Eat Out' , 'Eat In ' , "let's see what u want to do", chat_id)
 if keyboard.correction(msg['text']) == 'Eat In' :
     keyboard.customkeyboard('Dish Name' , 'Ingredient' , "What do you want to search?",chat_id)
 if keyboard.correction(msg['text']) =='Dish Name' :
     keyboard.remove_custom(chat_id)
     bot.sendMessage(chat_id, 'Key in the dish name:')
 if keyboard.correction(msg['text']) =='Ingredient' :
     keyboard.remove_custom(chat_id)
     bot.sendMessage(chat_id, 'Key in the ingredients , seperated by comas :')
 
 if chat_history.lastest_message1(chat_id) =='dish name' :
     
     
     
     food_api.new_id(chat_id,chat_id_list)

     checker = food_api.food2fork_search(chat_id,chat_id_list,results_list,msg['text'])

     if keyboard.check_error(checker, chat_id) == 0:
        check.keydn = food_api.search_chat_id(chat_id,results_list,1)
        keyboard.inlinequery10(chat_id , check.keydn, "Here are the recipes !")
     else:
         
          bot.sendMessage(chat_id , keyboard.check_error(checker, chat_id)[0] )
     
 if chat_history.lastest_message1(chat_id) =='ingredient' :
     food_api.new_id(chat_id,chat_id_list)
     
     checker = food_api.puppy_search(chat_id,chat_id_list,results_list,msg['text'])
     print("!!a ")
     if keyboard.check_error(checker, chat_id) == 0:
        print("!!c ", keyboard.check_error(checker, chat_id))
        check.keyin = food_api.search_chat_id(chat_id,results_list,1)
        keyboard.inlinequery10(chat_id , check.keyin, "Here are the recipes !")

     else:
       
        bot.sendMessage(chat_id , keyboard.check_error(checker, chat_id)[0] )

 if keyboard.correction(msg['text']) == 'Eat Out' or msg['text'] == '/eatout' :
      
      keyboard.inlinequery(chat_id, ['A random dish','A Canteen', 'A Stall'], 'Choose one:')
      
      
    



     
     
     
 

     
     
     
     

     
     
 
     
     
     
     
  

 




def on_callback_query(msg): 
 query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
 for i in check.keydn :
     if query_data == i :
        
        check.recipeindexdn = keyboard.list_order( i , check.keydn)
        recipe_index = check.recipeindexdn
        keyboard.inlinequery10(from_id , list(headers_food2fork.values()) , " What do u want to see about " + i + "?" )
 for i in check.keyin :
     if query_data == i :
        
        check.recipeindexin = keyboard.list_order( i , check.keyin)
        recipe_index = check.recipeindexin
        keyboard.inlinequery10(from_id , list(headers_puppy.values()), " What do u want to see about " + i + "?" )
 
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
 chat_history.write_data(from_id,query_data)
 databasefile = open('database.txt','a')
 databasefile.writelines(str(chat_history.database))

 wb = xl.load_wb('Canteen Restaurant List.xlsx')
 #USER CHOOSE CANTEEN FIRST
 if query_data == 'A Canteen':
    keyboard.inlinequery(from_id, xl.sheets(wb), 'Choose a canteen:')
 if chat_history.lastest_message1(from_id) == 'A Canteen':
    canteen = xl.load_ws(wb, query_data) #canteen is the sheet user has chosen
    print(canteen)
    canteen_name = str(query_data)
    keyboard.inlinequery(from_id, xl.column(canteen,'C'), 'You did choose '+ canteen_name +' ,Choose a stall')
 if chat_history.lastest_message2(from_id) == 'A Canteen':
    keyboard.inlinequery(from_id, ['All dishes','Recommended ones'], 'Do you want to get all the dishes or recommended by our users?')

 if query_data == 'All dishes' and chat_history.lastest_message3(from_id) == 'A Canteen':
    canteen = xl.load_ws(wb,chat_history.lastest_message2(from_id))
    stall_name = chat_history.lastest_message1(from_id)
    print(stall_name)
    row1 = xl.rowlist(canteen, 'C', stall_name)[0]
    row2 = xl.rowlist(canteen, 'C', stall_name)[1]
    for i in range(row1, row2 +1):
        bot.sendMessage(from_id, xl.cell(canteen,'D'+str(i))+', '+xl.cell(canteen,'E'+str(i)))
        bot.sendMessage(from_id, '...')
        bot.sendMessage(from_id, 'Type "eatntu" to restart')
 if query_data == 'Recommended ones' and chat_history.lastest_message3(from_id) == 'A Canteen':
    canteen = xl.load_ws(wb,chat_history.lastest_message2(from_id))
    stall_name = chat_history.lastest_message1(from_id)
    print(stall_name)
    row1 = xl.rowlist(canteen, 'C', stall_name)[0]
    row2 = xl.rowlist(canteen, 'C', stall_name)[1]
    for i in range(row1, row2 +1):
        if 'Yes' in xl.cell(canteen,'F'+str(i)):
            bot.sendMessage(from_id, xl.cell(canteen,'D'+str(i))+', '+xl.cell(canteen,'E'+str(i)),', '+xl.cell(canteen,'F'+str(i)))
            bot.sendMessage(from_id, '...')
    bot.sendMessage(from_id, 'Type "eatntu" to restart')
 #USER CHOOSE STALL FIRST
 if query_data == 'A Stall':
    
    stall_list = []
    for i in range(len(xl.sheets(wb))):
        
        stall_list = stall_list + xl.column(wb[xl.sheets(wb)[i]], 'C')
    stall_list2 = []
    
    for e in stall_list:
        if e not in stall_list2:
            stall_list2.append(e)
    
    keyboard.inlinequery(from_id , stall_list2 , 'Choose a stall')

 if chat_history.lastest_message1(from_id) == 'A Stall':
     stall_name = query_data
     canteen_list = []
     for i in range(len(xl.sheets(wb))):
        if stall_name in xl.column(xl.load_ws(wb, xl.sheets(wb)[i]), 'C'):
            canteen_list = canteen_list + [xl.sheets(wb)[i]]
        keyboard.inlinequery(from_id, canteen_list, 'Here is the list of canteen which has your chosen stall')
 if chat_history.lastest_message2(from_id) == 'A Stall':
     keyboard.inlinequery(from_id, ['All dishes','Recommended ones'], 'Do you want to get all the dishes or recommended by our users?')
      
 if query_data == 'All dishes' and chat_history.lastest_message3(from_id) == 'A Stall':
    canteen = xl.load_ws(wb,chat_history.lastest_message1(from_id))
    stall_name = chat_history.lastest_message2(from_id)
    print(stall_name)
    row1 = xl.rowlist(canteen, 'C', stall_name)[0]
    row2 = xl.rowlist(canteen, 'C', stall_name)[1]
    for i in range(row1, row2 +1):
        bot.sendMessage(from_id, xl.cell(canteen,'D'+str(i)) +', '+xl.cell(canteen,'E'+str(i)))
        bot.sendMessage(from_id, '...')
    bot.sendMessage(from_id, 'Type "eatntu" to restart')
 if query_data == 'Recommended ones' and chat_history.lastest_message3(from_id) == 'A Stall':
    canteen = xl.load_ws(wb,chat_history.lastest_message1(from_id))
    stall_name = chat_history.lastest_message2(from_id)
    print(stall_name)
    row1 = xl.rowlist(canteen, 'C', stall_name)[0]
    row2 = xl.rowlist(canteen, 'C', stall_name)[1]
    for i in range(row1, row2 +1):
        if 'Yes' in xl.cell(canteen,'F'+str(i)):
            bot.sendMessage(from_id, xl.cell(canteen,'D'+str(i)) +', '+ xl.cell(canteen,'E'+str(i)) +', '+ xl.cell(canteen,'F'+str(i)))
            bot.sendMessage(from_id, '...')
        bot.sendMessage(from_id, 'Type "eatntu" to restart')
 #USER CHOOSE A RANDOM DISH
 if query_data == 'A random dish' or query_data == 'Re-random a dish':
    canteen_name = str(random.choice(xl.sheets(wb)))
    canteen = xl.load_ws(wb, canteen_name)
    dish_name = str(random.choice(xl.column(canteen, 'D')))
    price = xl.cor_content(canteen,'D','E', dish_name)
    stall_name = xl.stall(canteen, 'D', 'C', dish_name)
    bot.sendMessage(from_id, dish_name +', '+price+' at '+stall_name +' in '+ canteen_name)
    keyboard.inlinequery(from_id , ['Re-random a dish'] , 'Type "eatntu" to restart' )


 databasefile.close()
     
 
        
        
    
    
    
     
     
     

 
    
     
         
         
     
     
     
     
     
             
     
     

 
        
         
     
     
    
 

    
     
        
 
     
     
 print('Callback Query:', query_id, from_id, query_data)
 bot.answerCallbackQuery(query_id, text='Got it')
 


MessageLoop(bot, {'chat': on_chat_message, 
                  'callback_query': on_callback_query}).run_as_thread()


print ('Listening')
while 1 :
    time.sleep(20) 
