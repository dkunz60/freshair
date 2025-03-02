import time

connection_status = False
user_input = False
IAQ_PM2 = 0
IAQ_PM10 = 0
IAQ_ovr = 0
Sensor_ID = 0

# Raw data from sensors comes in the following format:
# {"IAQI_PM2.5":12,"IAQI_PM10":2,"Overall_IAQI":12}
# NOTE: Numeric values between ":" and "," characters will change
# depending on real time data

# Data string parsing variables
start_2 = "{\"IAQI_PM2.5\":"
end_2 = ",\"IAQI_PM10"
start_10 = "IAQI_PM10\":"
end_10 = ",\"Overall"
start_ovr = "Overall_IAQI\":"
end_ovr = "}"
PM2_str = ""
PM10_str = ""
ovr_str = ""

# Wait for data input
while user_input == False:
    data = input("Enter data string: ")
        
    # Parse PM2.5 data
    parse_2 = data.split(start_2)
    if len(parse_2) > 1:
        PM2_str = parse_2[1].split(end_2)[0]
        print(PM2_str)
        IAQ_PM2 = int(PM2_str)

    # Parse PM10 data
    parse_10 = data.split(start_10)
    if len(parse_10) > 1:
        PM10_str = parse_10[1].split(end_10)[0]
        print(PM10_str)
        IAQ_PM10 = int(PM10_str)
        
    # Parse Overall PM data
    parse_ovr = data.split(start_ovr)
    if len(parse_ovr) > 1:
        ovr_str = parse_ovr[1].split(end_ovr)[0]
        print(ovr_str)
        IAQ_ovr = int(ovr_str)
        
    if IAQ_ovr == 0 and IAQ_PM2 == 0 and IAQ_PM10 == 0:
        print("Invalid data entry")
    else:
        user_input = True
        
    
while connection_status == True:
    time.sleep(0.5)
    # If over/equal to 200 IAQ, "Dangerous" PM condition met
    if IAQ_PM2 >= 200 or IAQ_PM10 >= 200 or IAQ_ovr >=200:
        print("Dangerous")
    # If under 200 and over/equal to 100, "Unhealthy" PM condition met
    elif IAQ_PM2 >= 100 or IAQ_PM10 >= 100 or IAQ_ovr >=100:
        print("Unhealthy")
    # If below both conditions, "Healthy" PM condition met
    else:
        print("Healthy")
