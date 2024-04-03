import paho.mqtt.server as mqtt
from mqtt_params import BROKER_ADDRESS, MQTT_PORT

# Define callback functions for events
def on_connect(client, userdata, flags, rc):
    print(f"Client connected with result code {str(rc)}")

def on_message(client, userdata, message):
    print(f"Message received on topic {message.topic}: {str(message.payload)}")

# Create an MQTT broker
broker = mqtt.Mosquitto()

# Assign callback functions to events
broker.on_connect = on_connect
broker.on_message = on_message

# Start the broker
broker.listen(BROKER_ADDRESS, MQTT_PORT)
broker.start()