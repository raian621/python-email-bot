from flask import Flask, request, Response, render_template, session, redirect, url_for
from dotenv import load_dotenv
from argon2 import PasswordHasher
from auth import login_user, generate_api_token, authenticate_api_key, check_for_valid_kmpass
from os import path
from time import sleep
from datetime import datetime
from database import get_api_keys, add_api_key, delete_api_keys
import os
import json

from email_bot import create_email_bot
import register_images

dotenv_path = path.join(path.dirname(__file__), '.env')
should_exit = False

if not check_for_valid_kmpass():
    if 'KM_PASSWORD' in os.environ and 'KM_USERNAME' in os.environ:
        kmusername = os.environ['KM_USERNAME']
        kmpassword = os.environ['KM_PASSWORD']

        ph = PasswordHasher()
        kmpassword = ph.hash(kmpassword)

        with open('.kmpass', 'w') as kmpass:
            kmpass.write(f"{kmusername}:{ph.hash(kmpassword)}")
    else:
        print("ERROR: No Key Manager credentials specified in environment or file '.kmpass'. Without Key Manager credentials, you cannot create or  manage api keys.")
        should_exit = True

if (load_dotenv(dotenv_path) is False):
    print("ERROR: .env not properly configured.")    
    should_exit = True

required_env_vars = ['BOT_EMAIL_ADDRESS', 'BOT_EMAIL_PASSWORD', 'SMTP_ADDRESS', 'SMTP_PORT']
for required in required_env_vars:
    if (os.environ[required] == None):
        print(f"ERROR: Required environment variable '{required}' not found.")
        should_exit = True

# ensure all environment variable errors are reported before exiting
# so that we don't play "error whack-a-mole" in the future
if should_exit:
    exit(1)

app = Flask(__name__)
# TODO: change this to an environment or config variable
app.secret_key = 'XMlvpaxlgYl8JpTcI5x9JQ'

# email_bot is initially None, it will be created upon the first 
# POST request to the email API
email_bot = None

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if 'auth' in session and session['auth']:
        return render_template('dashboard/dashboard.html')
    return redirect(url_for('login'))

@app.route('/send-email', methods=['POST'])
def email_api():

    if request.method == 'POST':
        authorization = request.authorization

        if not authenticate_api_key(authorization.username, authorization.password):
            return Response(status=401)

        print(request.url)
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
            return Response()
        else:
            return Response(json.dumps({
                    "message": "Email failed to sent"
                }),
                status=301
            )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'auth' in session and session['auth']:
            print("user authenticated")
            return redirect(url_for('dashboard'))

        return render_template('login/login.html')
    if request.method == 'POST':
        authorization = request.authorization
        print("Authorization:", authorization)
        username = authorization['username']
        password = authorization['password']

        login_user(username, password)
        
        res = Response()
        if not session['auth']:
            res.status = 401
        return res

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api-keys',methods=['GET', 'POST', 'DELETE'])
def api_keys():
    if 'auth' not in session or not session['auth']:
        return Response(status=401)
    
    if request.method == 'GET':
        return Response(json.dumps(get_api_keys()), headers={"content_type": "application/json"})
    if request.method == 'POST':
        data = request.json
        print(data)
        if 'title' in data and 'created' in data and 'expires' in data and 'username' in data:
            # truncate unneeded data
            apitoken = generate_api_token()
            add_api_key({
                "key": apitoken,
                "title": data["title"],
                "created": data["created"], 
                "expires": data["expires"],
                "username": data["username"]
            })
            return Response(json.dumps({"apitoken": apitoken}))
        return Response(status=400)
    if request.method == 'DELETE':
        data = request.json
      
        print(data)
        delete_api_keys(data["toBeDeleted"])
        return Response()
