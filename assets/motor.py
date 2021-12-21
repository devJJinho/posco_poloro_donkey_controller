import time
import board

import adafruit_motor.servo as servo
from adafruit_pca9685 import PCA9685
import threading, time

class motorControl:
    def __init__(self):
        self.i2c = board.I2C()
        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 90
        self.pca.channels[0].duty_cycle=0x0000
        self.servo_power=servo.Servo(self.pca.channels[0])
        self.servo_steer = servo.Servo(self.pca.channels[1])
        self.angle=90    
        self.defSpeed=82
        self.speed=self.defSpeed
        self.t = threading.Thread(target=self.start)
        self.tt=threading.Thread(target=self.setServo)
        self.t.start()
        self.tt.start()

    def setSpeed(self,sd):
        self.speed=self.defSpeed+sd

    def setDefSpeed(self,speed):
        self.defSpeed=speed

    def cali(self):
        self.angle=90
    
    def goLeft(self,dir):
        self.angle=90+dir

    def goRight(self,dir):
        self.angle=90-dir

    # def quit(self):
    #     self.pca.deinit()

    # def go(self):
    #     self.speed=self.defSpeed+1

    def stop(self):
        self.speed=50

    def setServo(self):
        while True:
            self.servo_steer.angle=self.angle
            time.sleep(0.2)

    def start(self):
        while True:
            self.servo_power.angle=self.speed
            time.sleep(0.2)

