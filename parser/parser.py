import email
import base64


class CurveEmail:
    def __init__(self, email_id, to):
        self.email_id = email_id
        self.to = to


class Parser:
    def __init__(self, emails):
        self.emails = emails

    def get_headers(self, email):
        headers = email['payload']['headers']
        return headers

    def list_headers(self):
        headers = self.get_headers(self.emails[0])
        response = []
        for h in headers:
            response.append(h['name'])
        return response

    def headers_comprehension(self):
        headers = self.get_headers(self.emails[0])
        response = []
        for h in headers:
            name = h['name']
            value = h['value']
            response.append({
                name: value
            }
            )
        return response


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



