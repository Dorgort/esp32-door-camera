import paho.mqtt.client as mqtt

broker_address="localhost"
print("creating new instance")
client = mqtt.Client() #create new instance
client.username_pw_set("user", "123")
print("connecting to broker")
client.connect(host=broker_address, port=1883,) #connect to broker
print("Subscribing to topic","hello/world")
client.subscribe("hello/world")

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client.on_message = on_message

client.loop_forever()