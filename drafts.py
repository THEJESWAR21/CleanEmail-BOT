import base64
from email.message import EmailMessage

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_draft(creds):

    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message["From"] = 'thejeswar21jeeva@gmail.com'
        message["To"] = "itsrazetitan@gmail.com"
        message["Subject"] = "Automated Draft From CleanMail BOT"
        message.set_content("YOYOYOYOYOYO YOYO OYOO OYOYO OOYOYOYO YOYOYO YOYO ")


        # Encodeding Message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"message": {"raw": encoded_message}}

        draft = (
            service.users()
            .drafts()
            .create(userId="me", body=create_message)
            .execute()
        )

        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

        
    except HttpError as Error:
        print(f"An error occurred: {Error}")
        draft = None