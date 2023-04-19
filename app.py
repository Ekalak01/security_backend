from flask import Flask, jsonify, request
from flask_cors import CORS
from paho.mqtt import client as mqtt_client

app = Flask(__name__)
CORS(app)

door_status = {'locked': True}

broker = 'test.mosquitto.org'
port = 1883
topic = '123'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

client = mqtt_client.Client()
client.on_connect = on_connect
client.connect(broker, port)
client.loop_start()

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(door_status)

@app.route('/api/toggle', methods=['POST'])
def toggle_lock():
    global door_status
    door_status['locked'] = not door_status['locked']

    lock_status = 'LOCK' if door_status['locked'] else 'UNLOCK'
    client.publish(topic, lock_status)

    return jsonify(door_status)

if __name__ == '__main__':
    app.run(debug=True)
