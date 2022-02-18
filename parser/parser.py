import email
import base64


class Parser:
    def __init__(self, emails):
        self.emails = emails

    def get_headers(self):
        for e in self.emails:
            headers = e['payload']['headers']
            to = next(item for item in headers if item["name"] == "To")
            print(to['value'])
            for h in headers:
                print(h['name'])
                print(h['value'])


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



