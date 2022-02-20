from parser.parser import Parser
from email_reader.email_reader import EmailReader
import os
import datetime
import pytest
from decimal import Decimal


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
    expected = os.environ['EMAIL_ADDRESS']
    actual = headers['Delivered-To']
    assert expected == actual


def test_curve_emails():
    parser = create_parser()
    expected = 0
    actual = len(parser.curve_emails)
    assert expected == actual


def test_add_curve_emails():
    parser = create_parser()
    parser.add_curve_emails()
    expected = 5
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



def test_parse_cost():
    parser = create_parser()
    email = parser.emails[0]
    parsed_response = parser.parse_cost(email)
    expected = True
    actual = isinstance(parsed_response, Decimal)
    assert expected == actual


def test_parse_cost_multiple_matches_raises_error():
    parser = create_parser()
    email = parser.emails[0]
    with pytest.raises(ValueError):
        parser.parse_cost(email, "for £ for £")


def test_parse_cost_no_matches_raises_error():
    parser = create_parser()
    email = parser.emails[0]
    with pytest.raises(ValueError):
        parser.parse_cost(email, "test string")






