import time
import sys

connection_status = False
user_input = False
IAQ_PM2 = 0
IAQ_PM10 = 0
IAQ_Overall = 0
Sensor_ID = 0

# Data string parsing variables
start_2 = "{\"IAQI_PM2.5\":"
end_2 = ",\"IAQI_PM10"
start_10 = "IAQI_PM10\":"
end_10 = ",Overall"
start_overall = "Overall_IAQI\":"
end_overall = "}"
PM2_str = ""
PM10_str = ""
Overall_str = ""

print(start_2)

while user_input == False:
    data = input("Enter data string: ")
    user_input = True
    
parse_2 = text.split(start_2)
if len(parse_2) > 1:
    PM2_str = parse_2[1].split(end_2)[0]
    print(PM2_str)

while connection_status == True:
    time.sleep(0.5)
    # If over/equal to 200 IAQ, "Dangerous" PM condition met
    if IAQ_PM2 >= 200 or IAQ_PM10 >= 200 or IAQ_Overall >=200:
        print("Dangerous")
    # If under 200 and over/equal to 100, "Unhealthy" PM condition met
    elif IAQ_PM2 >= 100 or IAQ_PM10 >= 100 or IAQ_Overall >=100:
        print("Unhealthy")
    # If below both conditions, "Healthy" PM condition met
    else:
        print("Healthy")
    

sys.exit()