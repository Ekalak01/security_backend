from flask import Flask, jsonify, request
from flask_cors import CORS
from paho.mqtt import client as mqtt_client
import json
app = Flask(__name__)
CORS(app)

door_status = {'locked': False, 'peopleCount': 0, 'doorOpen': False}

broker = 'test.mosquitto.org'
port = 1883
topic = '456'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code %d\n", rc)

# def on_message(client, userdata, msg):
#     global door_status
#     message = msg.payload.decode()
#     print(message)
#     if message == 'INC':
#         door_status['peopleCount'] += 1
#     elif message == 'DEC':
#         door_status['peopleCount'] -= 1
#     elif message == 'DOOR_OPEN':
#         door_status['doorOpen'] = True
#     elif message == 'DOOR_CLOSED':
#         door_status['doorOpen'] = False
#     # update web page
#     update_webpage()

def on_message(client, userdata, msg):
    global door_status
    data = json.loads(msg.payload)
    print(data)
    if 'people' in data:
        if data['people'] == 'INC': 
            door_status['peopleCount'] += 1 
        else :
            door_status['peopleCount'] -= 1
            
    if 'doorOpen' in data:
        
        if data['doorOpen'] == 'DOOR_OPEN':
            door_status['doorOpen'] = True 
        else :
            door_status['doorOpen'] = False
    # update web page
    update_webpage()

def update_webpage():
    global door_status
    data = json.dumps(door_status)
    # publish message to topic "update" with data as payload
    print(door_status) 
    client.publish("update", data)
    


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
    try:
        global door_status
        if not door_status['locked'] and not door_status['doorOpen'] :
            door_status['locked'] = True
            if client.is_connected():
                lock_status = 'LOCK'
                # create MQTT client instance
                client2 = mqtt_client.Client()
                client2.connect('test.mosquitto.org', 1883)     
                client2.publish("123", lock_status)
                client2.disconnect()
                

        elif door_status['locked']:
            door_status['locked'] = False
            if client.is_connected():
                lock_status = 'UNLOCK'
                client2 = mqtt_client.Client()
                client2.connect('test.mosquitto.org', 1883)     
                client2.publish("123", lock_status)
                client2.disconnect()
                
        print(door_status)   
        return jsonify(door_status)
    except:
        pass

if __name__ == '__main__':
    
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    client.loop_start()
    app.run(debug=True)
