from parser.parser import Parser
from email_reader.email_reader import EmailReader
import os
import datetime
import pytest
from decimal import Decimal


def create_emails():
    scopes = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify']
    token_dir = os.environ['CB_TOKEN_DIR']
    creds_dir = os.environ['CB_CREDS_DIR']
    email_to = os.environ['CB_TEST_EMAIL_ADDRESS']
    service = EmailReader(
        scopes,
        email_to,
        token_dir,
        creds_dir
    )
    emails = service.get_all_emails(2)
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


def test_headers_comprehension_format():
    parser = create_parser()
    email = parser.emails[0]
    headers = parser.headers_comprehension(email)
    expected = True
    actual = isinstance(headers, dict)
    assert expected == actual


def test_headers_comprehension_value():
    parser = create_parser()
    email = parser.emails[0]
    headers = parser.headers_comprehension(email)
    expected = os.environ['CB_TEST_EMAIL_ADDRESS']
    actual = headers['To']
    assert expected == actual


def test_curve_emails():
    parser = create_parser()
    expected = 0
    actual = len(parser.curve_emails)
    assert expected == actual


def test_add_curve_emails():
    parser = create_parser()
    parser.add_curve_emails()
    expected = 2
    actual = len(parser.curve_emails)
    assert expected == actual


def test_parse_datetime():
    parser = create_parser()
    email = parser.emails[0]
    parsed_response = parser.parse_datetime(email)
    expected = True
    actual = isinstance(parsed_response, datetime.datetime)
    assert expected == actual


def test_parse_datetime_wrong_format():
    parser = create_parser()
    email = parser.emails[0]
    with pytest.raises(ValueError):
        parser.parse_datetime(email, "wrong_format")


def test_parse_subject():
    parser = create_parser()
    email = parser.emails[0]
    email_subject = parser.headers_comprehension(email)['Subject']
    pattern = "for £"
    parsed_response = parser.parse_subject(email_subject, pattern)
    expected = True
    actual = isinstance(parsed_response, str)
    assert expected == actual


def test_parse_cost():
    parser = create_parser()
    email = parser.emails[0]
    email_subject = parser.headers_comprehension(email)['Subject']
    parsed_response = parser.parse_cost(email_subject)
    expected = True
    actual = isinstance(parsed_response, Decimal)
    assert expected == actual


def test_parse_payee():
    parser = create_parser()
    email_subject = "Curve Receipt: Purchase at Some Test Place on date for price"
    parsed_response = parser.parse_payee(email_subject)
    expected = "Some Test Place"
    actual = parsed_response
    assert expected == actual


def test_parse_payee_multiple_matches():
    parser = create_parser()
    email_subject = "Curve Receipt: Purchase at Restaurant on Place on Sea on date for price"
    parsed_response = parser.parse_payee(email_subject)
    expected = "Restaurant on Place on Sea"
    actual = parsed_response
    assert expected == actual


def test_parse_cost_multiple_matches_raises_error():
    parser = create_parser()
    email_subject = "for £ for £"
    pattern = "for £"
    with pytest.raises(ValueError):
        parser.parse_subject(email_subject, pattern)


def test_parse_cost_no_matches_raises_error():
    parser = create_parser()
    email_subject = "test string"
    pattern = "for £"
    with pytest.raises(ValueError):
        parser.parse_subject(email_subject, pattern)


def test_convert_beancount():
    parser = create_parser()
    parser.add_curve_emails()
    email = parser.curve_emails[0]
    parser.convert_beancount(email)

def test_convert_beancount_full():
    parser = create_parser()
    parser.add_curve_emails()
    parser.full_beancount_output()







