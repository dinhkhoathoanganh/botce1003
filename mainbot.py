import time
import threading
import random
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent



#print message content
def content_msg(msg):
 return msg['text'].lower()


#send a message
def send_msg(chat_id, content):#content(string)
 bot.sendMessage(chat_id,content)



#send a multiple-choice question
def send_mcq(chat_id, question, keyboard_list):#question(string) keyboard_list is a list including elements with forms <KeyboardButton(text='<string name of the button>')>. Example: [KeyboardButton(text='Yes'),KeyboardButton(text='No')].
 bot.sendMessage(chat_id, question, reply_markup=ReplyKeyboardMarkup(keyboard=[keyboard_list]))

#request location
def request_location(chat_id):
 markup = ReplyKeyboardMarkup(keyboard=[
                     ['Plain text', KeyboardButton(text='Text only')],
                     [dict(text='Phone', request_contact=True), KeyboardButton(text='Location', request_location=True)],
                 ])
 bot.sendMessage(chat_id, 'Share your location to get the direction', reply_markup=markup)



#call back
def call_back():
 mainbot()

#Mainbot starts from here
def mainbot(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 if content_msg(msg) == 'hello':
  request_location(chat_id)
 send_msg(chat_id, 'done')








bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')
MessageLoop(bot,{'chat':mainbot,'call_back': call_back}).run_as_thread()
print ('Listening ...')


# Keep the program running.
while 1:
 time.sleep(10)
