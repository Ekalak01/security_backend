import paho.mqtt.client as mqtt
import json

# MQTT broker config
broker = 'test.mosquitto.org'
port = 1883
topic = '456'

# create MQTT client instance
client = mqtt.Client()

# connect to MQTT broker
client.connect(broker, port)

# publish message to topic
#message = {'people': 'INC'}
message = {'doorOpen': 'DOOR_CLOSE'}
print(message)
client.publish(topic, json.dumps(message))

# disconnect from MQTT broker
client.disconnect()
