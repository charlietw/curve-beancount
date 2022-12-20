from .email_reader import EmailReader
import os


def main():
    # If modifying these scopes, delete the file token.json.
    scopes = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
    ]
    token_dir = os.environ["CB_TOKEN_DIR"]
    creds_dir = os.environ["CB_CREDS_DIR"]
    email_to = os.environ["CB_EMAIL_ADDRESS"]
    gmail = EmailReader(scopes, email_to, token_dir, creds_dir)


if __name__ == "__main__":
    main()
