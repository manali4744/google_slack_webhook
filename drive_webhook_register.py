import credential_handler
from googleapiclient.discovery import build
import json
import string
import random
import os


def webhook_file(file_Id, res):
    creds = credential_handler.get_creds()
    service = build('drive', 'v3', credentials=creds)
    resource = service.files()

    body = {
    "id": res,
    "type": "web_hook",
    "address": "https://5a00-123-201-0-1.ngrok-free.app/drive/"
    }

    data = service.files().watch(fileId=file_Id, body=body).execute()

    # Store the webhook data in a JSON file
    webhook_data = {
        "file_id": file_Id,
        "webhook_info": data
    }
    
    # Save the data to a JSON file with the file_id as the filename
    with open(os.path.join("webhookdata",f"{file_Id}_webhook.json"), "w") as json_file:
        json.dump(webhook_data, json_file)

creds = credential_handler.get_creds()
service = build('drive', 'v3', credentials=creds)
resource = service.files()


result = resource.list(fields="files(id, name)").execute() 

file_list = result.get('files') 


for file in file_list: 
    file_id = file['id']
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    webhook_file(file_id, res)
