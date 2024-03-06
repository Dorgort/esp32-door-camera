import psycopg2
from psycopg2 import sql
from os import getenv

db_params = {
    'host': getenv("DB_IP"),
    'port': int(getenv("DB_PORT")),
    'database': getenv("DB_NAME"),
    'user': getenv("DB_USER"),
    'password': getenv("DB_PASSWORD")
}

message = "hello world"
sql = """INSERT INTO test (message) VALUES(%s) RETURNING id;"""


try:
    conn = psycopg2.connect(**db_params)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    #cur.execute(sql, (message,))
    #print(cur.fetchone()[0])
    cur.execute("SELECT * FROM images")
    print(cur.fetchall())
    cur.execute("SELECT * FROM logs")
    print(cur.fetchall())

    # Make the changes to the database persistent
    conn.commit()
    cur.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()



