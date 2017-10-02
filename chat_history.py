class chat_history:

 database = {} #database (dict)
 def chat_history(chat_id):
  return database[chat_id]
 def lastest_message(chat_id):
  return database[chat_id][len(chat_history)-1]
 def write_data(chat_id, message):
  database = database[chat_id] + [message]

