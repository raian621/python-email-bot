from .logger import create_logger
from email.message import EmailMessage
from flask import render_template
import smtplib

class EmailBot:
    # Optional logger object that can be instantiated to write logs to a file
    logger=None

    def __init__(self, email_address:str, password:str, smtp_address:str, smtp_port:str, log_file:str=None):
        self.email_address = email_address
        self.password = password
        self.smtp_server = smtplib.SMTP_SSL(
            host=smtp_address, 
            port=smtp_port
        )
        # create member object logger if log_file (the path to a
        # log file) is specified.
        self.smtp_server.login(email_address, password)
        if log_file:
            self.logger = create_logger(log_file)

    def __del__(self):
        if self.logger:
            del self.logger
        self.smtpserver.close()

    def send_email(self, to, subject:str, template:str, context: dict):
        if isinstance(to, str):
            to = [to]

        html = render_template(template, **context)
        print(html)

        msg = EmailMessage()
        # msg.add_header('Content-Type','text/html')
        msg.make_related()
        msg.add_related(html, subtype='html')
        msg.set_payload(html)
        msg['Subject'] = subject
        msg['From'] = self.email_address
        msg['To'] = to
        
        try:
            self.smtp_server.send_message(msg)
            if self.logger:
                self.logger.log(f"'{subject}' sent to {to}")
                return True
        except:
            if self.logger:
                print(f"'{subject}' failed to send to {to}")
                self.logger.log(f"'{subject}' failed to send to {to}")
                return False


def create_email_bot(email_address:str, password:str, smtp_address:str, smtp_port:int, log_file:str=None) -> EmailBot:
    if log_file:
        return EmailBot(email_address, password, smtp_address, smtp_port, log_file)
    else:
        return EmailBot(email_address, password, smtp_address, smtp_port)