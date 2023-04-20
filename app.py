from flask import Flask, jsonify, request
from flask_cors import CORS
from paho.mqtt import client as mqtt_client

app = Flask(__name__)
CORS(app)

door_status = {'locked': True, 'peopleCount': 0, 'doorOpen': False}

broker = 'test.mosquitto.org'
port = 1883
topic = '123'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    global door_status
    message = msg.payload.decode()
    
    if message == 'INC':
        door_status['peopleCount'] += 1
    elif message == 'DEC':
        door_status['peopleCount'] -= 1
    elif message == 'DOOR_OPEN':
        door_status['doorOpen'] = True
    elif message == 'DOOR_CLOSED':
        door_status['doorOpen'] = False
 
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_start()

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(door_status)

# @app.route('/api/toggle', methods=['POST'])
# def toggle_lock():
#     global door_status
#     door_status['locked'] = not door_status['locked']

#     lock_status = 'LOCK' if door_status['locked'] else 'UNLOCK'
#     client.publish(topic, lock_status)
    
#     return jsonify(door_status)

@app.route('/api/toggle', methods=['POST'])
def toggle_lock():
    global door_status
    if not door_status['locked'] and not door_status['doorOpen']:
        door_status['locked'] = True

        lock_status = 'LOCK'
        client.publish(topic, lock_status)

    elif door_status['locked']:
        door_status['locked'] = False

        lock_status = 'UNLOCK'
        client.publish(topic, lock_status)
        print(door_status)   
    return jsonify(door_status)


if __name__ == '__main__':
    app.run(debug=True)
