import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import EmailMessage



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def gmail_importer():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("email_service/token.json"):
    
    creds = Credentials.from_authorized_user_file("email_service/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("email_service/credentials.json", SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("email_service/token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])
    
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    for message in messages:  # Получаем только первые 10 сообщений
      
      msg = service.users().messages().get(userId='me', id=message['id']).execute()
      data = msg['payload']['headers']
        
      subject = next(item['value'] for item in data if item['name'] == 'Subject')
      sender = next(item['value'] for item in data if item['name'] == 'From')
      if 'parts' in msg['payload']:
        body_data = msg['payload']['parts'][0]['body'].get('data')
      else:
        body_data = msg['payload']['body'].get('data')

      body = base64.urlsafe_b64decode(body_data).decode('utf-8')
      EmailMessage.objects.create(subject=subject, sender=sender, receiver='google.com', body=body)
      

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

