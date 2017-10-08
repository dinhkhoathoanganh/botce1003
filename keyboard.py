import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

bot = telepot.Bot('446414243:AAG13E9L9ifrrYJc0JNHIHMpHBK-306sd2A')
class keyboard :
    def customkeyboard(choice1 , choice2 , chat , chat_id) :
        
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah , got it !', reply_markup=markup)
        markup = ReplyKeyboardMarkup(keyboard=[
                    [ choice1 , KeyboardButton(text= choice2 )],])
                 
        bot.sendMessage(chat_id, chat, reply_markup=markup)
    def customkeyboard3(choice1 , choice2, choice3 , chat , chat_id) :
        
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah , got it !', reply_markup=markup)
        markup = ReplyKeyboardMarkup(keyboard=[
                    [ choice1 , choice2, choice3],])
                 
        bot.sendMessage(chat_id, chat, reply_markup=markup)

    def inlinequery10(chatid , listx , chat ) :
        all = []
        for i in listx[:10]: #Only take first 10 top results (not to spam the bot chat)
          element = [InlineKeyboardButton(text=  i , callback_data = i)]
          all.append(element)
        keyboard = InlineKeyboardMarkup(inline_keyboard= all)
        bot.sendMessage(chatid , chat , reply_markup=keyboard)

    def inlinequery(chatid , listx , chat ) :
        all = []
        for i in listx: 
          element = [InlineKeyboardButton(text=  i , callback_data = i)]
          all.append(element)
        keyboard = InlineKeyboardMarkup(inline_keyboard= all)
        bot.sendMessage(chatid , chat , reply_markup=keyboard)

    def check_error(checker, chat_id):
        print("!!b ", checker)
        if (isinstance(checker,dict)):
            if (list(checker)[0] == "Error"):
                return checker["Error"]
            elif (list(checker[chat_id])[0] == "Error"):
                return checker[chat_id]["Error"]
            else:
                return 0
        else:
            return 0

# listx o duoi dang list
# i , chat o duoi dang string
# chatid la id cua user
# Function nay lay chat id va chat can gui , gui lai chat do va cac du lieu trong list cho nguoi dung duoi dang inline query          

    def remove_custom(chat_id) :
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Oke lah , got it !', reply_markup=markup)

    def list_order ( string , listt ) :
        count = 0
        for i in listt :
            count += 1
            if string == i :
                break
        return (count)
            
        
    def correction(x) :
        if len(x) == 1 :
            return (False)
        # dau tien check xem co " " nao o dang truoc khong

        
        x = x.lower()
        last = len(x)-1
        first_space = 0
        for i in range( 0 , last+1) :
            if x[i] == " " :
                first_space += 1 
            else :
                break
        x = x[first_space:]

       #  check xem co " " o phia sau khong

        last = len(x) -1
        last_space = 0
        for i in range (0 , last+1):
            j = -i-1
            if x[j] == " " :
                last_space += 1 
            else :
                break
        x = x[:last-last_space+1]

        # viet hoa chu cai dau tien

        x = x.lower()
        last = len(x)-1
        viethoa = x[0].upper()
        x = viethoa + x[1:]

        # moi chu chi cach nhau 1 dau cach
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

        # moi chu deu viet hoa chu cai dau tien
        last = len(x)-1

        for i in range ( 1 ,last-1) :
            if x[i] == " " :
                viethoa = x[i+1].upper()
                x = x[:i+1] + viethoa + x[i+2:]
        
        if x[-2] == " " :
            x = x[:last] + x[-1].upper()
        
        return(x)
        

    
 


