import time
import datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton



#print message content
def content(msg):
 print('message:',msg['text'])
 return msg['text']


#send a message
def send(content):#content(string)
 bot.sendMessage(chat_id,content)



#send a multiple-choice question
def send_mcq(chat_id, question, keyboard_list):#question(string) keyboard_list is a list including elements with forms <KeyboardButton(text='<string name of the button>')>. Example: [KeyboardButton(text='Yes'),KeyboardButton(text='No')].
 bot.sendMessage(chat_id, question, reply_markup=ReplyKeyboardMarkup(keyboard=[keyboard_list]))







#Mainbot starts from here
def mainbot(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 #start coding from here


bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')#paste the key here
MessageLoop(bot, mainbot).run_as_thread()
print ('Listening ...')


# Keep the program running.
while 1:
 time.sleep(10)
