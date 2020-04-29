import os
import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

class sendmail():
    def __init__(self, sender, apikey):
        self.sender = sender
        self.sg = SendGridAPIClient(apikey)
        pass

    def sendfile(self, to=[], subject="test", content="", filename=""):
        message = Mail(
            from_email=self.sender,
            to_emails=to,
            subject=subject,
            html_content='<strong> '+ content +' </strong>'
        )
        with open(filename, 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()
        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName(filename.rsplit("/", 1)[1]),
            FileType('application/'+filename.rsplit(".", 1)[1]),
            Disposition('attachment')
        )
        message.attachment = attachedFile
        self.response = response = self.sg.send(message)
        print(response.status_code, response.body, response.headers)
        return response.status_code

        