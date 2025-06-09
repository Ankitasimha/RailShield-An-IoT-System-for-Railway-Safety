import tensorflow.lite as tflite
#from tflite_runtime.interpreter import Interpreter
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import cv2
import numpy as np
import RPi.GPIO as GPIO
Buzzer_Pin = 23
import time
import gpsloc as gps
import psutil# Import Library to access GPIO PIN
import smtplib
from email.message import EmailMessage
GPIO.setmode(GPIO.BCM)    # Consider complete raspberry-pi board
GPIO.setwarnings(False) 
GPIO.setup(Buzzer_Pin,GPIO.OUT)


interpreter = tflite.Interpreter(model_path='/home/pi/Desktop/RailEmegerency/Firemodel.tflite')
#allocate the tensors
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    #cv2.imshow("Input image",image)
    cv2.imwrite("test.jpg",image)
    image_path='test.jpg'
    img = cv2.imread(image_path)#img = cv2.resize(img,(224,224))
    img = cv2.resize(img,(256,256),cv2.INTER_AREA)
    img= np.expand_dims((img),axis=0).astype(np.float32)
    img= preprocess_input(img)
    
    #Preprocess the image to required size and cast
    input_shape = input_details[0]['shape']
    #input_tensor= np.array(np.expand_dims(img,0), dtype=np.float32)
    input_tensor= np.array(img, dtype=np.float32)
    #print(interpreter.get_input_details())
    input_index = interpreter.get_input_details()[0]['index']
    interpreter.set_tensor(input_index, input_tensor)
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    pred = np.squeeze(output_data)
    class_ind = {'Fire': 0, 'Neutral': 1, 'Smoke': 2}
    highest_pred_loc = np.argmax(pred)
    class_name = class_ind[highest_pred_loc]
    if str(class_name=='Fire'):
        print ("Fire Detected and Alaram ON")
        GPIO.output(Buzzer_Pin,GPIO.HIGH)
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
    else:
        print ("Fire not Detected and Alaram OFF")
        GPIO.output(Buzzer_Pin,GPIO.LOW)   #Buzzer OFF
    
    cv2.putText(image,str(class_name),(30,30),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,255),1)
    
    cv2.imshow("Video feed",image)
    keypress=cv2.waitKey(1)& 0xFF
    if(keypress==ord("q")):
        break
cap.release()
cv2.destroyAllWindows()
    
    
    #print("class_name==",class_name)
