import random
import ibmiotf.application
import ibmiotf.device
from time import sleep
import sys




#Provide your IBM Watson Device Credentials
organization = "zf801i"
deviceType = "bharathi"
deviceId = "bharathi123"
authMethod = "token"
authToken = "123456789"




def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data['command'])
    status=cmd.data['command']
    if status=="lighton":
        print ("led is on")
    else :
        print ("led is off")
   
    #print(cmd)
    
        


try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

#Connecting to IBM watson
deviceCli.connect()

while True:
    
     #Getting values from sensors

     temp_sensor = round( random.uniform(0,80),2)
     PH_sensor = round(random.uniform(1,14),3)
     camera = ["Detected","Not Detected","Not Detected","Not Detected","Not Detected","Not Detected",]
     camera_reading = random.choice(camera)
     flame = ["Detected","Not Detected","Not Detected","Not Detected","Not Detected","Not Detected",]
     flame_reading = random.choice(flame)
     moist_level = round(random.uniform(0,100),2)
     water_level = round(random.uniform(0,30),2)
    
     #storing the sensor data to send in json format to cloud
     
     temp_data = { 'Temperature' : temp_sensor }
     PH_data = { 'PH Level' : PH_sensor }
     camera_data = { 'Animal attack' : camera_reading}
     flame_data = { 'Flame' : flame_reading }
     moist_data = { 'Moisture Level' : moist_level}
     water_data = { 'Water Level' : water_level}



     #print data
   
     def myOnPublishCallback():
             print ("   ............................publish ok.............................   ")
             print ("Published Temperature = %s C" % temp_sensor,  "to IBM Watson")
             print ("Published PH Level = %s" % PH_sensor,  "to IBM Watson")
             print ("Published Animal attack %s " % camera_reading,  "to IBM Watson")
             print ("Published Flame %s " % flame_reading,  "to IBM Watson")
             print ("Published Moisture Level = %s " % moist_level,  "to IBM Watson")
             print ("Published Water Level = %s cm" % water_level,  "to IBM Watson")
             print ("")    
         
     success = deviceCli.publishEvent("Temperature sensor", "json", temp_data, qos=0)
     success = deviceCli.publishEvent("PH sensor", "json", PH_data, qos=0)
     success = deviceCli.publishEvent("camera", "json", camera_data, qos=0)
     success = deviceCli.publishEvent("Flame sensor", "json", flame_data, qos=0)
     success = deviceCli.publishEvent("Moisture sensor", "json", moist_data, qos=0)
     success = deviceCli.publishEvent("Water sensor", "json", water_data, qos=0, on_publish=myOnPublishCallback)
     sleep(5)
     
     if (temp_sensor > 35):
         success = deviceCli.publishEvent("Alert1", "json",{ 'alert1' : "Temperature(%s) is high, sprinkerlers are turned ON" %temp_sensor } , qos=0)
         print( 'alert1 : ',  "Temperature(%s) is high, sprinkerlers are turned ON" %temp_sensor)
         print("")
         
     if (PH_sensor > 7.5 or PH_sensor < 5.5):
         success = deviceCli.publishEvent("Alert2", "json",{ 'alert2' : "Fertilizer PH level(%s) is not safe,use other fertilizer" %PH_sensor } , qos=0)
         print('alert2 : ' , "Fertilizer PH level(%s) is not safe,use other fertilizer" %PH_sensor)
         print("")
         
     if (camera_reading == "Detected"):
        success = deviceCli.publishEvent("Alert3", "json", { 'alert3' : "Animal attack on crops detected" }, qos=0)
        print('alert3 : ' , "Animal attack on crops detected")
        print("")
        
     if (flame_reading == "Detected"):
         success = deviceCli.publishEvent("Alert4", "json", { 'alert4' : "Flame is detected crops are in danger" }, qos=0)
         print( 'alert4 : ' , "Flame is detected crops are in danger")
         print("")

     if (moist_level < 20):
          success = deviceCli.publishEvent("Alert5", "json", { 'alert5' : "Moisture level(%s) is low, Irrigation started" %moist_level }, qos=0)
          print('alert5 : ' , "Moisture level(%s) is low, Irrigation started" %moist_level )
          print("")

     if (water_level > 20):
          success = deviceCli.publishEvent("Alert6", "json", { 'alert6' : "Water level(%s) is high, so motor is ON to take water out " %water_level }, qos=0)
          print('alert6 : ' , "water level(%s) is high, so motor is ONto take water out " %water_level )
          print("")

     if not success:
          print("Not connected to IBM IOT")
          print("")
          sleep(1)
          
     
     deviceCli.commandCallback = myCommandCallback
     
# Disconnect the device and application from the cloud
deviceCli.disconnect()
