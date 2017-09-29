
import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent


#receive message
def receive_msg(msg):
 return msg['text'].lower()


#send a message
def send_msg(chat_id, content):#content(string)
 bot.sendMessage(chat_id,content)

#send a custom keyboard
def custom_key(chat_id, question, choices_list): #choices_list must be a list of string.
 keyboard = [[choices_list[0], KeyboardButton(text=choices_list[0])],]
 for i in range(1,len(choices_list)):
  keyboard = keyboard + [choices_list[i], KeyboardButton(text=choices_list[i])]
 markup = ReplyKeyboardMarkup(keyboard)
 bot.sendMessage(chat_id, question, reply_markup=markup)
  

#mainbot
def main(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
#start coding from here





bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')
MessageLoop(bot, main).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(3)
