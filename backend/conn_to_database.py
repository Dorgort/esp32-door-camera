import paho.mqtt.client as mqtt
import psycopg2
from psycopg2 import sql
import time


db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'camera_database',
    'user': 'user',
    'password': 'aetjauhwtwgbjreherh'
}
sql = """INSERT INTO test (message) VALUES(%s) RETURNING id;"""
result = ""

def mqtt_connect():
    broker_address="localhost"
    client = mqtt.Client() #create new instance
    client.username_pw_set("user", "123")
    print("Connecting...")
    client.connect(host=broker_address, port=1883,) #connect to broker
    client.subscribe("hello/world")
    return client

def mqtt_check(client):

    client.loop_start()
    client.on_message = on_message
    client.loop_stop()

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    global result 
    result = str(message.payload.decode("utf-8"))
    print (result)
    

    
    


def database_send(message):
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

def main():
    client = mqtt_connect()
    global result
    while True:
        time.sleep(1)
        
        mqtt_check(client)
        
        print(type(result), result)
        if result != "":
            database_send(result)
            result = ""


if __name__ == '__main__':
    main()


