import paho.mqtt.client as mqtt
from os import getenv

broker_address=getenv("MQTT_IP")
broker_port=int(getenv("MQTT_PORT"))
mqtt_user=getenv("MQTT_USER")
mqtt_password=getenv("MQTT_PASSWORD")


client = mqtt.Client(client_id="test_publisher", transport="websockets", callback_api_version=mqtt.CallbackAPIVersion.VERSION2) #create new instance
client.username_pw_set(mqtt_user, mqtt_password)
print("connecting to broker")
client.tls_set()
client.connect(host=broker_address, port=broker_port,) #connect to broker
print("Trying to send message")
message = "Hello World!"
client.publish("hello/world", message)
print("Sent message:", message)

client.disconnect()