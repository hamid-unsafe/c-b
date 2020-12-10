from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.patched import MessageService
from telethon import errors
from telethon.tl.types import MessageMediaPhoto
import datetime
import asyncio
import time
import sys
import os

image = 'image'
audio = 'audio'
document = 'document'
text = 'text'
video = 'video'

######################
# image | audio | video | document | text
######################
pairs = [
  {
    'source_id': -1001157812346,
    'dest_id': -1001439191924,
    'year': 2020,
    'month': 11, 
    'day': 15,
    'message_types': [],
  },
  {
    'source_id': -1001180639527,
    'dest_id': -1001155977872,
    'year': 0,
    'month': 0, 
    'day': 0,
    'message_types': [],
  },
]
sleep_time = 0.4
year = 0
month = 11
day = 14
######################

client_name = 'dude-cv'
API_ID = 1945628
API_HASH = '2c96a07930fe107684ab108250886d49'

client = TelegramClient(client_name, API_ID, API_HASH)

client.start()

def getMediaType(media):
  # list of types : image | audio | video | document | unknown
  
  MT = 'unknown'
  if type(media) == MessageMediaPhoto:
    MT = 'image'
  elif media.document.mime_type.startswith('image'):
    MT = 'image'
  elif media.document.mime_type.startswith('video'):
    MT = 'video'
  elif media.document.mime_type.startswith('audio'):
    MT = 'audio'
  elif media.document.mime_type.startswith('application'):
    MT = 'document'
  elif media.document.mime_type.startswith('text'):
    MT = 'document'

  return MT

def sendAllMessages(first_id, last_id, message_types, dest_id, source_id):
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
      message = message[0]
      if message_types:
        if message.media:
          messageMediaType = getMediaType(message.media)

          if messageMediaType in message_types:
            sendMessage(dest_id, message)
        elif 'text' in message_types:
          sendMessage(dest_id, message)
      else:
        sendMessage(dest_id, message)

      num += 1
      time.sleep(sleep_time)
    except Exception as e:
      print(e)
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      break

  print('++++++++++++++++++++++++++')
  print('+                        +')
  print('+    One channel Done    +')
  print('+                        +')
  print('++++++++++++++++++++++++++')

def sendMessage(dest_id, message):
  print(f'sent message {message.id}')
  
  client.forward_messages(dest_id, message)

def sendOnePair(source_id, dest_id, year, month, day, message_types):
  if year == 0:
    msgs = client.get_messages(source_id)

    last_message_id = msgs[0].id
    sendAllMessages(1, last_message_id, message_types, dest_id, source_id)
  else:
    date = datetime.datetime(year, month, day)
    allMessages = client.get_messages(source_id)
    last_message_id = allMessages[0].id
    
    messagesOfDate = client.get_messages(source_id, offset_date=date)
    first_message_id = messagesOfDate[0].id + 1

    sendAllMessages(first_message_id, last_message_id, message_types, dest_id, source_id)

def init():
  for p in pairs:
    sendOnePair(p['source_id'], p['dest_id'], p['year'], p['month'], p['day'], p['message_types'])

  print('++++++++++++++++++++++++++')
  print('+                        +')
  print('+    all process Done    +')
  print('+                        +')
  print('++++++++++++++++++++++++++')

init()