import psycopg2
import json
import datetime


with open('config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

try:
    connection = psycopg2.connect(
        host=cfg['PostgreSQL']['host'],
        user=cfg['PostgreSQL']['user'],
        password=cfg['PostgreSQL']['password'],
        database=cfg['PostgreSQL']['database'],
    )
    print(f"[POSTGRESQL] [INFO] [{datetime.datetime.now().strftime('%d/%m %H:%M')}] CONNECT SUCCESSFUL")

    pcursor = connection.cursor()
    connection.autocommit = True

except psycopg2.Error as e:
    print(f"[POSTGRESQL] [ERROR] [{datetime.datetime.now().strftime('%d/%m %H:%M')}] CONNECT FAILED WITH CODE {e}")