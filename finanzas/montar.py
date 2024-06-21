from __future__ import print_function
import os.path
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_file_to_drive(file_path, file_id):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Actualizar el archivo en Google Drive
    media = MediaIoBaseUpload(file_path, mimetype='text/plain', resumable=True)
    request = service.files().update(fileId=file_id, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}% of {file_path}")

    print(f"File {file_path} uploaded successfully.")

def main():
    # IDs de los archivos en Google Drive que quieres sobrescribir
    file_ids = [
        ('1WDh31MrQHaqWlTF9sgebFL3aDMkyDQMa', 'finanzas.txt'),
        ('1JuhWQY25dMK78YqbzU0MuYhyMCRPS7DS', 'historial.txt')
    ]

    for file_id, file_path in file_ids:
        upload_file_to_drive(file_path, file_id)

    print("All files uploaded successfully.")

if __name__ == '__main__':
    main()

