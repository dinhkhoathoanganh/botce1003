import telepot
from pprint import pprint
from telepot.loop import MessageLoop
import sys
import time
import threading
import random
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

bot = telepot.Bot('449387239:AAEEseg7LHllpcAAKc_gfzEKV-VRC3CQrsU')



response = bot.getUpdates()
#pprint(response)

message_with_inline_keyboard = None
class check:
    filename = []

def customkeyboard(choice1 , choice2 , message, msg) :
    content_type, chat_type, chat_id = telepot.glance(msg)
    markup = ReplyKeyboardRemove()
    bot.sendMessage(chat_id, 'Oke lah , got it !', reply_markup=markup)
    markup = ReplyKeyboardMarkup(keyboard=[
                    [ choice1 , KeyboardButton(text= choice2 )],])
                 
    bot.sendMessage(chat_id, message, reply_markup=markup)

    


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    command = msg['text'][-1:].lower()
    
    if msg['text'] == 'eatntu':
        customkeyboard('Eat In' , 'Eat Out' , 'Let us see what you want to do!',msg)

    if msg['text'] == 'Eat In' or msg['text'] == "/eatin" :
        customkeyboard('Dish Name','Ingredient','Do you want to search by dish name or by ingredient ?',msg)

    if 'Ingredient' in check.filename or 'Dish Name' in check.filename :
        print (msg['text'])
        # Phan cua chi Hoang Anh day 



        
        check.filename = []

    if msg['text'] == "Dish Name" :
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah , got it !', reply_markup=markup)
        bot.sendMessage(chat_id, 'Key in the dish name:')
        
    if msg['text'] == "Ingredient" :
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah , got it !', reply_markup=markup)
        bot.sendMessage(chat_id, 'Key in the ingredients you want , seperated by comas :')

    check.filename = check.filename + [msg['text']]
    if msg['text'] == "Eat Out" or msg['text'] == "/eatout" :
        customkeyboard('Yes,I do','No , suggest me please','Do you know where you want to eat ?',msg)
    if msg['text'] == 'Yes, I do' :
        
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah , got it !', reply_markup=markup)
        
        bot.sendMessage(chat_id, "Here's the list of canteens")# , reply_markup=keyboard)
    if msg['text'] == 'No , suggest me please' :
        customkeyboard('Location','Food','Do you want suggestions based on food or location ?',msg)
       


        
        
               
#This function works on the input chat message of the user . The below function works on the callback query of the user , so we need to put them in seperate parts , although it might look the same ~~
    

    
    


def on_callback_query(msg): 
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    
#    if query_data == "EatOut" :
#        
#        keyboard = InlineKeyboardMarkup(inline_keyboard=[
#                   [InlineKeyboardButton(text= 'Yes , I do', callback_data='Yes')],[InlineKeyboardButton(text= 'No , suggest me please', callback_data='No')],])
#        bot.sendMessage(from_id, 'Do you know where you want to eat ?', reply_markup=keyboard)
#    if query_data == 'Yes' :
#        bot.sendMessage(from_id, "Here's the list of canteens", reply_markup=keyboard)

#    if query_data == 'No' :
#        keyboard = InlineKeyboardMarkup(inline_keyboard=[
#                   [InlineKeyboardButton(text= '', callback_data='Location')],[InlineKeyboardButton(text= 'Food', callback_data='Food')],])
#        bot.sendMessage(from_id, 'Do you want to choose based on location or food ?', reply_markup=keyboard)
        
        
        
            







    bot.answerCallbackQuery(query_id, text='Got it')    
    
MessageLoop(bot, {'chat': on_chat_message, 
                  'callback_query': on_callback_query}).run_as_thread()

#MessageLoop(bot, {on_chat_message , on_callback_query
 #                 }).run_as_thread()

print ('Listening')
while 1 :
    time.sleep(10) 
