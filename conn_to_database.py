import paho.mqtt.client as mqtt

broker_address="localhost"
print("creating new instance")
client = mqtt.Client() #create new instance
client.username_pw_set("camera", "camera")
print("connecting to broker")
client.connect(host=broker_address, port=1883,) #connect to broker
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("hello/topic")
print("Publishing message to topic","house/bulbs/bulb1")
client.publish("hello/topic/bulb1","OFF")
