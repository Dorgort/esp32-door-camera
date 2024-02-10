import paho.mqtt.client as mqtt
import psycopg2
from psycopg2 import sql
import time
from os import getenv


db_params = {
    'host': getenv("DB_IP"),
    'port': int(getenv("DB_PORT")),
    'database': getenv("DB_NAME"),
    'user': getenv("DB_USER"),
    'password': getenv("DB_PASSWORD")
}
sql = """INSERT INTO images (image_data) VALUES(%s) RETURNING id;"""
result = ""

def mqtt_connect():
    broker_address=getenv("MQTT_IP")
    broker_port=int(getenv("MQTT_PORT"))
    mqtt_user=getenv("MQTT_USER")
    mqtt_password=getenv("MQTT_PASSWORD")

    print("creating new instance")
    client = mqtt.Client(client_id="db_saver", transport="websockets") #create new instance
    client.username_pw_set(mqtt_user, mqtt_password)
    print("connecting to broker")
    client.connect(host=broker_address, port=broker_port,) #connect to broker
    client.subscribe("image/db")
    
    
    return client

def mqtt_check(client):

    client.loop_start()
    client.on_message = on_message
    client.loop_stop()

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
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


