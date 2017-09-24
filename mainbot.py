
import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton



#message content
def content_msg(msg):
 return msg['text'].lower()


#send a message
def send_msg(chat_id, content):#content(string)
 bot.sendMessage(chat_id,content)


#send a inlinekeyboard
def inline_mcq(chat_id):
#question(string) choice_number(integer) choices(list)
#example for an array: (['press 1',1],['press 2',2],['press 3',3])
#(1) is a list or an integer, (1,) is a tuple
 keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Press me', callback_data='press')],])
# print('inline keyboard type', type(inline_keyboard))
#For this case, i will use exec statement.[tested]


 bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)


    

def on_callback_query(msg):
 query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
 print('Callback Query:',query_data)


# bot.answerCallbackQuery(query_id, text='Got it')

#mainbot
def on_chat_message(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
#test
 inline_mcq(chat_id)

#endtest











bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')
MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
