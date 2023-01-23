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

apikeys = []

def get_api_keys():
    return apikeys

def delete_api_keys(to_be_deleted):
<<<<<<< HEAD:email-bot/database.py
    print(to_be_deleted)
=======
    if type(to_be_deleted) == list:
        apikeys.remove(apikeys[to_be_deleted])
        return

>>>>>>> auth:database.py
    for user in to_be_deleted:
        for key in apikeys:
            if key["username"] == user:
                apikeys.remove(key)

def add_api_key(apikey):
    apikey["key"] = ph.hash(apikey["key"])
    apikeys.append(apikey)

    return True

def get_api_key(username):
    for key in apikeys:
        if key["username"] == username:
            return key

    return None
