import Adafruit_DHT
import os,sys
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
from urllib.parse import urlparse
import time
from time import sleep
import gpsloc as gps
import psutil# Import Library to access GPIO PIN
import smtplib
from email.message import EmailMessage
Button = 16
GPIO.setmode(GPIO.BCM)    # Consider complete raspberry-pi board
GPIO.setwarnings(False) 
 
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11
 
# Set GPIO sensor is connected to
gpio=4
Buzzer_Pin = 23               # Define PIN for Buzzer
MQ2_Pin = 12
IRP_Pin=14
GPIO.setup(Buzzer_Pin,GPIO.OUT)
GPIO.setup(IRP_Pin,GPIO.IN)
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# Set pin function as output
GPIO.setup(MQ2_Pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)   # Set pin function as input

def on_connect(self, mosq, obj, rc):
        self.subscribe("Fan", 0)
    
def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    # Give 5 second delay

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

    
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    

mqttc = paho.Client()                        # object declaration
# Assign event callbacks
mqttc.on_message = on_message                          # called as callback
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.emqx.io:1883') 
url = urlparse(url_str)
mqttc.connect(url.hostname, url.port)
 


rc = 0
while rc == 0: 
    rc = mqttc.loop()
    # Use read_retry method. This will retry up to 15 times to
    # get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    button_state = GPIO.input(Button)
    print(button_state)
    if button_state==1:
        print("Released")
    else:
        print("Pressed")
        loc=gps.get_loc()
        otp="I am in troble in the location"+str(loc)+" help me "
        msg=EmailMessage()
        msg.set_content("Your Message is :"+ str(otp))
        msg['Subject']='OTP'
        msg['From']="evotingotp4@gmail.com"
        msg['To']="ankitaskashyap@gmail.com"
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login("evotingotp4@gmail.com","xowpojqyiygprhgr")
        s.send_message(msg)
        s.quit()
        
    
    print("Humidity=",humidity)
    print("temperature=",temperature)
    # Reading the DHT11 is very sensitive to timings and occasionally
    # the Pi might fail to get a valid reading. So check if readings are valid.
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        print("GPIO.input(MQ2_Pin)==",GPIO.input(MQ2_Pin))
        if GPIO.input(IRP_Pin) == False or float(temperature)>37:
            print("Fire Detected")
            print("Alarm ON")
            print ("Fire Detected and Alaram ON")
            GPIO.output(Buzzer_Pin,GPIO.HIGH)
            mqttc.publish("object","Some object Detected")
            mqttc.publish("humidity",str(humidity))
            mqttc.publish("Temp",str(temperature))
        else :
            print("No Fire")
            print("Alarm OFF")
            print ("Fire not Detected and Alaram OFF")
            GPIO.output(Buzzer_Pin,GPIO.LOW)   #Buzzer OFF
            mqttc.publish("object","NO Objects Near by")
            mqttc.publish("humidity",str(humidity))
            mqttc.publish("Temp",str(temperature))
            time.sleep(1)
    else:
        print('Failed to get reading. Try again!') 

