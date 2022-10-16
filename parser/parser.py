import email
import base64
from datetime import datetime
import re
from decimal import Decimal
import os


class CurveEmail:
    def __init__(self, email_id, _datetime, cost, payee):
        self.email_id = email_id
        self.datetime = _datetime
        self.cost = cost
        self.payee = payee



class Parser:
    def __init__(self, emails: list, categories: dict, curve_emails = []):
        self.emails = emails
        self.categories = categories
        self.curve_emails = curve_emails

    def get_headers(self, _email):
        print(_email)
        headers = _email['payload']['headers']
        return headers

    def list_headers(self):
        headers = self.get_headers(self.emails[0])
        response = []
        for h in headers:
            response.append(h['name'])
        return response

    def headers_comprehension(self, _email):
        headers = _email['payload']['headers']
        response = {}
        for h in headers:
            response[h['name']] = h['value']
        return response

    def parse_datetime(self, _email, date_field = None):
        if date_field is None:
            date_field = self.headers_comprehension(_email)['Date']
        try:
            email_datetime = datetime.strptime(date_field, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            raise
        else:
            return email_datetime

    def parse_subject(self, email_subject, pattern):
        # check that there is only one match
        if len(re.findall(pattern, email_subject)) > 1:
            raise ValueError('Multiple matches in the field')
        elif len(re.findall(pattern, email_subject)) == 0:
            raise ValueError('No matches in the cost field')
        else:
            field_location = re.search(pattern, email_subject).span()[1]
            field = email_subject[field_location:]
            return field

    def parse_cost(self, email_subject):
        return Decimal(self.parse_subject(email_subject, "for £"))

    def parse_payee(self, email_subject):
        # returns everything after "purchase at"
        full_subject = self.parse_subject(email_subject, "Purchase at ")
        # gets an iter of every match of "on"
        field_iter = re.finditer(" on ", full_subject)
        matches = []
        for f in field_iter:
            matches.append(f)
        # finds the last match
        length = (len(matches) - 1)
        field_location = matches[length]
        char_location = field_location.span()[0]
        return full_subject[:char_location]

    def add_curve_emails(self):
        for e in self.emails:
            headers = self.headers_comprehension(e)
            message_id = headers['Message-ID']
            _datetime = self.parse_datetime(e)
            cost = self.parse_cost(headers['Subject'])
            payee = self.parse_payee(headers['Subject'])
            curve_email = CurveEmail(
                message_id,
                _datetime,
                cost,
                payee
            )
            self.curve_emails.append(curve_email)

    def parse_to(self):
        for e in self.emails:
            headers = self.get_headers(e)
            to = next(item for item in headers if item["name"] == "To")
            return to['value']


    def parse_category(self, curve_email):
        """
        If the payee is listed in the expected categories, return it,
        otherwise return the default
        """
        category = self.categories.get(curve_email.payee)
        if not category:
            return os.environ['CB_BEANCOUNT_EXPENSE_ACCOUNT']
        return category


    def convert_beancount(self, curve_email):
        txn_date = datetime.strftime(curve_email.datetime, "%Y-%m-%d")
        output_string = ""
        output_string += txn_date
        output_string += " ! "
        output_string += '"' + curve_email.payee + '"'
        output_string += ' ""'
        output_string += "\n"
        output_string += (" " * 2)
        output_string += os.environ['CB_BEANCOUNT_ACCOUNT']
        output_string += " -" + str(curve_email.cost) + " GBP"
        output_string += "\n"
        output_string += (" " * 2)
        output_string += self.parse_category(curve_email)
        output_string += ("\n" * 2)
        return output_string

    def full_beancount_output(self):
        curve_emails = self.curve_emails
        # oldest first
        curve_emails.sort(
            key=lambda c: c.datetime,
        )
        output_string = ""
        for c in curve_emails:
            output_string += self.convert_beancount(c)
        return output_string


    def get_card(self):
        """
        Searches through the body of the email to find the account
        """
        # TODO - add account parsing
        content = email.message_from_bytes(base64.urlsafe_b64decode(self.emails[0]['payload']['body']['data']))
        msg = email.message.EmailMessage()
        msg.set_content(content)
        for part in msg.walk():
            ctype = part.get_content_type()
            print(ctype)
            cdispo = str(part.get('Content-Disposition'))
            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
        # print(msg.get_payload(0).get_payload())



