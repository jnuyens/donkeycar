import RPi.GPIO as GPIO
import time
from datetime import datetime
from datetime import timedelta
import stat, os
import sys

GPIO.setmode(GPIO.BCM)
# accoustic sensor Right
# pin 16 is GPIO 23 
# pin 18 is GPIO 24
# accoustic sensor Left
# pin 15 is GPIO 22
# pin 18 is GPIO 10
TRIG_RIGHT = 23
ECHO_RIGHT = 24
TRIG_LEFT = 22
ECHO_LEFT = 10

GPIO.setup(TRIG_RIGHT,GPIO.OUT)
GPIO.setup(ECHO_RIGHT,GPIO.IN)
GPIO.setup(TRIG_LEFT,GPIO.OUT)
GPIO.setup(ECHO_LEFT,GPIO.IN)

GPIO.output(TRIG_RIGHT, False)
GPIO.output(TRIG_LEFT, False)
print "Waiting For Sensors To Settle"
time.sleep(2)
 
# typical numbers: pulse_end:  1541030536.43 pulse_start:  1541030536.42 pulse_duration:  0.00630187988281 for a Distance: 54.04 cm
max_pulse_duration = 0.050 #pulse duration is distance times 2 divided by 17150 
print "Max pulse time is: ", max_pulse_duration

previousdistance_right=1000
previousdistance_left=1000
def measuredistance(side):
    if side == "left":
        TRIG=TRIG_LEFT
        ECHO=ECHO_LEFT
    else:
        TRIG=TRIG_RIGHT
        ECHO=ECHO_RIGHT
    pulse_start = time.time()
    pulse_max = pulse_start + max_pulse_duration
    #print "Pulse start: ", pulse_start, "Max pulse duration: ", max_pulse_duration, "Pulse end: ", pulse_max
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    time_not_expired = True
    valid = 0
    #first GPIO.input is 0 till it receives when it turns 1 until the end of the pulse
    while (valid == 0):
        pulse_start = time.time()
        if GPIO.input(ECHO) != 0:
            valid = 1 
        if pulse_start > pulse_max:
            valid = 1
            pulse_end=pulse_max
            time_not_expired = None

    #while GPIO.input(ECHO)==0:
    #pulse_start = time.time()
    if time_not_expired:
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 / 2
    distance = round(distance, 2)
    print "Distance ", side, ": ",distance,"cm"
    #maybe discard too big changes in distance - not implemented
    return distance

while True:
    time.sleep(0.1)
    distance_left = measuredistance("left")
    time.sleep(0.1)
    distance_right = measuredistance("right")

GPIO.cleanup()
