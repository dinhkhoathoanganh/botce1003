import telepot
from pprint import pprint
from telepot.loop import MessageLoop
import sys
import time
from telepot.namedtuple import InlineKeyboardMarkup , InlineKeyboardButton

bot = telepot.Bot('449387239:AAEEseg7LHllpcAAKc_gfzEKV-VRC3CQrsU')

response = bot.getUpdates()
#pprint(response)

def check_data(msg) :
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    return query_data


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text= 'Eat Out', callback_data='EatOut')],[InlineKeyboardButton(text= 'Eat In', callback_data='EatIn')],])

    bot.sendMessage(chat_id, 'What do you want to do ?', reply_markup=keyboard)
    


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    if query_data == "EatOut" :
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text= 'Canteen1', callback_data='Canteen1')],[InlineKeyboardButton(text= 'Canteen2', callback_data='Canteen2')],])
        bot.sendMessage(from_id, 'Here is the list of the canteen', reply_markup=keyboard)
        
            
    elif query_data == "EatIn" :
       
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text= 'Chinese Cuisine', callback_data='Chinese Cuisine')],[InlineKeyboardButton(text= 'PhoBo', callback_data='PhoBo')],])
        bot.sendMessage(from_id, ' So you are interested in cooking ? ', reply_markup=keyboard)
    elif query_data == 'Canteen1' :
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text= 'Not Available yet', callback_data='Not Yet')],])
        bot.sendMessage(from_id, ' Oops , sorry we havent got any data for this now ', reply_markup=keyboard)
        



    bot.answerCallbackQuery(query_id, text='Got it')    
    
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

#MessageLoop(bot, {on_chat_message , on_callback_query
 #                 }).run_as_thread()

print ('Listening')
while 1 :
    time.sleep(10)
