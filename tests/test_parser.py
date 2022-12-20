from parser.parser import Parser
from email_reader.email_reader import EmailReader
import os
import datetime
import pytest
from decimal import Decimal


def get_all_emails():
    scopes = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
    ]
    token_dir = os.environ["CB_TOKEN_DIR"]
    creds_dir = os.environ["CB_CREDS_DIR"]
    email_to = os.environ["CB_TEST_EMAIL_ADDRESS"]
    service = EmailReader(scopes, email_to, token_dir, creds_dir)
    return service.get_all_emails(3)


@pytest.fixture
def parser():
    emails = get_all_emails()
    return Parser(emails, "test_categories.json")


def test_parser_creation_no_categories():
    """
    Asserts that it is possible to create an instance of Parser
    without a categories file
    """
    emails = get_all_emails()
    return Parser(emails)


def test_parser_creation(parser):
    expected = True
    actual = isinstance(parser, Parser)
    assert expected == actual


def test_list_headers(parser):
    headers = parser.list_headers()
    expected = True
    actual = isinstance(headers, list)
    assert expected == actual


def test_list_headers_format(parser):
    first_header = parser.list_headers()[0]
    expected = True
    actual = isinstance(first_header, str)
    assert expected == actual


def test_headers_comprehension_format(parser):
    email = parser.emails[0]
    headers = parser.headers_comprehension(email)
    expected = True
    actual = isinstance(headers, dict)
    assert expected == actual


def test_headers_comprehension_value(parser):
    email = parser.emails[0]
    headers = parser.headers_comprehension(email)
    expected = os.environ["CB_TEST_EMAIL_ADDRESS"]
    actual = headers["To"]
    assert expected == actual


def test_curve_emails(parser):
    expected = 0
    actual = len(parser.curve_emails)
    assert expected == actual


def test_add_curve_emails(parser):
    parser.add_curve_emails()
    expected = 3
    actual = len(parser.curve_emails)
    assert expected == actual


def test_parse_datetime(parser):

    email = parser.emails[0]
    parsed_response = parser.parse_datetime(email)
    expected = True
    actual = isinstance(parsed_response, datetime.datetime)
    assert expected == actual


def test_parse_datetime_wrong_format(parser):
    email = parser.emails[0]
    with pytest.raises(ValueError):
        parser.parse_datetime(email, "wrong_format")


def test_parse_subject(parser):
    email = parser.emails[0]
    email_subject = parser.headers_comprehension(email)["Subject"]
    pattern = "for £"
    parsed_response = parser.parse_subject(email_subject, pattern)
    expected = True
    actual = isinstance(parsed_response, str)
    assert expected == actual


def test_parse_cost(parser):
    email = parser.emails[0]
    email_subject = parser.headers_comprehension(email)["Subject"]
    parsed_response = parser.parse_cost(email_subject)
    expected = True
    actual = isinstance(parsed_response, Decimal)
    assert expected == actual


def test_parse_is_refund_true(parser):
    """
    Test 'is_refund' method when the subject is a genuine refund
    """
    email_subject = "Curve Receipt: Refund from Some Test Place on date for price"
    parsed_response = parser.is_refund(email_subject)
    expected = True
    actual = parsed_response
    assert expected == actual


def test_parse_is_refund_false(parser):
    """
    Test 'is_refund' method when the subject is not a refund
    """
    email_subject = "Curve Receipt: Purchase at Some Test Place on date for price"
    parsed_response = parser.is_refund(email_subject)
    expected = False
    actual = parsed_response
    assert expected == actual


def test_parse_payee(parser):
    email_subject = "Curve Receipt: Purchase at Some Test Place on date for price"
    parsed_response = parser.parse_payee(email_subject)
    expected = "Some Test Place"
    actual = parsed_response
    assert expected == actual


def test_parse_payee_multiple_matches(parser):
    email_subject = (
        "Curve Receipt: Purchase at Restaurant on Place on Sea on date for price"
    )
    parsed_response = parser.parse_payee(email_subject)
    expected = "Restaurant on Place on Sea"
    actual = parsed_response
    assert expected == actual


def test_parse_cost_multiple_matches_raises_error(parser):
    email_subject = "for £ for £"
    pattern = "for £"
    with pytest.raises(ValueError):
        parser.parse_subject(email_subject, pattern)


def test_parse_cost_no_matches_raises_error(parser):
    email_subject = "test string"
    pattern = "for £"
    with pytest.raises(ValueError):
        parser.parse_subject(email_subject, pattern)


def test_convert_beancount(parser):
    parser.add_curve_emails()
    email = parser.curve_emails[1]
    txn_date = datetime.datetime.strftime(email.datetime, "%Y-%m-%d")
    output_string = ""
    output_string += txn_date
    output_string += " ! "
    output_string += '"' + "OTHER TEST VENDOR" + '"'
    output_string += ' ""'
    output_string += "\n"
    output_string += " " * 2
    output_string += os.environ["CB_BEANCOUNT_ACCOUNT"]
    output_string += " -" + str(email.cost) + " GBP"
    output_string += "\n"
    output_string += " " * 2
    output_string += os.environ["CB_BEANCOUNT_EXPENSE_ACCOUNT"]
    output_string += "\n" * 2
    actual = parser.convert_beancount(email)
    assert output_string == actual


def test_convert_beancount_full(parser):
    parser.add_curve_emails()
    parser.full_beancount_output()


def test_find_category_when_present(parser):
    """
    Asserts that the find category function works as expected
    when the category is present
    """
    parser.add_curve_emails()
    email = parser.curve_emails[2]  # This email is TEST VENDOR
    expected = "Expenses:Something:TestVendor"
    actual = parser.parse_category(email)
    assert expected == actual


def test_find_category_when_not_present(parser):
    """
    Asserts that the find category function works as expected
    when the category is not present
    """
    parser.add_curve_emails()
    email = parser.curve_emails[0]  # First email is TSGN
    expected = os.environ["CB_BEANCOUNT_EXPENSE_ACCOUNT"]
    actual = parser.parse_category(email)
    assert expected == actual
