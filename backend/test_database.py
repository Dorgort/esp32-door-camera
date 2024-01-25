import psycopg2
from psycopg2 import sql

db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'camera',
    'user': 'camera',
    'password': 'camera'
}

conn = psycopg2.connect(**db_params)

# Open a cursor to perform database operations
cur = conn.cursor()
# Execute a command: create datacamp_courses table
cur.execute("""select * from information_schema.tables
            """)

print (cur.fetchall())
# Make the changes to the database persistent
conn.commit()
# Close cursor and communication with the database
cur.close()
conn.close()



