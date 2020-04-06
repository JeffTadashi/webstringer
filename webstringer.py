#!/usr/bin/env python3

# TODO: program in return address, change default to something not jefftadashi.com related
# TODO: Change jam script to docker format

import requests
import json
import sendgrid
import time
import datetime
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True, help="URL of the site to monitor")
parser.add_argument("-m", "--match",  help="String of text to match")
parser.add_argument("-n", "--nomatch",  help="String of text to NOT match")
parser.add_argument("-a", "--api",  required=True, help="File location of API key. Should be a single line text file with the key in first line.")
parser.add_argument("-e", "--email",  action='append', required=True, help="Email address to send alert to. Repeat argument for multiple email addresses")
# parser.add_argument("-f", "--from-email",  action='append', help="Email address to send from. Default is website-checker@jefftadashi.com")

args = parser.parse_args()

# Exit, if user did not specify match or nomatch
if args.match is None and args.nomatch is None:
    print("Please specify a match or nomatch option. See -h or --help for details")
    sys.exit(1)

# Default headers taken from MacOS Catalina, Firefox
headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'DNT': '1',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'Cache-Control': 'max-age=0',
'TE': 'Trailers'
}

# Get API key from file
try:
    with open(args.api) as file:
        read_api_key = file.readline().strip()
except IOError:
    print("API Key file not accessible! Please be sure we have permissions to read it, and it's spelled correctly.")
    sys.exit(1)


# Create email address list in proper format (single-entry dictionaries inside a list)
final_email_list=[]
for x in args.email: 
    final_email_list.append({"email":x})



# Send initial test/starting email
print ("Sending initial test/notice email...")
sg = sendgrid.SendGridAPIClient(api_key=read_api_key)
init_data = {
"personalizations": [
    {
   "to": final_email_list,
   "subject": "JeffTadashi/Webstringer: Begin monitoring notice"
    }
],
"from": {
    "email": "website-checker@jefftadashi.com"
},
"content": [
    {
    "type": "text/plain",
    "value": "Hello! This is a notice message to make sure your email is working, and to let you know that monitoring has begun on the following URL: " + args.url
    }
]
}
response = sg.client.mail.send.post(request_body=init_data)



while True:
    print ("Attemping connection again...at " + str(datetime.datetime.now()))

    # Do the actual web request!
    r = requests.get(args.url, headers=headers)
    #print(r.text)

    match = False
    nomatch = False

    # Perform logic if the match or nomatch strings were defined, and if they did/didn't exist in the web request
    if args.match is None:
        match = True 
    elif args.match in r.text:
        match = True 

    if args.nomatch is None:
        nomatch = True 
    elif args.nomatch not in r.text:
        nomatch = True 



    if match == True and nomatch == True:
        print("Trigger is fully matched!! Sending email, then waiting 2 hours until next check.")

        # TEMP TESTING/DEBUG ONLY
        #print("temp exit")
        #sys.exit(0)



        # from https://github.com/sendgrid/sendgrid-python
        sg = sendgrid.SendGridAPIClient(api_key=read_api_key)
        data = {
        "personalizations": [
            {
           "to": final_email_list,
            "subject": "JeffTadashi/Webstringer: MATCH FOUND!!!"
            }
        ],
        "from": {
            "email": "website-checker@jefftadashi.com"
        },
        "content": [
            {
            "type": "text/plain",
            "value": "Your requested website monitoring got a match! See URL here: " + args.url
            }
        ]
        }
        response = sg.client.mail.send.post(request_body=data)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)

        # Delay for 2 hours, then check again.
        time.sleep(7200)
        #sys.exit(0)

    # repeat this loop every 60 seconds
    time.sleep(60)

