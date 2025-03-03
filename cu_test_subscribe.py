# Initialize libraries
import time
import paho.mqtt.client as paho
import sys
import RPi.GPIO as GPIO
from paho import mqtt
import json

# Initialize variables
toggle = False
connection_status = False
new_data = False
user_input = False
Sensor_1 = False
Sensor_2 = False
Sensor_3 = False
received = False
data = {}
IAQ_PM2 = 0
IAQ_PM10 = 0
IAQ_ovr = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

# Raw data from sensors comes in the following format:
# {"IAQI_PM2.5":12,"IAQI_PM10":2,"Overall_IAQI":12}
# NOTE: Numeric values between ":" and "," characters will change
# depending on real time data

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

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    global data
    global received
    global Sensor_1
    global Sensor_2
    global Sensor_3
    
    try:
        # THE FOLLOWING EXCERPT IS ADAPTED FROM AN AI GENERATED EXAMPLE:
        payload = msg.payload.decode("utf-8")
        
        if isinstance(payload, str):
            try:
                data = json.loads(payload)
                print("Received message: ", data)
                received = True
            except json.JSONDecodeError:
                print("Failed to decode message")
                data = None
                received = True
        else:
            print("Invalid message type")
            data = None
            received = True
        
    except Exception as e:
        print("Message cannot be parsed in this data type")
        data = None
        received = True
        # END OF AI GENERATED CODE
                
    if "Sensor1" in msg.topic:
        Sensor_1 = True
    elif "Sensor2" in msg.topic:
        Sensor_2 = True
    elif "Sensor3" in msg.topic:
        Sensor_3 = True
    else:
        pass
     
# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("freshair", "Freshair1")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("307235db588f42bda5a2c31d242ef05c.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.subscribe("Sensor1/#", qos=0)
client.subscribe("Sensor2/#", qos=0)
client.subscribe("Sensor3/#", qos=0)
# Begin loop for broker
client.loop_start()

while connection_status == False:
    print("Waiting on connection...")
    time.sleep(1)

while connection_status == True:
    time.sleep(1)
    # If acknowledged, turn off sirens
    
    if toggle == True:
        GPIO.output(5, False)
        GPIO.output(6, False)
            
    while received == True:
        # Parse sensor data
        if isinstance(data, dict):
            # If in the proper form, parse the IAQ values
            IAQ_PM2 = data.get("IAQI_PM2.5", 0)
            IAQ_PM10 = data.get("IAQI_PM10", 0)
            IAQ_ovr = data.get("Overall_IAQI", 0)
            new_data = True
            received = False
        elif data is None:
            # If the data is invalid (None), print a message and skip further processing
            print("Invalid data, waiting for new entry...")
            IAQ_PM2 = IAQ_PM10 = IAQ_ovr = 0  # Default values for invalid data
            received = False
        else:
            # If data is of an unexpected type, print a message and skip further processing
            print("Unexpected data entry, waiting for new entry...")
            IAQ_PM2 = IAQ_PM10 = IAQ_ovr = 0  # Default values for invalid data
            received = False

        
    if new_data:
        time.sleep(0.5)
        # If over/equal to conditions below, "Dangerous" PM condition met (via OSHA 1910.1000)
        if IAQ_PM2 >= 55 or IAQ_PM10 >= 255 or IAQ_ovr >=255:
            print("Dangerous")
            GPIO.output(5, True)
            new_data = False
            user_input = False
        # If under "Dangerous" threshold and over/equal to conditions below, "Unhealthy" PM condition met (via OSHA 1910.1000)
        elif IAQ_PM2 >= 35 or IAQ_PM10 >= 155 or IAQ_ovr >=155:
            print("Unhealthy")
            GPIO.output(6, True)
            new_data = False
            user_input = False
        # If below both conditions, "Healthy" PM condition met (via OSHA 1910.1000)
        else:
            print("Healthy")
            toggle = True
            new_data = False
            user_input = False
            
        if Sensor_1 == True:
            print("Sensor1")
        if Sensor_2 == True:
            print("Sensor2")
        if Sensor_3 == True:
            print("Sensor3")
            
client.loop_stop()
sys.exit()
