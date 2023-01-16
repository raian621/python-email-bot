from flask import Flask, request, Response
from dotenv import load_dotenv
from os import path
import os
import json

from email_bot import create_email_bot
import register_images

dotenv_path = path.join(path.dirname(__file__), '.env')
should_exit = False

if (load_dotenv(dotenv_path) is False):
    print("ERROR: .env not properly configured.")    
    should_exit = True

required_env_vars = ['BOT_EMAIL_ADDRESS', 'BOT_EMAIL_PASSWORD', 'SMTP_ADDRESS', 'SMTP_PORT']
for required in required_env_vars:
    if (os.environ[required] == None):
        print(f"ERROR: Required nvironment variable '{required}' not found.")
        should_exit = True

# ensure all environment variable errors are reported before exiting
# so that we don't play "error whack-a-mole" in the future
if should_exit:
    exit(1)

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
            os.environ["BOT_EMAIL_ADDRESS"],
            os.environ["BOT_EMAIL_PASSWORD"],
            os.environ["SMTP_ADDRESS"],
            os.environ["SMTP_PORT"],
            os.environ["EMAIL_BOT_LOG_FILE"],
        )

    # TODO: check that all email data keys are valid and present

    print(email_data)

    email_sent = email_bot.send_email(
        to = [email_data['to']],
        subject = email_data['subject'],
        template = email_data['template'],
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