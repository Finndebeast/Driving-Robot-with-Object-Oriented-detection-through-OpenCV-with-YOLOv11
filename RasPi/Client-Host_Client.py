import socket
import json
import sys
import time
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit


HOST, PORT = "[Local IP of the server]", "[Any port]"

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the PC and send data to validate
sock.connect((HOST, PORT))


# Set variable for motorkit function, it's more efficient because of the character difference and capital letters
kit = MotorKit()

# Defining all functions for controlling the DC Motors, to make things easier later on
class Vehicle:

    def forwards(duration):
        kit.motor3.throttle = 1.0
        kit.motor4.throttle = -1.0
        time.sleep(duration)
        kit.motor3.throttle = 0
        kit.motor4.throttle = 0

    def backwards(duration):
        kit.motor3.throttle = -1.0
        kit.motor4.throttle = 1.0
        time.sleep(duration)
        kit.motor3.throttle = 0
        kit.motor4.throttle = 0

    def turn_left(duration):
        kit.motor4.throttle = -1.0
        time.sleep(duration)
        kit.motor4.throttle = 0

    def turn_right(duration):
        kit.motor3.throttle = 1.0
        time.sleep(duration)
        kit.motor3.throttle = 0

    def spin():
        kit.motor4.throttle = 1.0
        time.sleep(1.9)
        kit.motor4.throttle = 0


Last_Obj = "None"

while True:
    time.sleep(5.0)

    while True:
        # Receive the class/category name from the PC
        class_name = sock.recv(1024).decode("UTF-8")
        print("Received: {}".format(class_name))

        if str(class_name) == "car" and Last_Obj != "car":
            Vehicle.turn_left(0.2)
            Vehicle.turn_right(0.2)
            Vehicle.backwards(0.1)
            break

        elif str(class_name) == "apple" and Last_Obj != "apple":
            Vehicle.forwards(0.5)
            Vehicle.backwards(0.5)
            break

        elif str(class_name) == "bottle" and Last_Obj != "bottle":
            Vehicle.spin()
            break

        else:
            print("No objects were detected")

        Last_Obj = class_name

    Vehicle.turn_left(0.45)
    time.sleep(5.0)

    
