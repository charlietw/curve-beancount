from email_reader.email_reader import EmailReader
import os


def create_email_reader():
    scopes = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify']
    token_dir = os.environ['CB_TOKEN_DIR']
    creds_dir = os.environ['CB_CREDS_DIR']
    email_to = os.environ['CB_EMAIL_ADDRESS']
    service = EmailReader(
        scopes,
        email_to,
        token_dir,
        creds_dir
    )
    return service


def test_email_reader_creation():
    scopes = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify']
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
    messages = gmail.get_emails_to(2)
    expected = 2
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
    messages = gmail.get_all_emails(2)
    expected = 2
    actual = len(messages)
    assert expected == actual


def test_get_inbox_label_id():
    gmail = create_email_reader()
    label_str = "INBOX"
    label = gmail.get_label_id(label_str)
    expected = label_str
    actual = label['id']
    assert expected == actual


def test_get_filed_label_id():
    gmail = create_email_reader()
    label_str = os.environ['CB_GMAIL_LABEL']
    label = gmail.get_label_id(label_str)
    expected = label_str
    actual = label['id']
    assert expected == actual


def test_get_message_labels():
    gmail = create_email_reader()
    email = gmail.get_all_emails(1)[0]
    expected_label = "INBOX"
    labels = gmail.get_message_labels(email['id'])
    expected = True
    actual = False
    for label in labels:
        if label == expected_label:
            actual = True
    assert expected == actual


def test_has_label():
    gmail = create_email_reader()
    email = gmail.get_all_emails(1)[0]
    expected_label = "INBOX"
    expected = True
    actual = gmail.message_has_label(email, expected_label)
    assert expected == actual


def test_has_label_false():
    gmail = create_email_reader()
    email = gmail.get_all_emails(1)[0]
    expected_label = "fake_label"
    expected = False
    actual = gmail.message_has_label(email, expected_label)
    assert expected == actual


def test_move_email():
    gmail = create_email_reader()
    email = gmail.get_all_emails(1)[0]
    email_id = email['id']
    label_from = "INBOX"
    label_to = os.environ['CB_GMAIL_LABEL']
    gmail.move_email(email_id, label_from, label_to)
    assert gmail.message_has_label(email, label_from) == False
    assert gmail.message_has_label(email, label_to) == True
    gmail.move_email(email_id, label_to, label_from)
    assert gmail.message_has_label(email, label_from) == True
    assert gmail.message_has_label(email, label_to) == False






