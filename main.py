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


#os.run("sudo ifconfig 192.168.1.65 netmask 255.255.255.0")
fixed_time = config("FIXED_TIME")
fixed_distance = config("FIXED_DISTANCE")
image_path = os.path.realpath(config("IMAGE_PATH"))

if os.path.exists(image_path) is False:
    os.makedirs(image_path)


url = config("URL")



# image pixel size
width, height = 320, 240

# generate random image name
def get_image():
    image_name = str(uuid4()) + ".jpg"
    return image_name

#print(image_path +"/"+ get_image())
#  This allows us use the numbers printed on the board to refrence the pin to be used.
GPIO.setmode(GPIO.BCM)

# GPIO pin setup
GPIO.setwarnings(False)


#  Initializing IR sensors one and two
GPIO.setmode(GPIO.BCM)

ir_2, ir_1, ir_3, ir_4 = 2, 27, 4, 17

GPIO.setup(ir_1, GPIO.IN)
GPIO.setup(ir_2, GPIO.IN)
GPIO.setup(ir_3, GPIO.IN)
GPIO.setup(ir_4, GPIO.IN)




def traffic(time:float, image_path:str, image_name:str):
    

    # image = cv2.imwrite("/home/pi/Desktop/Rasberry_Pi-code/images/image.jpg", frame)

    speed = fixed_distance / time

    if time > fixed_time:
        is_speeding = False
        os.remove(image_path +"/"+ image_name)
        

    elif time < fixed_time:

        url = url

        payload ={"speed": int(speed), "is_speeding": True}

        files = [("image", (image_name, open(image_path +"/"+ image_name, "rb"), image_name))]

        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files = files)

        print(response.content)


        if response.status_code == 201:
            os.remove(image_path +"/"+ image_name)


def snapimage():
    
    # Initialize camera with cv2 
    cam = cv2.VideoCapture(STREAMING_URL)
    
    #  Read the first frame
    ret, frame = cam.read()
    if ret:
        image_path_name = image_path +"/" + get_image()
        image = cv2.imwrite(image_path_name, frame)
        
        cam.release()
        return image_path_name
    return

# send image path into the function



while True:
    


    
    state1= GPIO.input(ir_1)
    state2 = GPIO.input(ir_2)
    
    print(state1)
    if state1 == 0 and state2 == 0:
        
        image = snapimage()
        start = timer()
        state1 = 1
        state2 = 1

		
        try:
            state3 = GPIO.input(ir_3)
            state4 = GPIO.input(ir_4)

            result = 1

            while  state3 == result and state4 == result:
                state3, state4 = GPIO.input(ir_3), GPIO.input(ir_4)

            stop = timer()
            
            state3 = 1
            state4 = 1

            Time = float(timedelta(seconds=stop - start).total_seconds())  
            traffic(Time, image_path, image)

            #sleep(.001)
        except:
            continue
	
	
GPIO.cleanup()
