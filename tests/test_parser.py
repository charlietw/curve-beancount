from parser.parser import Parser
from email_reader.email_reader import EmailReader
import os

def create_emails():
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    token_dir = os.environ['TOKEN_DIR']
    creds_dir = os.environ['CREDS_DIR']
    email_to = os.environ['EMAIL_ADDRESS']
    service = EmailReader(
        scopes,
        email_to,
        token_dir,
        creds_dir
    )
    emails = service.get_all_emails(5)
    return emails


def create_parser():
    emails = create_emails()
    return Parser(emails)


def test_parser_creation():
    parser = create_parser()
    expected = True
    actual = isinstance(parser, Parser)
    assert expected == actual


def test_list_headers():
    parser = create_parser()
    headers = parser.list_headers()
    expected = True
    actual = isinstance(headers, list)
    assert expected == actual


def test_list_headers_format():
    parser = create_parser()
    first_header = parser.list_headers()[0]
    expected = True
    actual = isinstance(first_header, str)
    assert expected == actual


def test_headers_comprehension():
    parser = create_parser()
    headers = parser.headers_comprehension()
    expected = True
    actual = isinstance(headers, list)
    assert expected == actual


def test_headers_comprehension_format():
    parser = create_parser()
    headers = parser.headers_comprehension()[0]
    expected = True
    actual = isinstance(headers, dict)
    assert expected == actual
