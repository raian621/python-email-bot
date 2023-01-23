from argon2 import PasswordHasher
import psycopg2

class Database:
    def __init__(self):
        self.conn = None

    def __del__(self):
        if self.conn != None:
            self.conn.close()

    def connect_to_database(
        self,
        dbname="postgres", 
        user="postgres", 
        password=None, 
        host="localhost",
        port=5432
    ):
        if self.conn == None:
            self.details = {
                "dbname": dbname,
                "user": user,
                "password": password,
                "host": host,
                "port": port
            }
        elif self.conn.closed != False:
            self.conn.close()
        
        self.conn = psycopg2.connect(**self.details)

    def available(self):
        return self.conn != None and self.conn.closed == 0

    def reconnect(self):
        self.connect_to_database(**self.details)

db = Database()

def connect_to_database(
    dbname="postgres", 
    user="postgres", 
    password=None, 
    host="localhost",
    port=5432
):
    db.connect_to_database(dbname, user, password, host, port)

def create_tables():
    if not db.available():
        try:
            db.reconnect()
        except psycopg2.Error as e:
            print(e.pgerror)
            return

    with db.conn.cursor() as cur:
        cur.execute("""
            CREATE IF NOT EXISTS TABLE users (
                uid INT GENERATED ALWAYS AS IDENTITY
                uname varchar(50) NOT NULL
                passwd VARCHAR(100) NOT NULL
                role NOT NULL
            );
        """)
        cur.execute("""
            CREATE IF NOT EXISTS TABLE apikeys (
                aid INT SERIAL PRIMARY KEY
                owner INT REFERENCES users(uid) NOT NULL
                key VARCHAR(100) NOT NULL
                expires DATE
            );
        """)
        
ph = PasswordHasher()
registered_users = { 
    "bob": {
        "username": "bob",
        "password": ph.hash("password"),
        "role": "admin",
        "locked": False
    }
}

apikeys = [
    { "title": "Cat key", "created": "today", "expires": "tommorrow", "username": "bob" },
    { "title": "Rat key", "created": "today", "expires": "tommorrow", "username": "bob" },
    { "title": "Fox key", "created": "today", "expires": "tommorrow", "username": "bob" },
    { "title": "Dog key", "created": "today", "expires": "tommorrow", "username": "bob" },
]

def get_user_from_db(username):
    if username in registered_users:
        return registered_users(username)
    else:
        return None

def get_api_keys_for_user(username):
    keys = []
    
    for key in apikeys:
        if key["username"] == username:
            keys.append(key)

    return keys

def delete_api_keys_for_user(username, user_apikeys):
    pass

def add_api_key_for_user(username, apikey):
    if username not in apikeys:
        apikeys[username] = []
    
    apikeys[username].append(apikey)

    return True

def get_api_key_by_title(title):
    keys = []

    for key in apikeys:
        if key["title"] == title:
            keys.append(key)

    return keys