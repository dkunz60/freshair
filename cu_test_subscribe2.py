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
# {"iaqi_pm2.5":12,"iaqi_pm10":2,"overall_iaqi":12}
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

# Print message if data is received from sensor
def on_message(client, userdata, msg):
    global data
    global received
    global toggle
    global Sensor_1
    global Sensor_2
    global Sensor_3
    
    # If toggled, set equal to true
    if "Toggle" in msg.topic and msg == True:
        toggle = True
    # If message is from sensor, parse data and determine sensor ID
    if "Sensor" in msg.topic:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print("Received message: ", data)
        received = True                    
    if "Sensor1" in msg.topic:
        Sensor_1 = True
    if "Sensor2" in msg.topic:
        Sensor_2 = True
    if "Sensor3" in msg.topic:
        Sensor_3 = True
     
# MQTT Initialization
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("freshair", "Freshair1")
client.connect("307235db588f42bda5a2c31d242ef05c.s1.eu.hivemq.cloud", 8883)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.subscribe("Sensor1/#", qos=0)
client.subscribe("Sensor2/#", qos=0)
client.subscribe("Sensor3/#", qos=0)
client.subscribe("Toggle/#", qos=0)
client.loop_start()

# Wait on broker connection
while connection_status == False:
    print("Waiting for connection...")
    time.sleep(1)

# Broker successfully connected
while connection_status == True:
    time.sleep(1)
    
    # If acknowledged, turn off sirens
    while toggle == True:
        GPIO.output(5, False)
        GPIO.output(6, False)
        print("Sirens off")
        toggle = False
            
    # If data received from sensors, parse it into useable variables
    while received == True:
        # Parse sensor data
        IAQ_PM2 = data.get("iaqi_pm2.5", 0)
        IAQ_PM10 = data.get("iaqi_10", 0)
        IAQ_ovr = data.get("overall_iaqi", 0)
        new_data = True
        received = False
    
    # If sensor data is parsed:   
    if new_data:
        time.sleep(0.5)
        # Publish individual values to broker
        client.publish("cu/IAQ_PM2.5", payload=IAQ_PM2, qos=0)
        client.publish("cu/IAQ_PM10", payload=IAQ_PM10, qos=0)
        client.publish("cu/IAQ_ovr", payload=IAQ_ovr, qos=0)
        # If over/equal to conditions below, "Dangerous" PM condition met (via OSHA 1910.1000)
        if IAQ_PM2 >= 55 or IAQ_PM10 >= 255 or IAQ_ovr >=255:
            client.publish("cu/pm_status", payload="Dangerous", qos=0)
            GPIO.output(5, True)
            new_data = False
            user_input = False
        # If under "Dangerous" threshold and over/equal to conditions below, "Unhealthy" PM condition met (via OSHA 1910.1000)
        elif IAQ_PM2 >= 35 or IAQ_PM10 >= 155 or IAQ_ovr >=155:
            client.publish("cu/pm_status", payload="Unhealthy", qos=0)
            GPIO.output(6, True)
            new_data = False
            user_input = False
        # If below both conditions, "Healthy" PM condition met (via OSHA 1910.1000)
        else:
            client.publish("cu/pm_status", payload="Healthy", qos=0)
            toggle = True
            new_data = False
            user_input = False
        
        # Publish sensor ID of the data to the broker    
        if Sensor_1 == True:
            client.publish("cu/sensor_id", payload="Sensor 1", qos=0)
        if Sensor_2 == True:
            client.publish("cu/sensor_id", payload="Sensor 2", qos=0)
        if Sensor_3 == True:
            client.publish("cu/sensor_id", payload="Sensor 3", qos=0)
            
client.loop_stop()
sys.exit()
