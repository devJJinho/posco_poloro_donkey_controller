import time
# from board import SCL, SDA
import board
# import busio

import adafruit_motor.servo as servo
# from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
import threading, time

# i2c = busio.I2C(SCL, SDA)
# pca = PCA9685(i2c)
# pca.frequency = 90
# pca.channels[0].duty_cycle=0x0000
# servo_power=servo.Servo(pca.channels[0])
# servo_steer = servo.Servo(pca.channels[1])
# servo_steer.angle=90     


class motorControl:
    def __init__(self):
        self.i2c = board.I2C()
        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 90
        self.pca.channels[0].duty_cycle=0x0000
        self.servo_power=servo.Servo(self.pca.channels[0])
        self.servo_steer = servo.Servo(self.pca.channels[1])
        self.servo_steer.angle=90    
        self.defSpeed=0.55
        self.speed=self.defSpeed
        self.t = threading.Thread(target=self.start)
        self.t.start()

    def setAngle(self,ag):
        self.servo_steer.angle=ag

    def setSpeed(self,sd):
        nSpeed=(self.defSpeed+sd)/1
        self.speed=nSpeed
        print(nSpeed)

    def setDefSpeed(self,speed):
        self.defSpeed=speed

    def cali(self):
        self.servo_steer.angle=90
        time.sleep(0.1)
        self.servo_steer.angle=None

    def goLeft(self,dir):
        dir=int(dir)%21
        self.servo_steer.angle=90+dir
        time.sleep(0.1)
        self.servo_steer.angle=None

    def goRight(self,dir):
        dir=int(dir)%31
        self.servo_steer.angle=90-dir
        time.sleep(0.1)
        self.servo_steer.angle=None

    def quit(self):
        self.pca.deinit()

    def go(self):
        self.speed=self.speed+0.01

    def stop(self):
        self.speed=self.defSpeed

    def start(self):
        while True:
            self.servo_power.fraction=self.speed
            time.sleep(0.1)

