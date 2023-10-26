from fastapi import FastAPI, Request, HTTPException
import json
from starlette import status
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
import credential_handler
import drive
import base64
import gmail
from urllib.parse import urlparse, parse_qs
import slack
from slackeventsapi import SlackEventAdapter
import os
from dotenv import load_dotenv
import datetime
import webhook
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time

load_dotenv()

# Initialize the Slack WebClient with the provided token
slack_data = slack.WebClient(token=os.environ.get("SLACK_TOKEN"))


# Create a FastAPI application instance
app = FastAPI()

credential_handler.get_creds()
gmail.gmail_watch()

def webhook_check():
    data = webhook.webhook()
    gmail.gmail_watch()
    print("Process and handle webhook data", time.ctime())

scheduler = BackgroundScheduler()

scheduler.add_job(webhook_check, CronTrigger(hour=11))
scheduler.add_job(webhook_check, CronTrigger(hour=23))

scheduler.start()

@app.get("/drive_webhook/")
async def root(request: Request):
    return {"message": "Hello World"}


@app.post("/gmail/")
async def handle_gmail(request: Request):
    try:
        payload = await request.body()
        data = json.loads(payload)
        gmail_data = data['message']['data']
        pub_id = data['message']['messageId']
        publish_time = data['message']['publish_time']
        print("gmail_data", gmail_data)
        encoded_data = gmail_data
        encoded_data = encoded_data.replace('-', '+').replace('_', '/')
        padding = b'=' * (4 - (len(encoded_data) % 4))
        encoded_data += padding.decode('utf-8')
        decoded_bytes = base64.b64decode(encoded_data)
        json_string = decoded_bytes.decode('utf-8')
        data = json.loads(json_string)
        print(json.dumps(data, indent=2))
        print("pub_id", pub_id)
        print("publish_time", publish_time)

        gmail.get_mail_details()
        return {'status': status.HTTP_200_OK}
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON data")


@app.post("/drive/")
async def handle_gmail(request: Request):
    print(request, request.headers)
    file_url = request.headers['X-Goog-Resource-Uri']
    channel_expiration = request.headers['x-goog-channel-expiration']
    resource_state = request.headers['x-goog-resource-state']
    if resource_state == 'update':
        print("URL",file_url)
        print("Channel_Expiration", channel_expiration)
        parsed_url = urlparse(file_url)
        path_parts = parsed_url.path.split("/")
        file_id = path_parts[-1]
        data = drive.search_file(file_id)
        print(data)
    return {'status': status.HTTP_200_OK}


@app.post("/slack/")
async def handle_slack(request: Request):
    try:
        request_body = await request.body()
        data = json.loads(request_body.decode('utf-8'))
        user_Id=data['event']['user']
        user_data=slack_data.users_profile_get(user=user_Id)
        Channel_Id=data['event']['channel']
        Channel = slack_data.conversations_info(channel=Channel_Id)
        print("Type:",data['type'])
        time = data['event_time']
        dt_object = datetime.datetime.fromtimestamp(time)
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        print("Date & Time:", formatted_time)
        print("channel_name:", Channel['channel']['name'])
        print("User_Profile_name:", user_data['profile']['real_name'])
        print("User_Profile_email:", user_data['profile']['email'])
        print("message_text:",data['event']['text'])
    except:
        request_body = await request.body()
        data = json.loads(request_body.decode('utf-8'))
    return {'status': status.HTTP_200_OK, 'body': data}
