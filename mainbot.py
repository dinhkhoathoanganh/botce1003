
import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply


#receive message
def receive_msg(msg):
 return msg['text'].lower()


#send a message
def send_msg(chat_id, content):#content(string)
 bot.sendMessage(chat_id,content)

#send a custom keyboard example
def custom_key()
  markup = ReplyKeyboardMarkup(keyboard=[['Plain text'],['Testing text'],])
  bot.sendMessage(chat_id, 'Custom keyboard with various buttons', reply_markup=markup)
#remove keyboard
def remove_key()
 markup = ReplyKeyboardRemove()
 bot.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)
#mainbot
def main(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
#start coding from here



bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')
MessageLoop(bot, main).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(3)
