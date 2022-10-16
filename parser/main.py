from email_reader.email_reader import EmailReader
from parser.parser import Parser
import os
import argparse

def setup(email_to):
    scopes = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify']
    token_dir = os.environ['CB_TOKEN_DIR']
    creds_dir = os.environ['CB_CREDS_DIR']
    gmail = EmailReader(
        scopes,
        email_to,
        token_dir,
        creds_dir
    )
    emails = gmail.get_all_emails(1000)
    parser = Parser(emails, 'categories.json')

    return gmail, emails, parser


def main(email_to):
    gmail, emails, parser = setup(email_to)
    if emails:
        parser.add_curve_emails()
        full_output = parser.full_beancount_output()
        for e in emails:
            gmail.move_email(e['id'], "INBOX", os.environ['CB_GMAIL_LABEL'])
        print(full_output)



def list_headers(email_to):
    gmail, emails, parser = setup(email_to)
    print(parser.list_headers())


if __name__ == '__main__':
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument(
        '-lh',
        action='store_const',
        const='list_headers',
        help='list the headers to the console'
    )
    cli_parser.add_argument(
        '--email',
        help='the email address to read from'
    )
    args = cli_parser.parse_args()
    if args.lh == 'list_headers':
         list_headers(args.email)
    else:
         main(args.email)
