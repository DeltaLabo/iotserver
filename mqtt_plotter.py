import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import numpy as np

# List to store received values
values = []

# The callback function for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        value = float(payload)
        values.append(value)
        print(f"Received value: {value}")
        update_plot()
    except ValueError:
        print(f"Invalid value received: {payload}")

# Function to update the plot
def update_plot():
    plt.cla()  # Clear the plot
    plt.plot(values)
    plt.xlabel("Sample")
    plt.ylabel("Value")
    plt.title("MQTT Data Plot")
    plt.pause(0.001)  # Pause to allow the plot to update

# Create a new MQTT client instance
client = mqtt.Client()

# Set the callback function for incoming messages
client.on_message = on_message

# Connect to the MQTT broker
client.connect("broker.example.com", 1883, 60)  # Replace with your broker address and port

# Subscribe to the topic
topic = "test/float"
client.subscribe(topic)

# Start the network loop to receive messages
client.loop_start()

# Create a figure for plotting
plt.ion()  # Enable interactive mode
fig = plt.figure()

print("Waiting for incoming data...")

# Keep the script running until interrupted
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopping...")
    client.loop_stop()
    client.disconnect()
    plt.close()