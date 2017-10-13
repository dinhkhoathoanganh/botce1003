
import telepot

from telepot.loop import MessageLoop

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
bot = telepot.Bot('406130496:AAFNc17PwDi7mmsYVAg2bYBtsc1LR1OlqVg')
class keyboard :
    
# remove the existing custom keyboard , then create a custom keyboard of 2 choices ( choice1 and choice2 ), then send it together with a message to the given chat id .
    def customkeyboard(choice1 , choice2 , chat , chat_id) :
           
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah, got it!', reply_markup=markup)
        markup = ReplyKeyboardMarkup(keyboard=[[ choice1 , KeyboardButton(text= choice2 )],], resize_keyboard=True)
                 
        bot.sendMessage(chat_id, chat, reply_markup=markup)
       
# remove the existing custom keyboard , then create a custom keyboard of 3 choices ( choice1 , choice2 , choice3 ), then send it together with a message to the given chat id .
    def customkeyboard3(choice1 , choice2, choice3 , chat , chat_id) :
        
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah, got it!', reply_markup=markup)
        markup = ReplyKeyboardMarkup(keyboard=[[ choice1 , choice2,], 
                                                [choice3],], resize_keyboard=True)
                 
        bot.sendMessage(chat_id, chat, reply_markup=markup)
# Send a location request to the given chat id
    def location(chat_id) :
        markup = ReplyKeyboardRemove()
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Sure! Send My Location',request_location=True)]], resize_keyboard=True, one_time_keyboard=True)
        bot.sendMessage(chat_id, 'Give location?', reply_markup=keyboard)
        
    
# listx is a list of string . Create an inline query , with choices are the first 10 string elements in listx , then send it together with a chat to the given chat id .
    def inlinequery10(chatid , listx , chat ) :
        all = []
        print("#### ", listx)
        for i in listx[:10]: #Only take first 10 top results (not to spam the bot chat)
          element = [InlineKeyboardButton(text=  i , callback_data = i)]
          all.append(element)
        keyboard = InlineKeyboardMarkup(inline_keyboard= all)
        bot.sendMessage(chatid , chat , reply_markup=keyboard)
        
# listx is a list of string . Create an inline query , with choices are strings in listx , then send it together with a chat to the given chat id .
   
    def inlinequery(chatid , listx , chat ) :
        all = []

        print(listx) #checkpoint


        for i in listx: 
          element = [InlineKeyboardButton(text=  i , callback_data = i)]
          all.append(element)
        print("!@#!#@#")
        keyboard = InlineKeyboardMarkup(inline_keyboard= all)
        bot.sendMessage(chatid , chat , reply_markup=keyboard)

#Check if there is an error from the api call
    def check_error(checker, chat_id):
        if (isinstance(checker,dict)):
            if (list(checker)[0] == "Error"):
                return checker["Error"]
            elif (list(checker[chat_id])[0] == "Error"):
                return checker[chat_id]["Error"]
            else:
                return 0
        else:
            return 0
# remove the current custom keyboard from the chat with the given chat id        

    def remove_custom(chat_id) :
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah , got it !', reply_markup=markup)
# check whether a string is in a list and return the order of the string in the list 

    def list_order ( string , listt ) :
        count = 0
        for i in listt :
            count += 1
            if string == i :
                break
        return (count)
# correct the string x such that : + No spaces at the start or end of the string 
#                                  + Each word is seperated by EXACTLY ONE space . 
#                                  + Every word has its first letter written in upper case .            
        
    def correction(x) :
        if len(x) == 1 :
            return (False)

        x = x.lower()
        last = len(x)-1
        first_space = 0
        for i in range( 0 , last+1) :
            if x[i] == " " :
                first_space += 1 
            else :
                break
        x = x[first_space:]

       

        last = len(x) -1
        last_space = 0
        for i in range (0 , last+1):
            j = -i-1
            if x[j] == " " :
                last_space += 1 
            else :
                break
        x = x[:last-last_space+1]
        x = x.lower()
        last = len(x)-1
        viethoa = x[0].upper()
        x = viethoa + x[1:]

        
        raw = x
        for i in range(0,last+1) :
            if i > len(x)-1 :
                break
        
            if x[i] == " " :
                count = 0
                for j in range ( i+1 , last + 1):
                    if x[j] == " " :
                        count +=1
                    else :
                        break
                x = x[:i+1] + x[i+count+1:]

        
        last = len(x)-1

        for i in range ( 1 ,last-1) :
            if x[i] == " " :
                viethoa = x[i+1].upper()
                x = x[:i+1] + viethoa + x[i+2:]
        
        if x[-2] == " " :
            x = x[:last] + x[-1].upper()
        
        return(x)
        

    
 

