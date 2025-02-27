import RPi.GPIO as GPIO
import time

led = 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)
    
while True:
    GPIO.output(led, True)
    time.sleep(1)
    GPIO.output(led, False)
    time.sleep(1)