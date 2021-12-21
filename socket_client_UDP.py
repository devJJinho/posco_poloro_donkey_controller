import cv2
import assets.motor as motor
from assets.apiCom import apiCommunication as API
import json
import base64
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
        speed=data['speed']
        if speed==0:
            self.mc.stop()
            self.mc.cali()
            # print("Motor Stopped")
            return
        angle=4*int(data['angle'])
        # print(angle)
        if data['dir']=='l':
            self.mc.goLeft(angle)
        elif data['dir']=='r':
            self.mc.goRight(angle)
        elif data['dir']=='c':
            self.mc.cali()
        self.mc.setDefSpeed(data['def_speed'])
        self.mc.setSpeed(speed)
        # print("Motor updated")

###########################################################

class HandleImage:
    def __init__(self):
        print(1)
        self.deviceIndex=1
        if self.deviceIndex==0:
            self.cap=cv2.VideoCapture("nvarguscamerasrc ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)
            self.cap.set(3, 640)  # Set horizontal resolution
            self.cap.set(4, 360)  # Set vertical resolution

        elif self.deviceIndex==1:
            self.cap=cv2.VideoCapture('/dev/video1')
            # self.cap=cv2.VideoCapture(1)

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,360)
        print(2)
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]   
        print("Image init done")
 
    def getImageData(self):
        _, frame = self.cap.read()
        frame=cv2.resize(frame,(640,360))
        if self.deviceIndex==0:
            frame=cv2.flip(frame,0)
            frame=cv2.flip(frame,1)
        # frame=frame[:200,:,:]
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif self.deviceIndex==1:
            pass
        d=frame.flatten()
        s=d.tostring()

        return s


class donkeyParams:
    def __init__(self,index):
        self.steerData=None
        self.index=index
        self.prePoint=None
        self.desPoint=None
        self.status=True

    def setSteerData(self,data):
        self.steerData=data
    
    def getSteerData(self):
        return self.steerData
    
    def getIndex(self):
        return self.index
    
    def setPrePoint(self,point):
        self.prePoint=point
    
    def getPrePoint(self):
        return self.prePoint
    
    def setDesPoint(self,point):
        self.desPoint=point
    
    def getDesPoint(self):
        return self.desPoint
    
    def setStatus(self, value):
        self.status=value
    
    def getStatus(self):
        return self.status

############################################################

class ClientSocket:
    def __init__(self, ip, port):
        self.UDP_SERVER_IP = ip
        self.UDP_SERVER_PORT = port
        self.cap=HandleImage()
        self.motor=UpdateMotor()
        self.params=donkeyParams(0)
        self.api=API("http://141.223.140.53:9666/cars/")

        time.sleep(1)
        self.connectServer()

        self.receiveThread = threading.Thread(target=self.receiveSteerData)
        self.sendThread=threading.Thread(target=self.sendImages)
        self.orderListenThread=threading.Thread(target=self.listenOrder)
        self.vehicleControl=threading.Thread(target=self.donkeyControl)

        self.receiveThread.start()
        self.sendThread.start()
        self.orderListenThread.start()
        self.vehicleControl.start()

    def connectServer(self):
            self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("UDP Socket initialized")

    def sendImages(self):
        # try:
        while True:
            frame=self.cap.getImageData()
            for i in range(15):
                self.sock.sendto(bytes([i])+frame[i*46080:(i+1)*46080],(self.UDP_SERVER_IP,self.UDP_SERVER_PORT))
            time.sleep(0.04)

        # except Exception as e:
            # self.handleError(e)

    def receiveSteerData(self):
        # try:
        while True:
            data,_= self.sock.recvfrom(64)
            data = data.decode('utf-8')
            data=json.loads(data)
            # print(data)
            self.params.setSteerData(data)
            # self.motor.updateSteer(data)

        # except Exception as e:
            # self.handleError(e)

    def listenOrder(self):
        try:
            while True:
                index=self.params.getIndex()
                if index==None:
                    continue
                res=self.api.get(index)
                if res==None:
                    continue
                print(res)
                self.params.setPrePoint(res['prePoint'])
                self.params.setDesPoint(res['destPoint'])
                self.params.setStatus(res['status'])
                time.sleep(3)
        except:
            self.orderListenThread.start()


    def donkeyControl(self):
        while True:
            STOP_DATA={"speed":0,"angle":None,"def_speed":None,"dir":None}
            if not self.params.getStatus():
                self.motor.updateSteer(STOP_DATA)
                continue
            if self.params.prePoint==self.params.desPoint:
                self.params.setStatus(False)
                continue
            if self.params.getSteerData()==None:
                continue
            self.motor.updateSteer(self.params.getSteerData())
            time.sleep(0.1)

    def handleError(self,e):
        print(e)
        self.sock.close()
        sys.exit()

def main():
    UDP_IP_sm = '192.168.0.3'
    UDP_IP_mi= '141.223.140.52'
    UDP_IP_jinho='141.223.140.53'
    UDP_PORT = 9667
    # ClientSocket(TCP_IP_jinho,TCP_PORT)
    ClientSocket(UDP_IP_jinho,UDP_PORT)

main()
