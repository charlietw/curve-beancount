from .email_reader import EmailReader
import os

def main():
    # If modifying these scopes, delete the file token.json.
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


if __name__ == '__main__':
    main()