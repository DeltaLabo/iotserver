from paho.mqtt import client as client
import random
import time
from mqtt_params import BROKER_ADDRESS, MQTT_PORT, KEEP_ALIVE_S, USER, PASSWORD

# The callback function for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
# Create a new MQTT client instance
client = client.Client("test")

# Set the callback function for successful connections
client.on_connect = on_connect

# Set username and password
client.username_pw_set(USER, PASSWORD)

# Connect to the MQTT broker
client.connect(BROKER_ADDRESS, MQTT_PORT, KEEP_ALIVE_S)

# Start the network loop to handle incoming/outgoing messages
client.loop_start()

# Publish a message to the topic
topic = "test/float"
message = random.uniform(0.0, 1.0)
client.publish(topic, str(message))
print(f"Published message: {message} to topic: {topic}")

# Main program loop
try:
    while True:
        # Send data at 1s intervals
        message = random.uniform(0.0, 1.0)
        client.publish(topic, str(message))
        print(f"Published message: {message} to topic: {topic}")
        time.sleep(1)
except KeyboardInterrupt:
    # Stop the network loop and disconnect
    client.loop_stop()
    client.disconnect()