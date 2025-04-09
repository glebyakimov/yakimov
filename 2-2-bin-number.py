import RPi.GPIO as GPIO
import time

dac =  [26,19,13,6,5,11,9,10]


GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

numbers = [255, 127, 64, 32, 5, 0 , 256]

for i in range(7):
    our_number = numbers[i]%256
    str = bin(our_number)[2:]
    number = [0,0,0,0,0,0,0,0]
    for i in range(len(str)):
        if(str[len(str) - i - 1] == '1'):
            number[7-i] = 1
    GPIO.output(dac, number)
    time.sleep(10)

GPIO.output(dac, 0)
GPIO.cleanup()
