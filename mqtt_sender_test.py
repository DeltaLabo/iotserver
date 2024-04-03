import paho.mqtt.client as mqtt
import random

# The callback function for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Create a new MQTT client instance
client = mqtt.Client()

# Set the callback function for successful connections
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect("broker.example.com", 1883, 60)  # Replace with your broker address and port

# Start the network loop to handle incoming/outgoing messages
client.loop_start()

# Publish a message to the topic
topic = "test/float"
message = random.uniform(0.0, 1.0)
client.publish(topic, str(message))
print(f"Published message: {message} to topic: {topic}")

# Keep the script running for a while to allow message delivery
import time
time.sleep(2)

# Stop the network loop and disconnect
client.loop_stop()
client.disconnect()