
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

#send a inline keyboard
 


#mainbot
def main(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)






bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')
MessageLoop(bot, mainbot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(3)
