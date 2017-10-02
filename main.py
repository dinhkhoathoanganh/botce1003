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
bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')

def on_chat_message(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 chat_history.write_data(chat_id,msg['text'].lower())
 
 if msg['text'].lower() == 'eatntu':
  keyboard.inlinequery(chat_id, ['A random dish','A Canteen', 'A Stall'], 'Choose one:')

 




def on_callback_query(msg): 
 query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
 print('Callback Query:', query_id, from_id, query_data)
 bot.answerCallbackQuery(query_id, text='Got it')    
 chat_history.write_data(from_id,query_data)
 chat_history.show_chat(from_id)


# if query_data == 'A random dish':
 wb = xl.load_wb('Canteen Restaurant List.xlsx')
 if query_data == 'A Canteen':
  keyboard.inlinequery(from_id, xl.sheets(wb), 'Choose a canteen:')

 if chat_history.lastest_message(from_id) == 'A Canteen':
  canteen = xl.load_ws(wb, query_data) #canteen is the sheet user has chosen
  print(canteen)
  canteen_name = str(query_data)
  keyboard.inlinequery(from_id, xl.column(canteen,'C'), 'You did choose '+ canteen_name +' ,Choose a stall')

 if chat_history.lastest_message2(from_id) == 'A Canteen':
  stall = str(query_data) #stall is the name of stall (str)
  keyboard.inlinequery(from_id, ['All dishes','Recommended ones'], 'Do you want to get all the dishes or recommended by our users?')

 if query_data == 'All dishes':
  canteen = xl.load_ws(wb,chat_history.lastest_message2(from_id))
  stall_name = chat_history.lastest_message(from_id)
  print(stall_name)
  row1 = xl.rowlist(canteen, 'C', stall_name)[0]
  row2 = xl.rowlist(canteen, 'C', stall_name)[1]
  for i in range(row1, row2 +1):
   bot.sendMessage(from_id, xl.cell(canteen,'D'+str(i)))
   bot.sendMessage(from_id, xl.cell(canteen,'E'+str(i)))
   bot.sendMessage(from_id, '...')

  bot.sendMessage(from_id, 'Type "eatntu" to restart')
 


MessageLoop(bot, {'chat': on_chat_message, 
                  'callback_query': on_callback_query}).run_as_thread()


print ('Listening')
while 1 :
    time.sleep(1) 
