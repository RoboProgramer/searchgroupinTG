from pyrogram import Client

from pyrogram.raw import functions
from pyrogram.errors import FloodWait
from pyrogram.types import  MessageEntity

# pyrogram.raw.functions.contacts.GetBlocked

import  time
import random

################
# first get your api id and api hash from this link https://my.telegram.org.
api_id = YOUR_API_ID
api_hash ="Your API HASH"

##########
myphonenumber = "123456789"
app = Client(myphonenumber,api_id=api_id,api_hash=api_hash)

with app:
  ME = app.get_me()
  print("ME",ME)
  MeId = ME.id

query = ['word1','word2','word3']
for iquery in range(0,len(query)):
  print(f"Checking {query[iquery]}")
  #####################
  #### Read done dialog
  with app:
    for dialog in app.iter_dialogs():
      if dialog.chat.type == 'bot':
        continue
      if dialog.chat.is_creator is None:
        continue
      chatid = dialog.chat.id
      if chatid in [MeId,]:  # you can add any user id to exculde from searching
        continue
      message_ids = []
      result = False
      try:
        for message in app.search_messages(chatid, query=query[iquery]):
          message_ids.append(message.message_id)
      except Exception as e:
        print(f"Err>>{e} in \nMSG>>{dialog}")
        continue
      ############ Now Delete the founded message
      if message_ids:
        try:
          result = app.delete_messages(chatid, message_ids)
        except FloodWait as e:
          sleeptime = e.x + random.randint(5, 60)
          print(f"Floodwait in Sendign Message Time Sleep for {sleeptime}")
          time.sleep(sleeptime)
          # try delete it again
          try:
            result = app.delete_messages(chatid, message_ids)
          except Exception as e:
            print(f"again cant delete due to {e} for chatid {chatid} in msgs {message_ids}" )
        except Exception as e:
          print(f"cant delete due to {e} for chatid {chatid} in msgs {message_ids}")
      text = f"The query {query[iquery]}  has been found in these message id:{message_ids} of user {chatid}"
  waitTime = random.randint(60, 200)
  print(f"Wait about {waitTime} to start NEXT word")

