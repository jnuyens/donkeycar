#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x6f)

for motorid in range(1,4):
    mh.getMotor(motorid).run(Adafruit_MotorHAT.RELEASE)

time.sleep(1.0)
