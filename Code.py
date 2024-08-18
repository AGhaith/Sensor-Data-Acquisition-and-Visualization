#import board
import blynklib
#import adafruit_dht
from time import sleep
import time
import matplotlib.pyplot as plt
from datetime import datetime
#import RPi.GPIO as GPIO
start_time = time.time()
ot=0
try:
    #th_sensor = adafruit_dht.DHT11(board.D27)
    blynk = blynklib.Blynk("mVkujtgml2vx5D25IT1jQUBOxhgRLnXw", server="blynk.cloud", port=80)
    humidity = None
    temperature = None
    dim = None
    yaxis1=[]
    yaxis2=[]
    yaxis3=[]
    xaxis=[]
    try:
        logp = open("log.txt", 'x')
        print("there was no previous log file so it has been created")
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
        global humidity, temperature, dim, end_time, elapsed_time, start_time, yaxis1, yaxis2, yaxis3, xaxis, ot
        end_time = time.time()
        elapsed_time = end_time - start_time
        xaxis.append(ot+elapsed_time)
        ot=elapsed_time
        humidity = 9
        temperature = 20
        yaxis1.append(humidity)
        yaxis2.append(temperature)
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
    def plot():
        
        plt.plot(xaxis, yaxis1, color='r')
        plt.plot(xaxis, yaxis2, color='r')
        plt.plot(xaxis, yaxis3, color='r')
        plt.show()
    while True:
        blynk.run()
        updatevariables()
        th_blynk()
        log()
        sleep (2)

except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    plot()
