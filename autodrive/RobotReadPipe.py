# Simple two DC motor robot class usage example.
# Author: Tony DiCola
# License: MIT License https://opensource.org/licenses/MIT
import time
import os
import errno

# Import the Robot.py file (must be in the same directory as this file!).
import Robot

# Set the trim offset for each motor (left and right).  This is a value that
# will offset the speed of movement of each motor in order to make them both
# move at the same desired speed.  Because there's no feedback the robot doesn't
# know how fast each motor is spinning and the robot can pull to a side if one
# motor spins faster than the other motor.  To determine the trim values move the
# robot forward slowly (around 100 speed) and watch if it veers to the left or
# right.  If it veers left then the _right_ motor is spinning faster so try
# setting RIGHT_TRIM to a small negative value, like -5, to slow down the right
# motor.  Likewise if it veers right then adjust the _left_ motor trim to a small
# negative value.  Increase or decrease the trim value until the bot moves
# straight forward/backward.
LEFT_TRIM   = 0
RIGHT_TRIM  = 0


# Create an instance of the robot with the specified trim values.
# Not shown are other optional parameters:
#  - addr: The I2C address of the motor HAT, default is 0x60.
#  - left_id: The ID of the left motor, default is 1.
#  - right_id: The ID of the right motor, default is 2.
# You can also set this in Robot.py
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# Now move the robot around!
# Each call below takes two parameters:
#  - speed: The speed of the movement, a value from 0-255.  The higher the value
#           the faster the movement.  You need to start with a value around 100
#           to get enough torque to move the robot.
#  - time (seconds):  Amount of time to perform the movement.  After moving for
#                     this amount of seconds the robot will stop.  This parameter
#                     is optional and if not specified the robot will start moving
#                     forever.

FIFO="/var/run/robotpidirection"
try:
        os.mkfifo(FIFO)
except OSError as oe: 
        if oe.errno != errno.EEXIST:
                    raise
print("Opening FIFO: ",FIFO)
#First we do this to start driving: echo start > robotpidirection 
#then we continue reopening the FIFO to read possible left or right commands

speed=80
timeinterval=0.13
#timeinterval=1
driving=None
#open the fifo in read mode and without buffering
with open(FIFO, "r", 0) as fifo:
    print("FIFO opened")
    while True:
        direction=fifo.read()
        if len(direction)== 0:
            if driving == True:
                robot.forward(speed, timeinterval)   # Move forward at speed 150 for 1 second.
        elif direction == "left\n":
            print("Left")
            robot.left(speed, timeinterval)
        elif direction == "right\n":
            print("Right")
            #this did left motor backward instead of right motor forward
            robot.right(speed, timeinterval)
        elif direction == "start\n":
            print("Start")
            robot.forward(speed, timeinterval)  
            driving=True
            print
        elif direction == "stop\n":
            print("Stop")
            robot.stop()      # Stop the robot from moving.
            driving=None
        else:
            print("Wrong command detected: ", direction)



robot.stop()      # Stop the robot from moving.
