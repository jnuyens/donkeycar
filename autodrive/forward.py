#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x6f)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

# the real thing
myMotorLeft = mh.getMotor(2)
myMotorRight = mh.getMotor(1)
# set the speed to start, from 0 (off) to 255 (max speed)
speed = 200

# set the motors speed 
#myMotorLeft.setSpeed(15)
#myMotorRight.setSpeed(15)

print("\tSpeed up...")
myMotorLeft.run(Adafruit_MotorHAT.FORWARD)
time.sleep(0.01)
myMotorRight.run(Adafruit_MotorHAT.FORWARD)
for i in range(speed):
        myMotorLeft.setSpeed(i)
        time.sleep(0.01)
        myMotorRight.setSpeed(i)
        time.sleep(0.01)

print("\tContinuing...")
time.sleep(4.0)
print("END")
myMotorLeft.run(Adafruit_MotorHAT.RELEASE)
myMotorRight.run(Adafruit_MotorHAT.RELEASE)
time.sleep(1.0)

