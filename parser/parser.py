import email
import base64
from datetime import datetime
import re
from decimal import Decimal


class CurveEmail:
    def __init__(self, email_id, _datetime):
        self.email_id = email_id
        self.datetime = _datetime


class Parser:
    def __init__(self, emails: list, curve_emails: list[CurveEmail] = []):
        self.emails = emails
        self.curve_emails = curve_emails

    def get_headers(self, _email):
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


    def parse_cost(self, _email, cost_field = None):
        if cost_field is None:
            cost_field = self.headers_comprehension(_email)['Subject']
        print(cost_field)
        pattern = "for £"
        # check that there is only one match
        if len(re.findall(pattern, cost_field)) > 1:
            raise ValueError('Multiple matches in the cost field')
        elif len(re.findall(pattern, cost_field)) == 0:
            raise ValueError('No matches in the cost field')
        else:
            cost_location = re.search(pattern, cost_field).span()[1]
            cost = Decimal(cost_field[cost_location:])
            return cost


    def add_curve_emails(self):
        for e in self.emails:
            headers = self.headers_comprehension(e)
            message_id = headers['Message-ID']
            _datetime = headers['Received']
            curve_email = CurveEmail(
                message_id,
                _datetime
            )
            self.curve_emails.append(curve_email)

    def parse_to(self):
        for e in self.emails:
            headers = self.get_headers(e)
            to = next(item for item in headers if item["name"] == "To")
            return to['value']


    def get_card(self):
        """
        Searches through the body of the email to find the account
        """

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



