from logger import create_logger
import smtplib

class EmailBot:
    # Logger object that can be instantiated to write logs to a file
    logger=None

    def __init__(self, email_address:str, password:str, log_file:str=None):
        self.email_address = email_address
        self.password = password
        # create member object logger if log_file (the path to a
        # log file) is specified.
        if log_file:
            self.logger = create_logger(log_file)

    def __del__(self):
        if self.logger:
            del self.logger

    def send_email(self, to:str, subject:str, message:str):
        if self.logger:
            self.logger.log(f"'{subject} - {message}' sent to {to}")

    
            

def create_email_bot(email_address:str, password:str, log_file:str=None) -> EmailBot:
    if log_file:
        return EmailBot(email_address, password, log_file)
    return EmailBot(email_address)