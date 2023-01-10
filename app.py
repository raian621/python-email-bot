from flask import Flask, request, Response
from dotenv import load_dotenv
from os import path
import os
import json

from email_bot import create_email_bot

dotenv_path = path.join(path.dirname(__file__), '.env')
should_exit = False

if (load_dotenv(dotenv_path) is False):
    print("ERROR: .env not properly configured.")    
    should_exit = True

bot_email_address = os.environ['BOT_EMAIL_ADDRESS']
if (bot_email_address == None):
    print("ERROR: Environment variable 'BOT_EMAIL_ADDRESS' not found.")
    should_exit = True

bot_email_password = os.environ['BOT_EMAIL_PASSWORD']
if (bot_email_password == None):
    print("ERROR: Environment variable 'BOT_EMAIL_PASSWORD' not found.")
    should_exit = True

log_file = os.environ['EMAIL_BOT_LOG_FILE']
smtp_address = os.environ['SMTP_ADDRESS']
smtp_port = os.environ['SMTP_PORT']

app = Flask(__name__)

# email_bot is initially None, it will be created upon the first 
# POST request to the email API
email_bot = None

@app.route('/email-api', methods=['POST'])
def email_api():
    email_data = json.loads(request.data)
    global email_bot
    if email_bot is None:
        email_bot = create_email_bot(
            bot_email_address,
            bot_email_password,
            smtp_address,
            smtp_port,
            log_file
        )

    email_sent = email_bot.send_email(
        to = [email_data['to']],
        subject = email_data['subject'],
        template_path=email_data['template_path'],
        context = email_data['context'],
    )

    if email_sent:
        return Response(json.dumps({
                "message": "Email sent"
            }),
            status=201
        )
    else:
        return Response(json.dumps({
                "message": "Email failed to sent"
            }),
            status=301
        )

