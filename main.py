# Make it easier to refer to file paths without worrying about platform specific notations
import os.path

# Used when refreshing expired authentication Tokens
from google.auth.transport.requests import Request

# To Store login / Authentication Data
from google.oauth2.credentials import Credentials

# Flows typically opens the system browser and directs the user to Google's Authorization for authentication
from google_auth_oauthlib.flow import InstalledAppFlow


# Used to create a connection to a Google APi Service
from googleapiclient.discovery import build

# To handle API request failures
from googleapiclient.errors import HttpError

# Choosing a Scope
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# readonly - View your Emails and Messages

def main():
    """ Creating the Token File for authoriziation to user the Gmail API"""

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # if there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentails for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    
    body2 = {
        "removeLabelIds": ['INBOX'],
        "addLabelIds": ['Label_906954676064142011']
    }

        
    try:
        """ Call the Gmail API """

        service = build("gmail", "v1", credentials=creds)
        results = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX"])  
            .execute()
        )
        messages = results.get("messages", [])

        if not messages:
            print("No Messages Found.")
            return
        
        print("Messages: ")

        for message in messages:
            print(f"message ID: {message["id"]}")
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=message["id"])
                .execute()
            )

            email_data = msg["payload"]["headers"]
            for values in email_data:

                name = values["name"]
                if name == "From":
                    email =  values["value"]

                    if email == "Neon Blue <itsrazetitan@gmail.com>":
                        updated = (
                            service.users()
                            .messages()
                            .modify(
                                userId = "me",
                                id = msg["id"],
                                body = body2
                            )
                            .execute()
                        )
                        print("MODIFIED SUCESSFULLY")

            # if msg["snippet"] == "BIG BIG BALLS":
            #     result = (
            #         service.users()
            #         .messages()
            #         .modify(
            #             userId = "me",
            #             id = msg["id"],
            #             body = body2
            #         )
            #         .execute()
            #     )
            #     print("MODIFYED SUCCESFULLY")



    # Checks for Errors
    except HttpError as error:
        print(f"An error occurred: {error}")

    
if __name__ == "__main__":
    main()
        




