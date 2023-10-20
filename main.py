from fastapi import FastAPI, Request, HTTPException
import json
from starlette import status
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
import requests
import credential_handler
import drive
from starlette import status
import base64
import json
import gmail
from urllib.parse import urlparse, parse_qs



app = FastAPI()


credential_handler.get_creds()


@app.get("/")
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