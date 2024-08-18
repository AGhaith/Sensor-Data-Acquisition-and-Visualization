import board
import blynklib
import adafruit_dht
from time import sleep
import time
import matplotlib.pyplot as plt
from datetime import datetime
import gpiozero as GPIO
start_time = time.time()
ot=0
try:
    th_sensor = adafruit_dht.DHT11(board.D14)
    blynk = blynklib.Blynk("mVkujtgml2vx5D25IT1jQUBOxhgRLnXw", server="blynk.cloud", port=80)
    humidity = None
    temperature = None
    dim = None
    yaxis1=[]
    yaxis2=[]
    yaxis3=[]
    xaxis=[]
    try:
        logp = open("C:\\Users\\Ahmed\\Documents\\GitHub\\Sensor-Data-Acquisition-and-Visualization\\log.txt", 'x')
        print("there was no previous log file so it has been created")
        logp.close()
    except:
        print("file is already there")

    def log() :
        logp = open("C:\\Users\\Ahmed\\Documents\\GitHub\\Sensor-Data-Acquisition-and-Visualization\\log.txt",'a')
        status = f"{datetime.now().strftime('%Y-%B-%d\t%A %I:%M:%S %p')}\nThe Current Temperature is {temperature}C\nThe Current Humidity is {humidity}%\nThe Current Distance in meter is {dim}\n\n"
        logp.write(status)
        logp.close()
        print("logs sent and saved successfully")
    
    def updatevariables():
        global humidity, temperature, dim, end_time, elapsed_time, start_time, yaxis1, yaxis2, yaxis3, xaxis, ot
        end_time = time.time()
        elapsed_time = end_time - start_time
        xaxis.append(int(ot+elapsed_time))
        ot=int(elapsed_time)
        humidity = th_sensor.humidity
        temperature = th_sensor.temerature
        yaxis1.append(humidity)
        yaxis2.append(temperature)
        yaxis3.append(dim)
        #dim = 
        print (f"Temp = {temperature}C \nHumidity = {humidity}% \nDistance = {dim}%")
    
    def th_blynk():
        for l in range(5):
            try :
                print("Trying to connect")
                blynk.virtual_write(0, humidity) 
                blynk.virtual_write(1, temperature)
                blynk.virtual_write(2, dim)
                print('Values Sent to server')
                return
            except RuntimeError as error :
                print (f"Error reading DHT sensor: {error.args}") 
                sleep (2) # Wait before retrying
                print("Sensor failure. Check wiring.")
    def plot():
        plt.figure()
        plt.plot(xaxis, yaxis1, color='r', label='Humidity')
        plt.plot(xaxis, yaxis2, color='b', label='Temperature')
        plt.plot(xaxis, yaxis3, color='g', label='Distance')
        plt.xlabel('Elapsed Time (seconds)')
        plt.ylabel('Values')
        plt.title('Sensor Data Over Time')
        plt.legend()
        plt.show()  # Display the plot
    while True:
        blynk.run()
        updatevariables()
        th_blynk()
        log()
        sleep (2)

except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    print(xaxis)
    print(yaxis1)
    plot()
