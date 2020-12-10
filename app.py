from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.patched import MessageService
from telethon import errors
import datetime
import asyncio
import time

# lrivate1: -1001157812346
# lrivate2: -1001368465447

######################
source_id = -1001157812346
dest_id = -1001368465447
pairs = [
  {

  }
]
sleep_time = 0.4
year = 2020
month = 11
day = 14
######################

client_name = 'dude-cv'
API_ID = 1945628
API_HASH = '2c96a07930fe107684ab108250886d49'

client = TelegramClient(client_name, API_ID, API_HASH)

client.start()

def sendAllMessages(first_id, last_id):
  num = first_id
  
  while num <= last_id:
    try:
      message = client.get_messages(source_id, ids=[num])
      if type(message[0]) == MessageService:
        num += 1
        continue
      if not message[0]:
        print(f'message {num} has been deleted in source channel')
        num += 1
        continue
      sendMessage(message[0])

      num += 1
      time.sleep(sleep_time)
    except Exception as e:
      print(e)
      pass

  print('++++++++++++++++++++++++++')
  print('+                        +')
  print('+    all process Done    +')
  print('+                        +')
  print('++++++++++++++++++++++++++')

def sendMessage(message):
  print(f'sent message {message.id}')
  
  client.send_message(dest_id, message)

if year == 0:
  msgs = client.get_messages(source_id)

  last_message_id = msgs[0].id
  sendAllMessages(1, last_message_id)
else:
  date = datetime.datetime(year, month, day)
  allMessages = client.get_messages(source_id)
  last_message_id = allMessages[0].id
  
  messagesOfDate = client.get_messages(source_id, offset_date=date)
  first_message_id = messagesOfDate[0].id + 1

  sendAllMessages(first_message_id, last_message_id)