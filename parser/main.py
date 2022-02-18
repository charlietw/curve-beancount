from email_reader.email_reader import EmailReader
from parser.parser import Parser
import os

def main():
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    token_dir = os.environ['TOKEN_DIR']
    creds_dir = os.environ['CREDS_DIR']
    email_to = os.environ['EMAIL_ADDRESS']
    gmail = EmailReader(
        scopes,
        email_to,
        token_dir,
        creds_dir
    )
    emails = gmail.get_all_emails(1)
    parser = Parser(emails)
    parser.get_headers()


if __name__ == '__main__':
    main()