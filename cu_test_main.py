import time
import paho.mqtt.client as paho
import sys
import RPi.GPIO as GPIO
from paho import mqtt

connection_status = False
IAQ_PM2 = 0
IAQ_PM10 = 0
IAQ_Overall = 0
Sensor_ID = 0

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
    
# Upon subscription, print confirmation
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Upon message, print confirmation
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    Sensor_ID = msg.topic
    print("ID" %s)
    if Sensor_ID = 1:
        client.publish("cu/id", payload="Sensor 1", qos=1)
        GPIO.output(5, True)
        GPIO.output(6, False)
        GPIO.output(6, False)
    elif Sensor_ID = 2:
        client.publish("cu/id", payload="Sensor 2", qos=1)
        GPIO.output(5, False)
        GPIO.output(6, True)
        GPIO.output(6, False)
    else:
        client.publish("cu/id", payload="Sensor 3", qos=1)
        GPIO.output(5, False)
        GPIO.output(6, False)
        GPIO.output(6, True)
        
    
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
    client.subscribe("Sensor1/#", qos=0)
    # If over/equal to 200 IAQ, "Dangerous" PM condition met
    if IAQ_PM2 >= 200 or IAQ_PM10 >= 200 or IAQ_Overall >=200:
        client.publish("cu/control", payload="Dangerous", qos=1)
        GPIO.output(5, True)
        GPIO.output(6, False)
    # If under 200 and over/equal to 100, "Unhealthy" PM condition met
    elif IAQ_PM2 >= 100 or IAQ_PM10 >= 100 or IAQ_Overall >=100:
        client.publish("cu/control", payload="Unhealthy", qos=1)
        GPIO.output(5, False)
        GPIO.output(6, True)
    # If below both conditions, "Healthy" PM condition met
    else:
        client.publish("cu/control", payload="Healthy", qos=1)
        GPIO.output(5, False)
        GPIO.output(6, False)

sys.exit()
