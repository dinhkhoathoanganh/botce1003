import telepot
from telepot.loop import MessageLoop
import time
import random
from credentialshhanh import *
from foodapi import *
from keyboard import keyboard
from chat_history import chat_history
from xl import xl
from preferences import pref
'''
Intruction: type eatntu to restart the bot
'''
bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')

def on_chat_message(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 chat_history.write_data(chat_id,msg['text'].lower())
 databasefile = open('database.txt','a')
 databasefile.writelines(str(chat_history.database))
 databasefile.close()
 if msg['text'] == 'Eat Out':
  pref.user_type[chat_id] = ''
  pref.canteen[chat_id] = ''
  pref.canteen_name[chat_id] = ''
  pref.stall[chat_id] = ''
  pref.food_type[chat_id] = ''
  keyboard.inlinequery(chat_id, ['A random dish','A Food Type','A Canteen'], 'Choose one:')




def on_callback_query(msg): 
 query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
 print('Callback Query:', query_id, from_id, query_data)
 bot.answerCallbackQuery(query_id, text='Got it! '+ query_data )    
 chat_history.write_data(from_id,query_data)
 databasefile = open('database.txt','a')
 databasefile.writelines(str(chat_history.database))
 databasefile.close()

 wb = xl.load_wb('Canteen Restaurant List.xlsx')


#USER CHOOSES A RANDOM DISH
 if query_data == 'A random dish' or query_data == 'Re-random a dish':
  canteen_name = str(random.choice(xl.sheets(wb)))
  canteen = xl.load_ws(wb, canteen_name)
  dish_name = str(random.choice(xl.column(canteen, 'D')))
  price = xl.cor_content(canteen,'D','E', dish_name)
  stall_name = xl.stall(canteen, 'D', 'C', dish_name)
  bot.sendMessage(from_id, dish_name +', '+price+' at '+stall_name +' in '+ canteen_name)
  keyboard.inlinequery(from_id , ['Re-random a dish'] , 'Type "eatntu" to restart' ) 


#USER CHOOSES A Favorite Food Type
 if query_data == 'A Food Type':
  pref.user_type[from_id] = 'A Food Type'
  keyboard.inlinequery(from_id, xl.all_columns(wb, 'B'), 'Choose:')

 if (query_data in xl.all_columns(wb, 'B')) and pref.user_type[from_id] == 'A Food Type':
  pref.food_type[from_id] = query_data
  keyboard.inlinequery(from_id, xl.stall_and_sheet(wb, 'B', 'C', pref.food_type[from_id]), 'Here is the stalls')

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
    message_out = message_out + str(pref.canteen[from_id]['D'][i].value) + ', ' + str(pref.canteen[from_id]['E'][i].value) + ', ' + str(pref.canteen[from_id]['F'][i].value) + '\n'
  bot.sendMessage(from_id, message_out)
  bot.sendMessage(from_id, 'Type "eatntu" to restart')


   










MessageLoop(bot, {'chat': on_chat_message, 
                  'callback_query': on_callback_query}).run_as_thread()


print ('Listening')
while 1 :
    time.sleep(1) 
