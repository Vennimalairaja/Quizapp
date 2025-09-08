import os
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Step 1: Define the Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Step 2: Authorize and build service
def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

# Step 3: Compose and send email
def send_email(receiver,Subject,content):
    service = get_gmail_service()

    msg = EmailMessage()
    msg.set_content(content)
    msg['To'] = receiver           # <-- Change this to your test recipient
    msg['From'] = 'productracker@gmail.com'          # <-- Change this to your Gmail
    msg['Subject'] = Subject

    # Encode the message
    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    body = {'raw': raw_message}

    # Send the email
    message = service.users().messages().send(userId='me', body=body).execute()
    print(f'Message sent! Message ID: {message["id"]}')

