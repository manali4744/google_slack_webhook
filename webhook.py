import credential_handler
from googleapiclient.discovery import build
import os
import json
from datetime import datetime
import time
import string
import random


# Calculate the expiration time to be one day (24 hours) from the current time
current_time = int(time.time())
one_day = 24 * 60 * 60  # 24 hours in seconds
expiration_time_webhook = current_time + one_day


current_time = int(time.time())
dt_object = datetime.fromtimestamp(current_time)
readable_time_current = dt_object.strftime('%Y-%m-%d %H:%M:%S')


def webhook():
    creds = credential_handler.get_creds()
    service = build('drive', 'v3', credentials=creds)
    resource = service.files()
    result = resource.list(fields="files(id, name)").execute()
    file_list = result.get('files')
    for file in file_list:
        file_id =  file['id']
        file_path = f'webhookdata/{file_id}_webhook.json'
        print(file_path)

        if os.path.exists(file_path):
            print(f"The file '{file_path}' exists.")
            with open(file_path, "r") as file:
                data = json.load(file)
                expiration_time = int(data['webhook_info']['expiration'])
                unix_timestamp = expiration_time / 1000
                dt_object = datetime.fromtimestamp(unix_timestamp)
                readable_time_expiration = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                print(readable_time_expiration)
                if current_time > unix_timestamp:
                    print(f"current_time: {current_time}, expiration: {expiration_time}, expired ")
                    body = {
                        "id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)),
                        "type": "web_hook",
                        "address": "https://2d51-203-109-79-250.ngrok-free.app/drive/",
                        "expiration":expiration_time_webhook*1000,
                    }
                    data = service.files().watch(fileId=file_id, body=body).execute()
                     # Store the webhook data in a JSON file
                    webhook_data = {
                        "file_id": file_id,
                        "webhook_info": data
                    }
                    # Save the data to a JSON file with the file_id as the filename
                    with open(os.path.join("webhookdata",f"{file_id}_webhook.json"), "w") as json_file:
                        json.dump(webhook_data, json_file)
        else:
            body = {
                "id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)),
                "type": "web_hook",
                "address": "https://2d51-203-109-79-250.ngrok-free.app/drive/"
            }
            data = service.files().watch(fileId=file_id, body=body).execute()
            # Store the webhook data in a JSON file
            print(data)
            webhook_data = {
                "file_id": file_id,
                "webhook_info": data
            }
            # Save the data to a JSON file with the file_id as the filename
            with open(os.path.join("webhookdata",f"{file_id}_webhook.json"), "w") as json_file:
                json.dump(webhook_data, json_file)
    print("here")
    return "info"