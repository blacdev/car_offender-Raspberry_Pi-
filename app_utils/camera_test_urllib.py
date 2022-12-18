import cv2
import RPi.GPIO as GPIO
import datetime
import urllib.request
import numpy as np

camera_url = "http://admin:@fuoye2022@192.168.1.64:554/streaming/channels/1" 

GPIO.setmode(GPIO.BCM)

ir_sensor = 27

GPIO.setup(ir_sensor, GPIO.IN)

while True:
	
	ir_sensor_state = GPIO.input(ir_sensor)
	
	if ir_sensor_state ==0:
		
		with urllib.request.urlopen(camera_url) as url:
			
			image_array = np.asarray(bytearray(url.read()), dtype=np.uint8)
			frame = cv2.imdecode(image_array, -1)
			
			cv2.imwrite('seye.jpg', frame)
			
