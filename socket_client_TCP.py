import assets.motor as motor
import json
import base64
import cv2
import socket
import sys
import numpy
import time
import threading


class UpdateMotor:
    def __init__(self):
        self.mc=motor.motorControl()
        print("Motor init done")

    def updateSteer(self,data):
        print("motor updated")
        if data['dir']=='l':
            self.mc.goLeft(10)
        elif data['dir']=='r':
            self.mc.goRight(15)
        elif data['dir']=='c':
            self.mc.cali()
        self.mc.setDefSpeed(data['def_speed'])
        speed=data['speed']
        if speed==0:
            self.mc.stop()
        else:
            self.mc.setSpeed(speed)

class HandleImage:
    def __init__(self):
        print(1)
        self.deviceIndex=1  
        if self.deviceIndex==0: #picam
            self.cap=cv2.VideoCapture("nvarguscamerasrc ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)
            self.cap.set(3, 640)  # Set horizontal resolution
            self.cap.set(4, 360)  # Set vertical resolution

        elif self.deviceIndex==1: #webcam
            self.cap=cv2.VideoCapture('/dev/video1')
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,360)        
        print(2)
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]   
        print("Image init done")
 
    def getImageData(self):
        _, frame = self.cap.read()
        frame=cv2.resize(frame,(480,240))
        # frame=frame[:200,:,:]
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame=cv2.flip(frame,0)
        frame=cv2.flip(frame,1)
        _, frame = cv2.imencode('.jpeg', frame)
        data = numpy.array(frame)
        stringData = base64.b64encode(data)
        length = str(len(stringData))
        return length,stringData

############################################################

class ClientSocket:
    def __init__(self, ip, port):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0
        self.cap=HandleImage()
        self.motor=UpdateMotor()
        time.sleep(1)
        print("connecting")
        self.connectServer()
        print("connected")
        self.receiveThread = threading.Thread(target=self.receiveSteerData)
        self.sendThread=threading.Thread(target=self.sendImages)
        self.receiveThread.start()
        self.sendThread.start()
        print("socket Done")

    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0

        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                sys.exit()
            time.sleep(1)
            self.connectServer()
                
    def sendImages(self):
        try:
            while True:
                length,stringData=self.cap.getImageData()
                self.sock.send(length.encode('utf-8').ljust(64))
                self.sock.send(stringData)
                time.sleep(0.15)

        except Exception as e:
            self.handleError(e)

    def receiveSteerData(self):
        try:
            while True:
                data = self.sock.recv(64)
                data = data.decode('utf-8')
                data=json.loads(data)
                print(data)
                self.motor.updateSteer(data)

        except Exception as e:
            self.handleError(e)
    
    def handleError(self,e):
        print(e)
        self.sock.close()
        sys.exit()

def main():
    TCP_IP_sm = '192.168.0.3'
    TCP_IP_mi= '192.168.0.242'
    TCP_IP_jinho='192.168.0.243'
    TCP_PORT = 9667
    ClientSocket(TCP_IP_jinho,TCP_PORT)

main()
