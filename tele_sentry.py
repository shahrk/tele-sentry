#!/usr/bin/env python3
import time
import os
from sms import send_message
from telethon import TelegramClient, types, sync
API_ID = os.environ['TELEGRAM_API_ID']
API_HASH = os.environ['TELEGRAM_API_HASH']
CHAT_NAME = 'H1B_H4_Visa_Dropbox_slots'
PHONE_NUMBER = os.environ['PHONE_NUMBER']
CARRIER = 'att'
prev_msg = ''
SLEEP_TIME = 3600 # 1 hr
SLOT_TIMES_FILE = 'slot_times'

def update_slot_times(slots):
  with open(SLOT_TIMES_FILE, 'w') as writer:
    writer.write(slots)
    print("Successfully udpated slot times")

try:
  while True:
    with TelegramClient(f'+1{PHONE_NUMBER}', API_ID, API_HASH) as client:
      message = client.get_messages(CHAT_NAME, ids=types.InputMessagePinned())
    if message.message == prev_msg:
      print("no change in slot times!")
      time.sleep(SLEEP_TIME)
    elif 'Pacific Time zone' in message.message:
      slot_times = message.message.split('Pacific Time zone (PT) - ', 1)[1].split('\n',1)[0]
      # send_message(PHONE_NUMBER, CARRIER, slot_times)
      update_slot_times(slot_times)
      prev_msg = message.message
      time.sleep(SLEEP_TIME)
    else:
      print("unexpected message found")
      print(message.message)
except Exception as e:
  print("tele-sentry exited unexpectedly. Sending alert.")
  send_message(PHONE_NUMBER, CARRIER, "tele-sentry exited unexpectedly: " + str(e))