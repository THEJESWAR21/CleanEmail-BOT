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
SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic']

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

        
    try:
        """ Call the Gmail API """

        service = build("gmail", "v1", credentials=creds)

        label_name = "IMPORTANT"
        filter_content = {
            "criteria": {"query": "PISSBABY"},
            "action": {
                "addLabelIds": [label_name],
                "removeLabelIds": ["INBOX"],
            },
        }


        result = (
            service.users()
            .settings()
            .filters()
            .create(userId="me", body=filter_content)
            .execute()
        )
        print(f'Created Filter with id: {result.get("id")}')

        # # Creates a Authorzied Gmail API Client service object using the credentails
        # service = build("gmail", "v1", credentials=creds)

        # # The result object contains a "labels" list
        # results = service.users().labels().list(userId="me").execute()

        # # Extracts a list of labels from a dictionary named results
        # labels = results.get("labels", [])

        # if not labels:
        #     print("No Labels found.")
        #     return
        # print("Labels:")
        # for label in labels:
        #     print(label)

    # Checks for Errors
    except HttpError as error:
        print(f"An error occurred: {error}")

    
if __name__ == "__main__":
    main()
        




