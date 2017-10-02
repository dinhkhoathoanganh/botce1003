class chat_history:

 database = {} #database (dict)
 #return all chat
 def show_chat(chat_id):
  return chat_history.database[chat_id]
 #return lastest message
 def lastest_message(chat_id):
  return chat_history.show_chat(chat_id)[len(chat_history.show_chat(chat_id))-2]
 #return lastest message 2 (the message before the lastest message)
 def lastest_message2(chat_id):
  return chat_history.show_chat(chat_id)[len(chat_history.show_chat(chat_id))-3]
 #return lastest message 3 (the message before the lastest message2)
 def lastest_message3(chat_id):
  return chat_history.show_chat(chat_id)[len(chat_history.show_chat(chat_id))-4]
 #write message to database
 def write_data(chat_id, message):
  if chat_id in chat_history.database:
   chat_history.database[chat_id] = chat_history.database[chat_id] + [message]
  else:
   chat_history.database[chat_id] = ['0',message]

#SAMPLE
chat_history.write_data('123456789','hihi')
chat_history.write_data('123456789','hihihi')
print(chat_history.show_chat('123456789'))
print(chat_history.lastest_message('123456789'))
