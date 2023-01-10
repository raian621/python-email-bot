from flask import Flask, request
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

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# email_bot is initially None, it will be created upon the first 
# POST request to the email API
email_bot = None

@app.route('/email-api', methods=['POST'])
def email_api():
    print(bot_email_address)
    email_data = json.loads(request.data)
    if email_bot is None:
        email_bot = create_email_bot(bot_email_address, bot_email_password, log_file)
    
    email_bot.send_email()

    return json.dump({
        "message": "Email sent"
    })
