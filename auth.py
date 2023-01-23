from argon2 import PasswordHasher, exceptions
from datetime import timedelta, datetime
from secrets import token_urlsafe
from base64 import b64encode
from database import get_api_key
from flask import session
from time import sleep
from os import path

ph = PasswordHasher()

def authenticate_user(username, password):
    kmusername = None
    kmpassword = None
    with open('.kmpass', 'r') as kmpass:
        kmuser_data = kmpass.readline().split(':')
        print(kmuser_data)
        kmusername = kmuser_data[0]
        kmpassword = kmuser_data[1]

        if (kmusername != username):
            return False

    try:
        if (ph.verify(kmpassword, password)):
            if (ph.check_needs_rehash(kmpassword)):
                kmpassword = ph.hash(kmpassword)
                with open('.kmpass', 'w') as kmpass:
                    kmpass.write(f"{kmusername}:{kmpassword}")
            return True
    except exceptions.VerifyMismatchError as vme:
        print(vme.with_traceback)
        return False

def login_user(username, password):
    if 'next_attempt' in session and datetime.now().timestamp() < session['next_attempt'].timestamp():
        print("sleeping...")
        sleep((session['next_attempt'] - datetime.now()).total_seconds())
        print("woke up...")

    authenticated = authenticate_user(username, password)

    if authenticated:
        session['failed_logins'] = 0
        session['auth'] = True
        session['expires'] = datetime.now() + timedelta(minutes=10)
        session['username'] = username
    else:
        session['auth'] = False
        if 'failed_logins' in session:
            session['failed_logins'] += 1
            if session['failed_logins'] >= 10:
                session['locked'] = True
            elif session['failed_logins'] >= 3:
                session['next_attempt'] = datetime.now() + timedelta(seconds=5)
        else:
            session['failed_logins'] = 1

    session.modified = True

def generate_api_token():
    return token_urlsafe(16)

def authenticate_api_key(username, apikey):
    apikey_from_db = get_api_key(username)
    if apikey_from_db["username"] != username:
        return False

    try:
        ph.verify(apikey_from_db["key"], apikey)
        if (ph.check_needs_rehash(apikey_from_db["key"])):
            apikey_from_db["key"] = ph.hash(apikey)
        return True
    except exceptions.VerifyMismatchError as vme:
        print(vme.with_traceback)
        return False

def check_for_valid_kmpass():
    if not path.exists('.kmpass'):
        return False

    valid = False
    with open(".kmpass", "r") as kmpass:
        if len(kmpass.readline().split(':')) == 2:
            valid = True
    
    return valid
    