import io
import os
import credential_handler
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


def search_file(file_Id):
    creds = credential_handler.get_creds()
    service = build('drive', 'v3', credentials=creds)
    file_info = service.files().get(fileId=file_Id, fields='id, name').execute()
    print(file_info)
    request = service.files().get_media(fileId=file_Id)
    try:
        print(request)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        print(downloader)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(status)
            print('Download progress {0}'.format(status.progress()*100))
        fh.seek(0)
        with open(os.path.join('drive_download', file_info['name']), 'wb') as f:
            f.write(fh.read())
            f.close()
        return "downloaded successfully"
    except:
        return "download failed"



