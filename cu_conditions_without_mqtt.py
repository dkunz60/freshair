import time

connection_status = True
new_data = False
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

while connection_status == True:
    
    # Wait for data input
    while user_input == False:
        data = input("Enter data string: ")
            
        # Parse PM2.5 data
        parse_2 = data.split(start_2)
        if len(parse_2) > 1:
            PM2_str = parse_2[1].split(end_2)[0]
            print(PM2_str)
            # Try to convert string to int type
            try:
                IAQ_PM2 = int(PM2_str)
            # If error, something is wrong with entry
            except ValueError:
                print("Invalid data entry")
                pass          

        # Parse PM10 data
        parse_10 = data.split(start_10)
        if len(parse_10) > 1:
            PM10_str = parse_10[1].split(end_10)[0]
            print(PM10_str)
            # Try to convert string to int type
            try:
                IAQ_PM10 = int(PM10_str)
            # If error, something is wrong with entry
            except ValueError:
                print("Invalid data entry")
                pass
            
        # Parse Overall PM data
        parse_ovr = data.split(start_ovr)
        if len(parse_ovr) > 1:
            ovr_str = parse_ovr[1].split(end_ovr)[0]
            print(ovr_str)
            # Try to convert string to int type
            try:
                IAQ_ovr = int(ovr_str)
            # If error, something is wrong with entry
            except ValueError:
                print("Invalid data entry")
                pass
        
        # If all data is still zero, something is wrong, ask for data again
        if IAQ_ovr == 0 and IAQ_PM2 == 0 and IAQ_PM10 == 0:
            print("Invalid data entry")
        # Else, data is good, strings were parsed, continue
        else:
            new_data = True
            user_input = True
                   
        
    while new_data == True:
        time.sleep(0.5)
        # If over/equal to conditions below, "Dangerous" PM condition met (via OSHA 1910.1000)
        if IAQ_PM2 >= 55 or IAQ_PM10 >= 255 or IAQ_ovr >=255:
            print("Dangerous")
            new_data = False
            user_input = False
        # If under "Dangerous" threshold and over/equal to conditions below, "Unhealthy" PM condition met (via OSHA 1910.1000)
        elif IAQ_PM2 >= 35 or IAQ_PM10 >= 155 or IAQ_ovr >=155:
            print("Unhealthy")
            new_data = False
            user_input = False
        # If below both conditions, "Healthy" PM condition met (via OSHA 1910.1000)
        else:
            print("Healthy")
            new_data = False
            user_input = False
