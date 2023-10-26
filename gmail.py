import credential_handler
from googleapiclient.discovery import build

def get_mail_details():
    creds = credential_handler.get_creds()
    service = build('gmail', 'v1', credentials=creds)
    result = service.users().messages().list(userId='me', maxResults=1).execute()
    messages = result.get('messages')

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute() 
        payload = txt['payload']
        headers = payload['headers']
        body = txt['snippet']

        print("gmail information")
        for data in headers: 
            if data['name'] == 'Subject': 
                subject = data['value']
            if data['name'] == 'To':
                receiver = data['value']
            if data['name'] == 'From': 
                sender = data['value'] 
        print("Subject:", subject)
        print("Body:",body)
        print("From:",sender)
        print("To:", receiver)


def gmail_watch():
    creds = credential_handler.get_creds()
    service = build('gmail', 'v1', credentials=creds)
    request = {
    "topicName": "projects/revival-login/topics/magnifio-email", 
    "labelIds": ["INBOX"],
    "labelFilterBehavior": "INCLUDE"
    }
    gmail_watch = service.users().watch(userId='me', body=request).execute() 

    return gmail_watch