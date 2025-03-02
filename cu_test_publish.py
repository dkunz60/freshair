import time
import paho.mqtt.client as paho
import sys
from paho import mqtt

connection_status = False

# Upon connection, print connection status and set global variable
def on_connect(client, userdata, flags, rc, properties=None):
    # THE FOLLOWING EXCERPT IS ADAPTED FROM AN AI GENERATED EXAMPLE:
    global connection_status
    if rc == 0:
        print("Successfully connected to the broker")
        connection_status = True
    else:
        print("Failed to connect, code %d" %rc)
        connection_status = False
    # END OF AI GENERATED CODE
    
# Upon published message, print confirmation
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Set up for connection function
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("freshair", "Freshair1")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("307235db588f42bda5a2c31d242ef05c.s1.eu.hivemq.cloud", 8883)
# Set up for publish function
client.on_publish = on_publish

# Begin loop for broker
client.loop_start()

# If connected, go through the following conditions:
while True:
    time.sleep(0.5)
    prompt1 = input("Enter a data value? [y/n]: ").lower()
    # If yes, prompt user for input
    if prompt1 == "y":
        payload = input("Enter data: ").lower()
        # Publish input to server
        client.publish("Sensor1/data", payload, qos=1)
    elif prompt1 == "n":
        # If no, end the loop
        client.loop_stop()
        print("Connection ended")
        break
    else:
        # If non y/n input, prompt the user again
        pass

sys.exit()
