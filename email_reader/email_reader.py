import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class EmailReader:
    def __init__(
            self,
            scopes,
            address_to,
            token_dir,
            creds_dir):
        self.scopes = scopes
        self.address_to = address_to
        self.token_dir = token_dir
        self.creds_dir = creds_dir


    def service(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_dir):
            creds = Credentials.from_authorized_user_file(self.token_dir, self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_dir, self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_dir, 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=creds)
            return service

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')


    def get_emails_to(self, emails_to_retrieve):
        query = 'to:' + self.address_to + ' subject:Curve Receipt in:inbox'
        results = self.service().users().messages().list(
            userId='me',
            maxResults=emails_to_retrieve,
            q=query
        ).execute()
        return results['messages']


    def get_email(self, message_id):
        result = self.service().users().messages().get(
            userId='me',
            id=message_id).execute()
        return result


    def get_all_emails(self, no_of_emails_to_retrieve):
        all_emails = self.get_emails_to(no_of_emails_to_retrieve)
        emails = []
        for a in all_emails:
            email = self.get_email(a['id'])
            emails.append(email)
        return emails


    def get_label_id(self, label_str):
        label_id = self.service().users().labels().get(
            userId='me',
            id=label_str
        ).execute()
        return label_id


    def get_message_labels(self, message_id):
        """
        Returns all of the labels in a message
        """
        email = self.get_email(message_id)
        labels = email['labelIds']
        return labels


    def message_has_label(self, email, label_str):
        """
        Returns true if the message has a given label
        """
        labels = self.get_message_labels(email['id'])
        has_label = False
        for label in labels:
            if label == label_str:
                has_label = True
        return has_label


    def move_email(self, message_id, label_from, label_to):
        """
        Removes one label and adds another
        """
        body = {
            "addLabelIds": [
                label_to
            ],
            "removeLabelIds": [
                label_from
            ],
        }

        self.service().users().messages().modify(
            userId='me',
            id=message_id,
            body=body,
        ).execute()
        return True




