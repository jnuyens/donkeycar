import RPi.GPIO as GPIO
import time
from datetime import datetime
from datetime import timedelta
import stat, os
import sys
import random

GPIO.setmode(GPIO.BCM)
# pin 16 is GPIO 23 
# pin 18 is GPIO 24
TRIG = 23 
ECHO = 24

FIFO="/var/run/robotpidirection"
wait=0.25 #time interval for waiting after sending a command
print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)
 
# typical numbers: pulse_end:  1541030536.43 pulse_start:  1541030536.42 pulse_duration:  0.00630187988281 for a Distance: 54.04 cm
max_pulse_duration = 0.050 #pulse duration is distance times 2 divided by 17150 
print "Max pulse time is: ", max_pulse_duration

previousdistance=1000
def measuredistance():
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
            time_expired = None

    #while GPIO.input(ECHO)==0:
    #pulse_start = time.time()
    if time_not_expired:
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150 / 2

    distance = round(distance, 2)

    print "Distance:",distance,"cm"
    #maybe discard too big changes in distance - not implemented
    return distance

def turn(direction):
    """Send the string provided to this function the the fifo
    to steer the robot in the correct direction
    """
    fifo = open(FIFO, "w", 0) #open the file without buffering; hence the 0
    fifo.write(direction)
    fifo.close()
    time.sleep(wait) #ensure the reader process can read it before we write again

#wait for the fifo to be created by RobotReadPipe.py
if not stat.S_ISFIFO(os.stat(FIFO).st_mode):
    print ("Fifo :",FIFO," does not exist - run RobotReadPipe.py first")
    sys.exit(1)


stop_distance=8 #distance in cm at which it will stop to change directions
avoid_distance=20 #distance at which it will start turning to avoid objects

turndirection=random.choice(['right\n', 'left\n'])
print ("Random Turndirection: ", turndirection)
turn("start\n")
while True:
    time.sleep(wait)
    distance = measuredistance()
    while distance < stop_distance:
        print("Distance Alert: ", distance)
        #stop
        turn("stop\n")
        #turn in the randomdirection and measure again
        turn(turndirection)
        prevdistance = distance
        distance = measuredistance()
        if distance > prevdistance:
            #seems a good direction
            #just give it another turn in this direction 
            turn(turndirection)
            turn("start\n")
        else:
            #seemed the wrong direction, invert and turn 2 times in that direction
            #invert turning direction
            if turndirection == "right\n":
                turndirection="left\n"
            else:
                turndirection="right\n"
            turn(turndirection)
            turn(turndirection)
    if distance < avoid_distance:
        #In this case we might be able to still avoid the obstacle without stopping
        print("Turning while driving ", distance)
        #turn in the random direction and see if it gets better, otherwise invert the direction
        previous_distance=distance #should we substract to compensate for the forward motion?
        #turn
        turn(turndirection)
        distance=measuredistance()
        if distance > previous_distance:
            #we must be turning in the right direction
            #turn another time
            turn(turndirection)
            #and randomise the turn direction for next time we get near an obstacle
            turndirection=random.choice(['right\n', 'left\n'])
        else:
            #invert turning direction
            if turndirection == "right\n":
                turndirection="left\n"
            else:
                turndirection="right\n"
            #turn 2 times to compensate for the previous mistake
            turn(turndirection)
            turn(turndirection)
            #keep this turning direction 


GPIO.cleanup()
