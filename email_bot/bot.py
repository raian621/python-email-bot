from .logger import create_logger
from email.message import EmailMessage
import smtplib
from flask import render_template 

class EmailBot:
    # Logger object that can be instantiated to write logs to a file
    logger=None

    def __init__(self, email_address:str, password:str, smtp_address:str, smtp_port:str, log_file:str=None):
        self.email_address = email_address
        self.password = password
        # create member object logger if log_file (the path to a
        # log file) is specified.
        self.smtpserver = smtplib.SMTP_SSL(
            host=smtp_address, port=smtp_port
        )
        self.smtpserver.login(email_address, password)
        if log_file:
            self.logger = create_logger(log_file)

    def __del__(self):
        if self.logger:
            del self.logger
        self.smtpserver.close()

    def send_email(self, to, subject:str, template_path:str, context: dict):
        if isinstance(to, str):
            to = [to]

        html = render_template(template_path, **context)
        print(html)

        # msg = EmailMessage()
        # msg.add_header('Content-Type','text/html')
        # msg.set_payload()
        # msg['Subject'] = subject
        # msg['From'] = self.email_address
        # msg['To'] = to
        
        # email_success = self.smtpserver.send_message(msg)
        email_success = True
        if self.logger:
            if email_success:
                self.logger.log(f"'{subject}' sent to {to}")
                return True

            print(f"'{subject}' failed to send to {to}")
            self.logger.log(f"'{subject}' failed to send to {to}")
            return False


def create_email_bot(email_address:str, password:str, smtp_address:str, smtp_port:int, log_file:str=None) -> EmailBot:
    if log_file:
        return EmailBot(email_address, password, smtp_address, smtp_port, log_file)
    return EmailBot(email_address, password, smtp_address, smtp_port)