from .logger import create_logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from flask import render_template
from image_registry import image_registry, ImageEntry
import smtplib

def build_mime_multipart_message(email_address:str, to, subject:str, template:str, context: dict) -> MIMEMultipart:
    if isinstance(to, str):
        to = [to]
    
    to_str = ""
    for recipient in to:
        to_str += (f"{recipient},")

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to_str
    msg.preamble = 'This is a multi-part message in MIME format.'

    msgHTML = MIMEText(render_template(template, **context), 'html')
    msg.attach(msgHTML)

    # TODO: add some kind of cache (LRU? idk) so that we can improve
    # efficiency

    # adds images stored in image registry for the current template to
    # the MIME message
    for entry in image_registry[template]:
        with open(entry.img_path, 'rb') as img_file:
            msgImage = MIMEImage(img_file.read())
            msgImage.add_header('Content-ID', f"<{entry.cid}>")
            msg.attach(msgImage)

    return msg

    
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
        # msg.add_header('Content-Type','text/html')
        msg = build_mime_multipart_message(self.email_address, to, subject, template, context)        
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