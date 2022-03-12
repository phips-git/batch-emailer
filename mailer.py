import time
from os import environ, path, getcwd
from ssl import create_default_context
from smtplib import SMTPSenderRefused, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailer:
    SERVER_URL_ENV_KEY = "SERVER_URL"
    SERVER_PORT_ENV_KEY = "SERVER_PORT"
    USERNAME_ENV_KEY = "MAIL_HOST_USERNAME"
    PASSWORD_ENV_KEY = "MAIL_HOST_PASSWORD"
    RECIPIENTS_FILENAME_ENV_KEY = "RECIPIENTS_FILENAME"
    TEMPLATE_FILENAME_ENV_KEY = "TEMPLATE_FILENAME"
    IMAGE_FILENAMES_ENV_KEY = "IMAGE_"
    MAIL_SENDER_ENV_KEY = "MAIL_SENDER"
    MAIL_SUBJECT_ENV_KEY = "MAIL_SUBJECT"
    MAIL_BUFFER_SECONDS = 2

    def __init__(self):
        self.server_url = environ.get(self.SERVER_URL_ENV_KEY)
        self.server_port = environ.get(self.SERVER_PORT_ENV_KEY)
        self.username = environ.get(self.USERNAME_ENV_KEY)
        self.password = environ.get(self.PASSWORD_ENV_KEY)
        self.recipients_filename = environ.get(self.RECIPIENTS_FILENAME_ENV_KEY)
        self.template_filename = environ.get(self.TEMPLATE_FILENAME_ENV_KEY)
        self.sender = environ.get(self.MAIL_SENDER_ENV_KEY)
        self.subject = environ.get(self.MAIL_SUBJECT_ENV_KEY)
        self.recipients = self._get_recipients_from_file()
        self.total_count = len(self.recipients)
        self.current_recipient_index = 0
        self.html_template = self._get_html_from_file()
        self.context = create_default_context()

    def start_mailing(self):
        for index, recipient in enumerate(self.recipients[self.current_recipient_index :]):
            with SMTP_SSL(self.server_url, self.server_port, context=self.context) as server:
                server.login(self.username, self.password)
                print(f"Sending mail {self.current_recipient_index + 1} of {self.total_count} to {recipient}...")
                self.current_recipient_index = index
                try:
                    server.sendmail(self.sender, recipient, self._prepare_mail(recipient))
                except SMTPSenderRefused:
                    print(f"Could not send to {recipient} due to a SenderRefusedError. Skipping...")

    def _get_recipients_from_file(self):
        if not path.isfile(getcwd() + self.recipients_filename):
            print("Recipients file does not exist.")
        else:
            recipients = []
            with open(getcwd() + self.recipients_filename) as f:
                lines = f.read().splitlines()
                for line in lines:
                    if line:
                        recipients.append(line)
            return recipients

    def _prepare_mail(self, recipient):
        msgRoot = MIMEMultipart("related")
        msgRoot["Subject"] = self.subject
        msgRoot["From"] = self.sender
        msgRoot["To"] = recipient
        msgRoot.attach(MIMEText(self.html_template, "html", "utf-8"))
        return msgRoot.as_string()

    def _get_html_from_file(self):
        if not path.isfile(getcwd() + self.template_filename):
            print("Template file does not exist.")
        else:
            with open(getcwd() + self.template_filename) as f:
                return f.read()


emailer = Emailer().start_mailing()
