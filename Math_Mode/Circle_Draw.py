##Cate Final Working Circle Code ##

###############
# IMPORTS ####
#############

import sys
from typing import Any, Union
sys.path.append('../')
import time
import threading
from pigpio_encoder import Rotary
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import RPi.GPIO as GPIO
import math

#############
# Variables
#############
# Activate pull resistors for limit switches
xMotorBSwitchPin = 17
yMotorBSwitchPin = 5

GPIO.setup(xMotorBSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(yMotorBSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create Motor Object
motor = MotorKit(i2c=board.I2C(), address=0x61)

# Setting GPIO to use Broadcom
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Enable pins for IN1-4 to control step sequence
coil_A_1_pin = 4
coil_A_2_pin = 27
coil_B_1_pin = 23
coil_B_2_pin = 24

# Set GPIO pin states
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# Boolean Variable for faster setting
global faster
faster = False

# Boolean Variable for Z-motor pen setting
global isUp
isUp = True
steps = 15
delay = 0.01

# Mechnaical Bounds of plotters in steps
YMECHBOUND = 1890
XMECHBOUND = 624

# Page boundaries for the 25mm
XLEFTBOUND = 60
XRIGHTBOUND = 530
YTOPBOUND = 5
YBOTTOMBOUND = 1590

# Variables to store x and y position of plotter
global xCoord
xCoord = 0
global yCoord
yCoord = 0
global OLDxCoord
OLDxCoord = 0
global OLDyCoord
OLDyCoord = 0

# Page boundaries & Coord sys for the 25mm
XLEFTBOUND = -530
XRIGHTBOUND = 530
YTOPBOUND = 730
YBOTTOMBOUND = -730

# Graph Origin middle of full paper relative to 0,0
xMid = 0
yMid = 0

## motorswitch

xMotorBSwitch = GPIO.input(xMotorBSwitchPin)

yMotorBSwitch = GPIO.input(yMotorBSwitchPin)

#mm to steps radius
global r
r = 1000
rfloat: float = r * 6.25
global rad
rad = round(rfloat)
radrad = rad * rad

#####################
# Defined Functions
#####################

def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)
    
#pen down function
def pend():
    i = 0
    for i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)
#pen up function
def penup():
    i = 0
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
#move to middle/ origin function
def moveTo_mid():
    i = 0
    j = 0
    for i in range(515):
        motor.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    for j in range(715):
        motor.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
   #MOVE TO INITAL STARTING POINT (RAD,0) 
def moveTo_inital():
    global rad
    i = 0
    for i in range(rad):
        motor.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
#MOVE BACK TO MIDDLE/ORIGIN AFTER DRAWING CIRCLE
def moveTo_Ninital():
    global rad
    i = 0
    for i in range(rad):
        motor.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
 #MOVE FUNCTION FOR DRAWING CIRCLE IN Q1       
def moveTo_q1():
    global xCoord
    global yCoord
    global OLDxCoord
    global OLDyCoord
    i = 0
    j = 0
    motor.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    for j in range(abs(OLDyCoord - yCoord)):
        motor.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    
 
# eqUATION CALCULATION for COORDINATES Q1
def q1():
    global radrad
    global xCoord
    global yCoord
    global OLDxCoord
    global OLDyCoord
    OLDyCoord = yCoord
    yCoord = round(math.sqrt((radrad - (xCoord**2))))
    OLDxCoord = xCoord
    xCoord = xCoord - 1
     #MOVE FUNCTION FOR DRAWING CIRCLE IN Q4 
def moveTo_q4():
    global xCoord
    global yCoord
    global OLDxCoord
    global OLDyCoord
    i = 0
    j = 0
    motor.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    for j in range(abs(OLDyCoord - yCoord)):
        motor.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    
 
## eqUATION CALCULATION for COORDINATES Q1
def q4():
    global radrad
    global xCoord
    global yCoord
    global OLDxCoord
    global OLDyCoord
    OLDyCoord = yCoord
    yCoord = round(math.sqrt((radrad - (xCoord**2))))
    OLDxCoord = xCoord
    xCoord = xCoord - 1
      #MOVE FUNCTION FOR DRAWING CIRCLE IN Q3
def moveTo_q3():
    global xCoord
    global yCoord
    global OLDxCoord
    global OLDyCoord
    i = 0
    j = 0
    motor.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    for j in range(abs(OLDyCoord - yCoord)):
        motor.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    
 
# eqUATION CALCULATION for COORDINATES Q1
def q3():
    global radrad
    global xCoord
    global yCoord
    global OLDxCoord
    global OLDyCoord
    OLDyCoord = yCoord
    yCoord = -round(math.sqrt((radrad - (xCoord**2))))
    OLDxCoord = xCoord
    xCoord = xCoord + 1
    
#  #MOVE FUNCTION FOR DRAWING CIRCLE IN Q2
def moveTo_q2():
    global xCoord
    global yCoord
    global OLDxCoord
    global OLDyCoord
    i = 0
    j = 0
    motor.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    for j in range(abs(OLDyCoord - yCoord)):
        motor.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    
# eqUATION CALCULATION for COORDINATES Q1
def q2():
    global radrad
    global xCoord
    global yCoord
    global OLDxCoord
    global OLDyCoord
    OLDyCoord = yCoord
    yCoord = -round(math.sqrt(abs((radrad - (xCoord**2)))))
    OLDxCoord = xCoord
    xCoord = xCoord + 1
      
#MAIN FUNCTION TO DRAW CIRCLE OF RADIUS R   
def drawcircle():
    moveTo_mid()
    moveTo_inital()
    global OLDxCoord
    OLDxCoord = rad
    global OLDyCoord
    OLDyCoord = 0
    global xCoord
    xCoord = rad
    global yCoord
    yCoord = 0
    pend()
    while xCoord != 0:
        q1()
        moveTo_q1()
    while xCoord != -rad:
        q4()
        moveTo_q4()
    while xCoord != 0:
        q3()
        moveTo_q3()
    while xCoord != rad:
        q2()
        moveTo_q2()
    for i in range(round(rad/10)):
        motor.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    time.sleep(delay)
    penup()
    moveTo_Ninital()
   
   
####################
#IMPLEMENTATION ###
##################
#if __name__ == "__drawcircle__":
drawcircle()
