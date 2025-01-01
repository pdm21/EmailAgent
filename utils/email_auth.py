import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.settings.basic'
]

def authenticate_gmail():
    """Authenticate with Gmail API and return a service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Return the Gmail API service object
    return build('gmail', 'v1', credentials=creds)

def list_gmail_labels(service):
    """Fetch and print Gmail labels to test the connection."""
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        if not labels:
            print("No labels found.")
        else:
            print("Labels:")
            for label in labels:
                print(f"- {label['name']}")
    except Exception as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    # Authenticate and get the Gmail API service
    try:
        service = authenticate_gmail()
    except Exception as e:
        print("There was an error in the Gmail authentication process. More info: ", e)
    

