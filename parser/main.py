from email_reader.email_reader import EmailReader
from parser.parser import Parser
import os
import argparse

def setup():
    scopes = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify']
    token_dir = os.environ['CB_TOKEN_DIR']
    creds_dir = os.environ['CB_CREDS_DIR']
    email_to = os.environ['CB_EMAIL_ADDRESS']
    gmail = EmailReader(
        scopes,
        email_to,
        token_dir,
        creds_dir
    )
    emails = gmail.get_all_emails(10)
    parser = Parser(emails)

    return gmail, emails, parser


def main():
    gmail, emails, parser = setup()
    if emails:
        parser.add_curve_emails()
        full_output = parser.full_beancount_output()
        for e in emails:
            gmail.move_email(e['id'], "INBOX", os.environ['CB_GMAIL_LABEL'])
        print(full_output)



def list_headers():
    gmail, emails, parser = setup()
    print(parser.list_headers())


if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument(
        '-lh',
        action='store_const',
        const='list_headers',
        help='list the headers to the console'
    )
    args = cli_parser.parse_args()
    if args.lh == 'list_headers':
         list_headers()
    else:
         main()