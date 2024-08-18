#import board
import blynklib
#import adafruit_dht
from time import sleep
import matplotlib.pyplot as plt
from datetime import datetime
#import RPi.GPIO as GPIO


#th_sensor = adafruit_dht.DHT11(board.D27)
blynk = blynklib.Blynk("mVkujtgml2vx5D25IT1jQUBOxhgRLnXw", server="blynk.cloud", port=80)
humidity = None
temperature = None
dim = None
try:
    logp = open("log.txt", 'x')
    logp.close()
except:
    print("file is already there")

def log() :
    logp = open("log.txt",'a')
    status = f"{datetime.now().strftime('%Y-%B-%d\t%A %I:%M:%S %p')}\nThe Current Temperature is {temperature}C\n The Current Humidity is {humidity}%\nThe Current Distance in meter is {dim}\n\n"
    logp.write(status)
    logp.close()
    print("logs sent and saved successfully")
    
def updatevariables():
    global humidity, temperature, dim
    humidity = 9
    temperature = 20
    #dim = 
    print (f"Temp= {temperature}C Humidity= {humidity}%")
    
def th_blynk():
    for l in range(5):
        try :
            print("Trying to connect")
            blynk.virtual_write(0, humidity) 
            blynk.virtual_write(1, temperature)
            print('Values Sent to server')
            return
        except RuntimeError as error :
            print (f"Error reading DHT sensor: {error.args}") 
            sleep (2) # Wait before retrying
            print("Sensor failure. Check wiring.")

while True:
    blynk.run()
    updatevariables()
    th_blynk()
    log()
    #plot()
    sleep (2)
