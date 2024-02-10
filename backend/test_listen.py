import paho.mqtt.client as mqtt
from os import getenv


broker_address=getenv("MQTT_IP")
broker_port=int(getenv("MQTT_PORT"))
mqtt_user=getenv("MQTT_USER")
mqtt_password=getenv("MQTT_PASSWORD")


print("creating new instance")
client = mqtt.Client(client_id="test_listener", transport="websockets") #create new instance
client.username_pw_set(mqtt_user, mqtt_password)
print("connecting to broker")
client.connect(host=broker_address, port=broker_port,) #connect to broker
print("Subscribed: hello/world")
client.subscribe("hello/world")

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client.on_message = on_message

client.loop_forever()