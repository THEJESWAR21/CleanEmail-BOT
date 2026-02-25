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


        # Encoding Message For the API
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"message": {"raw": encoded_message}}

        draft = (
            service.users()
            .drafts()
            .create(userId="me", body=create_message)
            .execute()
        )

        # What Gmail API expects for Draft

        # {
        #     "Message": {
        #         "raw": "BASE64_ENCODED_EMAIL"
        #     }
        # }

        send = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": encoded_message})
            .execute()
        )

        # What Gmail API expects for Send

        # {
        #    "raw": "BASE64_ENCODED_EMAIL"
        # }


        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        print(f"Message Id: {send["id"]}")
        
    # Checking For Errors
    except HttpError as Error:
        print(f"An error occurred: {Error}")
        draft = None



