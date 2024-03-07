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
sql_insert_log = """INSERT INTO logs (text) VALUES(%s) RETURNING id;"""
result = ""

def mqtt_connect():
    broker_address=getenv("MQTT_IP")
    broker_port=int(getenv("MQTT_PORT"))
    mqtt_user=getenv("MQTT_USER")
    mqtt_password=getenv("MQTT_PASSWORD")

    print("creating new instance")
    client = mqtt.Client(client_id="db_saver", transport="websockets", callback_api_version=mqtt.CallbackAPIVersion.VERSION2) #create new instance
    client.username_pw_set(mqtt_user, mqtt_password)
    client.will_set(topic="connection/db", payload='DB ist nicht mehr verbunden')
    print("connecting to broker")
    client.tls_set()
    client.connect(host=broker_address, port=broker_port,) #connect to broker
    client.publish(topic="connection/db", payload='DB ist verbunden')
    print("connected")
    client.subscribe("db/image")
    client.subscribe("face")
    client.subscribe("door")
    
    
    return client

def mqtt_check(client):
    client.loop_start()
    client.on_message = on_message
    client.loop_stop()

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    global result 
    result = message.topic, str(message.payload.decode("utf-8"))
    #print (result[0])

def database_send(message, client):
    conn = None
    try:
        conn = psycopg2.connect(**db_params)

        # Open a cursor to perform database operations
        cur = conn.cursor()
        topic = message[0]
        content = message[1]
        if topic == "face":
            cur.execute(sql_insert_log, (content+" war an deiner Haustür.", ))
            print(cur.fetchone()[0])
        elif topic == "db/image":
            cur.execute(sql_insert_log, (content,))
            print(cur.fetchone()[0])
        elif topic == "door":
            cur.execute(sql_insert_log, ("Tür ist jetzt "+content,))
            print(cur.fetchone()[0])

        # Make the changes to the database persistent
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        client.publish("connection/db", "DB nicht erreichbar.")
        print(error)
    finally:
        if conn is not None:
            conn.close()

def main():
    client = mqtt_connect()
    global result
    while True:
        
        mqtt_check(client)
        
        #print(time.time(), "Connected to MQTT")
        if result != "":
            database_send(result, client)
            result = ""


if __name__ == '__main__':
    main()


