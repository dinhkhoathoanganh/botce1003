import time
import datetime
import telepot
from telepot.loop import MessageLoop
#sendmsg
def sendmsg(userid,content):
 bot.sendMessage(userid,conten)
#userid
def userid(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 return chat_id
#username
def username(msg):
 return msg['from']['first_name']+msg['from']['last_name']
#





#receive message and answer
def handle(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 print('msg=',msg)
 print('message:',msg['text'])
 print('glance:',content_type, chat_type, chat_id)
 msgfrom=msg['from']
 print(msgfrom, type(msgfrom))
#answer a msg with 'dit me'
 if True:
  bot.sendMessage(chat_id, 'dit me '+msgfrom['first_name']+' '+msgfrom['last_name'])
#print the time
  bot.sendMessage(chat_id,'bay gio la may gio nhi? :'+str(datetime.datetime.now()))










#bot started
bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')#paste the key here
bot.message_loop(handle)
print ('Listening ...')

