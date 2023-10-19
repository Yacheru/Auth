import pymysql
import pymysql.cursors
import json
import datetime


with open('config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

def connect_to_database():
    try:
        connection = pymysql.connect(
            host=cfg['MySQL']['host'],
            user=cfg['MySQL']['user'],
            password=cfg['MySQL']['password'],
            database=cfg['MySQL']['database'],
            cursorclass=pymysql.cursors.DictCursor)

        connection.autocommit = True

        print(f"[{datetime.datetime.now().strftime('%H:%M:%S, %d/%m')}] [MYSQL] [INFO] CONNECT SUCCESSFULLY")
        return connection
    except pymysql.Error as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S, %d/%m')}] [MYSQL] [ERROR] CONNECT FAILED WITH CODE {e}")
        return None


def check_and_reconnect(connection: pymysql.connect):
    try:
        connection.ping(reconnect=True)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S, %d/%m')}] [MYSQL] [INFO] THE CONNECTION TO THE DB IS ALIVE.")
    except pymysql.OperationalError as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S, %d/%m')}] [MYSQL] [ERROR] THE CONNECTION TO THE DB HAS BEEN DISCONNECTED. RECONNECTING... AS {e}")
        connection = connect_to_database()
    return connection

db_connection = connect_to_database()