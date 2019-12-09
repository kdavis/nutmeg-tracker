import os
import time
import sys
import pymysql
from time import strftime
from nutmeg import Nutmeg

EMAIL = os.environ.get('NUTMEG_EMAIL')
PASSWORD = os.environ.get('NUTMEG_PASSWORD')
HOURS = int(os.environ.get('HOURS'))
DB_HOST = os.environ.get('DB_HOST')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PORT = int(os.environ.get('DB_PORT'))
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')

if EMAIL is None or PASSWORD is None or HOURS is None or DB_HOST is None:
    print("Environment variables are needed!")
    sys.exit(0)

db_create_query = """
CREATE TABLE IF NOT EXISTS nutmeg_pots (
    Id INT AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Type VARCHAR(255) NOT NULL,
    Value DECIMAL(18,2) NOT NULL,
    RecordDateTime DATETIME NOT NULL,
    PRIMARY KEY (Id)
)
"""


def execute_query(query):
    conn = pymysql.connect(host=DB_HOST, port=DB_PORT,
                           user=DB_USERNAME, passwd=DB_PASSWORD, db=DB_DATABASE)
    cur = conn.cursor()

    cur.execute(query)

    cur.close()
    conn.commit()
    conn.close()


execute_query(db_create_query)

print("Created database")

while True:
    nutmeg = Nutmeg(EMAIL, PASSWORD)
    nutmeg.login()

    values = nutmeg.get_values()
    for value in values:
        print("Found value of %s for %s" % (value[2], value[1]))

        insert_query = "INSERT INTO nutmeg_pots (Name, Type, Value, RecordDateTime) values ('%s', '%s', %s, '%s')" % (
            value[0], value[1], value[2], strftime("%Y-%m-%d %H:%M:%S"))

        execute_query(insert_query)

    print("Inserted data points.")
    time.sleep(HOURS * 3600)
