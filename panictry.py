import RPi.GPIO as GPIO
from time import sleep
import gpsloc as gps
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#Set Button and LED pins
import smtplib
from email.message import EmailMessage
Button = 16

#Setup Button and LED
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#flag = 0

while True:
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
        
        
    sleep(1)
    
   