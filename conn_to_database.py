import paho.mqtt.client as mqtt

broker_address="localhost"
print("creating new instance")
client = mqtt.Client() #create new instance
client.username_pw_set("user", "123")
print("connecting to broker")
client.connect(host=broker_address, port=1883,) #connect to broker

