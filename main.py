"""
HOW THIS CODE IS SUPPOSED  TO WORK

When IR_1 is high,camera 1 takes picture of the car and the ultrasonic sensors 1 and 2 calculate the time
When IR_2 is High,camera 1 takes picture of the car and the ultrasonic sensors 3 and 4 calculate the time

- Run 'sudo apt-get install v4l-utils' to allow you get the list of cameras plugged into the rasberry pi
- Run 'v4l2-ctl --list-devices' to see the list of cameras

"""

from timeit import default_timer as timer
import time
from datetime import timedelta
import RPi.GPIO as GPIO
import requests
import pygame
import pygame.camera
import glob
import os
import base64
import json
from time import sleep

fixed_time = 0.99
fixed_distance = 11 # This will be calculated to fit the length used for the body of the vehicle

# Initialize camera
pygame.init()
pygame.camera.init()

# image pixel size
width, height = 320, 240

# camera
cam_1 = pygame.camera.Camera("/dev/video2", (width, height))
cam_2 = pygame.camera.Camera("/dev/video0", (width, height))

window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
window1 = pygame.display.set_mode((width, height), pygame.RESIZABLE)

# start cameras
cam_1.start()
cam_2.start()

#  This allows us use the numbers printed on the board to refrence the pin to be used.
GPIO.setmode(GPIO.BCM)

# GPIO pin setup
GPIO.setwarnings(False)


#  Initializing IR sensors one and two
GPIO.setmode(GPIO.BCM)

ir_2, ir_1, ir_3, ir_4 = 2, 3, 4, 17

GPIO.setup(ir_1, GPIO.IN)
GPIO.setup(ir_2, GPIO.IN)
GPIO.setup(ir_3, GPIO.IN)
GPIO.setup(ir_4, GPIO.IN)



def incoming_traffic(time, image):
    
    window.blit(image, (0, 0))
    image = pygame.image.save(window, "left/image.jpg")

    speed = fixed_distance / time

    if time > fixed_time:
        is_speeding = False
        os.remove("/home/pi/Desktop/Rasberry_Pi-code/left/image.jpg")
        

    if time < fixed_time:
        url = "https://road-traffic-offender.herokuapp.com/file/upload/"
        payload ={"speed": int(speed), "is_speeding": True}
        files = [("image", ("image.jpg", open("/home/pi/Desktop/Rasberry_Pi-code/left/image.jpg", "rb"), "image/jpg"))]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files = files)
        print(response.content)
        if response.status_code == 201:
            os.remove("/home/pi/Desktop/Rasberry_Pi-code/left/image.jpg")


def outgoing_traffic(time, image):
    #  This is where the command for taking pictures will seat . The name of the picture will be the speed
    
    window.blit(image, (0, 0))

    pygame.image.save(window, "right/image2.jpg")

    speed = fixed_distance / time


    if time > fixed_time:
        is_speeding = False
        removing_files = glob.glob("right/image2.jpg")
        for i in removing_files:
            os.remove(i)
        
        

    if time < fixed_time:

        url = "https://road-traffic-offender.herokuapp.com/file/upload/"

        payload ={"speed": int(speed), "is_speeding": True}
        files = [("image", ("image2.jpg", open("/home/pi/Desktop/Rasberry_Pi-code/right/image2.jpg", "rb"), "image/jpg"))]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files = files)

        print(response.content)
        if response.status_code == 201:
            os.remove("/home/pi/Desktop/Rasberry_Pi-code/right/image2.jpg")





while True:
    state= GPIO.input(ir_1)
    state2 = GPIO.input(ir_2)

    if state == 0:
        image = cam_1.get_image()
        start = timer()
        state = 1

		
        try:
            state3 = GPIO.input(ir_3)
            result = 1
            while  state3 == result:
                state3 = GPIO.input(ir_3)
            stop = timer()
            state3 = 2

            time = float(timedelta(seconds=stop - start).total_seconds())  
            incoming_traffic(time, image)

            sleep(.001)
        except:
            continue
	
	

    elif state2 == 0:
        image = cam_2.get_image()
        start = timer()

        state2 = 1
        try:
            state4 = GPIO.input(ir_4)
            result = 1
            while  state4 == result:
                state4 = GPIO.input(ir_4)
            stop = timer()
            state3 = 2
 
            time = float(timedelta(seconds=stop - start).total_seconds())  
            outgoing_traffic(time, image)
            sleep(.001)
        except:
            continue
	
GPIO.cleanup()
