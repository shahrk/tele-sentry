#!/usr/bin/env python3
import os
import time
import asyncio
from sms import send_message
from telethon import TelegramClient
from datetime import datetime
API_ID = os.environ['TELEGRAM_API_ID']
API_HASH = os.environ['TELEGRAM_API_HASH']
CHAT_NAME = 'H1B_H4_Visa_Dropbox_slots'
PHONE_NUMBER = os.environ['PHONE_NUMBER']
CARRIER = 'att'
prev_msg = ''
SLEEP_TIME = 5 #secs
SLOT_TIMES_FILE = 'slot_times'
ALERT_THRESHOLD = 60 #mins
seen = {}

async def main():
  read = 0
  async with TelegramClient(f'+1{PHONE_NUMBER}', API_ID, API_HASH) as client:
    async for message in client.iter_messages(CHAT_NAME):
      if not message.text:
        continue
      key = str(message.id) + ": " + message.text
      if key in seen:
        return
      if "bulk" in message.text.lower():
        curr_timestamp = datetime.now()
        if 'bulk_last_seen' in seen:
          delta = curr_timestamp - seen['bulk_last_seen']
          if delta.total_seconds()/60 < ALERT_THRESHOLD:
            continue
        seen['bulk_last_seen'] = curr_timestamp
        send_message(PHONE_NUMBER, CARRIER, "BULK SLOTS")
        # add check to see last alert. If within 30 mins don't alert again
      print(message.id, message.text)
      seen[key] = True
      read += 1
      if read > 100:
        return

if __name__ == "__main__":
    import time
    while True:
      s = time.perf_counter()
      asyncio.run(main())
      elapsed = time.perf_counter() - s
      print(f"Checked messages in {elapsed:0.2f} seconds.")
      time.sleep(SLEEP_TIME)