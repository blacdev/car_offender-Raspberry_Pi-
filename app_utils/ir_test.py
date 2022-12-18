import RPi.GPIO as GPIO

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



print("script starting")

while True:
	state1= GPIO.input(ir_1)
	state2 = GPIO.input(ir_2)
	state3 = GPIO.input(ir_3)
	state4 = GPIO.input(ir_4)
	
	if state1 == 0:
		print("state 1 high")
	
	if state2 == 0:
		print("state 2 high")

	if state3 == 0:
		print("state 3 high")

	if state4 == 0:
		print("state 4 high")
