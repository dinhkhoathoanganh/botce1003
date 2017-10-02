
import sys
import time
import telepot
from telepot.loop import MessageLoop



#receive message
def receive_msg(msg):
 return msg['text'].lower()


#send a message
def send_msg(chat_id, content):#content(string)
 bot.sendMessage(chat_id,content)

#mainbot
def main(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
#start coding from here
 send_msg(chat_id, 'you have typed '+receive_msg(msg))

bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')
MessageLoop(bot, main).run_as_thread()
print('Listening ...')
while 1:
    time.sleep(3)
