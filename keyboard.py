
import telepot

from telepot.loop import MessageLoop

import time

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')
class keyboard :
    def customkeyboard(choice1 , choice2 , message, msg) :
        content_type, chat_type, chat_id = telepot.glance(msg)
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah , got it !', reply_markup=markup)
        markup = ReplyKeyboardMarkup(keyboard=[
                    [ choice1 , KeyboardButton(text= choice2 )],])
                 
        bot.sendMessage(chat_id, message, reply_markup=markup)

    def inlinequery(chatid , listx , chat ) :
        all = []
        for i in listx :
          element = [InlineKeyboardButton(text=  i , callback_data = i)]
          all.append(element)
        keyboard = InlineKeyboardMarkup(inline_keyboard= all)
        bot.sendMessage(chatid, chat, reply_markup=keyboard)
    def remove_custom(chat_id) :
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah , got it !', reply_markup=markup)
    
 

# listx o duoi dang list
# i , chat o duoi dang string
# chatid la id cua user
# Function nay lay chat id va chat can gui , gui lai chat do va cac du lieu trong list cho nguoi dung duoi dang inline query  

