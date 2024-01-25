import psycopg2
from psycopg2 import sql

db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'camera_database',
    'user': 'user',
    'password': 'aetjauhwtwgbjreherh'
}

message = "hello world"
sql = """INSERT INTO test (message) VALUES(%s) RETURNING id;"""


try:
    conn = psycopg2.connect(**db_params)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute(sql, (message,))
    print(cur.fetchone()[0])

    # Make the changes to the database persistent
    conn.commit()
    cur.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()



