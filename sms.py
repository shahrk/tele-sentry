#!/usr/bin/env python3
import yagmail
import sys
import os

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtex.com",
    "sprint": "@page.nextel.com"
}
 
USER = os.environ['GMAIL_ID']
APP_PASSWORD = os.environ['GMAIL_APP_PASSWORD']
 
def send_message(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = (USER, APP_PASSWORD)
    
    with yagmail.SMTP(auth[0], auth[1]) as yag:
      yag.send(recipient, message)
      print('Sent email successfully')
 
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: python3 {sys.argv[0]} <PHONE_NUMBER> <CARRIER> <MESSAGE>")
        sys.exit(0)
 
    phone_number = sys.argv[1]
    carrier = sys.argv[2]
    message = sys.argv[3]
 
    send_message(phone_number, carrier, message)