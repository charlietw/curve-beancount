from email_reader.email_reader import EmailReader
import os


def create_email_reader():
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
    return service


def test_email_reader_creation():
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    gmail = create_email_reader()
    expected = scopes
    actual = gmail.scopes
    assert expected == actual


def test_email_service():
    gmail = create_email_reader()
    expected = True
    actual = isinstance(gmail, EmailReader)
    assert expected == actual


def test_email_retrieve():
    gmail = create_email_reader()
    messages = gmail.get_emails_to(5)
    expected = 5
    actual = len(messages)
    assert expected == actual


def test_get_email_raw():
    gmail = create_email_reader()
    messages = gmail.get_emails_to(1)
    for m in messages:
        gmail.get_email(m['id'])
    expected = True
    actual = isinstance(gmail, EmailReader)
    assert expected == actual


def test_get_all_emails():
    gmail = create_email_reader()
    messages = gmail.get_all_emails(5)
    expected = 5
    actual = len(messages)
    assert expected == actual
