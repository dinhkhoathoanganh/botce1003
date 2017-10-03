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
bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')

def on_chat_message(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 chat_history.write_data(chat_id,msg['text'].lower())
 databasefile = open('database.txt','a')
 databasefile.writelines(str(chat_history.database))
 if msg['text'].lower() == 'eatntu':
  keyboard.inlinequery(chat_id, ['A random dish','A Canteen', 'A Stall'], 'Choose one:')

 databasefile.close()


def on_callback_query(msg): 
 query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
 print('Callback Query:', query_id, from_id, query_data)
 bot.answerCallbackQuery(query_id, text='Got it')    
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

MessageLoop(bot, {'chat': on_chat_message, 
                  'callback_query': on_callback_query}).run_as_thread()


print ('Listening')
while 1 :
    time.sleep(1) 
