import mysql.connector
import json

with open("config.json") as f:
    config = json.load(f)

try:
    conn = mysql.connector.connect(
          user=config["database_connection"]["username"],
          password=config["database_connection"]["password"],
          host=config["database_connection"]["host"],
          database=config["database_connection"]["database"])

    cursor = conn.cursor()

    cursor.close()

    print "Connection success"

except mysql.connector.errors.ProgrammingError as err:
    print "Error connecting to database: \n{}".format(err)
