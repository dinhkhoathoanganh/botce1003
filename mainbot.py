
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

#send a custom keyboard
def custom_key(chat_id, question, choices_list): #choices_list must be a list of string.
 execmarkup = ''
 for i in range(len(choices_list)):
  execmarkup = execmarkup + '['+ choices_list[i]+'],'
 execmarkup0 = 'markup = ReplyKeyboardMarkup(keyboard=[' + execmarkup + '])'
 exec(execmarkup0)
 bot.sendMessage(chat_id, question, reply_markup=markup)
#mainbot
def main(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
#start coding from here
 send_msg(chat_id, 'testing')
 print(receive_msg(msg))
 if receive_msg(msg) == 'hello':
  markup = ReplyKeyboardMarkup(keyboard=[['Plain text'],['Testing text'],])
  bot.sendMessage(chat_id, 'Custom keyboard with various buttons', reply_markup=markup)


bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')
MessageLoop(bot, main).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(3)
