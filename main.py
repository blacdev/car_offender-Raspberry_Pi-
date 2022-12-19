"""
HOW THIS CODE IS SUPPOSED  TO WORK

When IR_1 is high,camera 1 takes picture of the car and the ultrasonic sensors 1 and 2 calculate the time
When IR_2 is High,camera 1 takes picture of the car and the ultrasonic sensors 3 and 4 calculate the time

- Run 'sudo apt-get install v4l-utils' to allow you get the list of cameras plugged into the rasberry pi
- Run 'v4l2-ctl --list-devices' to see the list of cameras

"""

from timeit import default_timer as timer

from datetime import timedelta
import RPi.GPIO as GPIO
import requests
import cv2
from uuid import uuid4
import os
from dotenv import load_dotenv
from decouple import config
from time import sleep

from app_utils.camera import STREAMING_URL


os.system("sudo ifconfig eth0 192.168.1.65 netmask 255.255.255.0")
os.system("sudo ip route del default via 192.168.1.1 dev eth0")
fixed_time = float(config("FIXED_TIME"))
fixed_distance = float(config("FIXED_DISTANCE"))
image_path = os.path.realpath(config("IMAGE_PATH"))

if os.path.exists(image_path) is False:
    os.makedirs(image_path)


url = "https://5099-102-89-22-78.eu.ngrok.io/offenders/api/post/"


# generate random image name
def get_image():
    image_name = str(uuid4()) + ".jpg"
    return image_name


#  This allows us use the numbers printed on the board to refrence the pin to be used.
GPIO.setmode(GPIO.BCM)

# GPIO pin setup
#GPIO.setwarnings(False)


#  Initializing IR sensors one and two
GPIO.setmode(GPIO.BCM)

ir_1, ir_2 = 2, 27

GPIO.setup(ir_1, GPIO.IN)
GPIO.setup(ir_2, GPIO.IN)




def traffic(time:float, image_path:str, image_name:str):
    
    print("got here")
    # image = cv2.imwrite("/home/pi/Desktop/Rasberry_Pi-code/images/image.jpg", frame)

    speed = int(float(fixed_distance / time))
    
    print("speed is:", speed)
    if time > fixed_time:
        is_speeding = False
        os.remove(image_path +"/"+ image_name)
        

    elif time < fixed_time:

        print("Vehicle overspeeding!!!")
        
        print("uploading to database...")


        files = [("image", (image_name,open(image_path + "/" + image_name, "rb"), "image/jpeg"))]
        
        headers = {}

        response = requests.post(url + f"{speed}/{True}", headers=headers, files=files)
        print(response.text)


        if response.status_code == 200:
            os.remove(image_path +"/"+ image_name)
            print("Upload complete")


def snapimage(image_name, image_path):
    
    # Initialize camera with cv2 
    cam = cv2.VideoCapture(STREAMING_URL)
    
    #  Read the first frame
    ret, frame = cam.read()
    if ret:
        
        image = image_path +"/" + image_name
        image = cv2.imwrite(image, frame)
        
        cam.release()


# send image path into the function



while True:
    
    state1= GPIO.input(ir_1)
    
    
    if state1 == 0:
        image_name= get_image()
        print("Vehicle detected!")
        print("Capturing...")
        
        image = snapimage(image_name, image_path)
        
        #print("Calculating speed")
        
        start = timer()
        state1 = 1
        

        try:
            state2 = GPIO.input(ir_2)

            result = 1

            while  state2 == result:
                state2 = GPIO.input(ir_2)

            stop = timer()
            
            state2 = 1

            Time = float(timedelta(seconds=stop - start).total_seconds())  
            print(Time)
            traffic(Time, image_path, image_name)

            #sleep(.001)
        except:
            continue
	
	
GPIO.cleanup()
