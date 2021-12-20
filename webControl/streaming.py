HOSTING_IP='192.168.0.236'
HOSTING_PORT='9998'

import socket_server as server
import motor_control.motor as motor
import json
import base64
import cv2

class webControl(server.socket_server):
    def __init__(self,IP,PORT):
        server.socket_server.__init__(self,IP,PORT)
        self.motorControl=motor.motorControl()
        # self.cap=cv2.VideoCapture("nvarguscamerasrc ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)
        self.cap=cv2.VideoCapture('/dev/video1')

        # self.cap=cv2.VideoCapture(0,cv2.)
        print("1")
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        print("2")
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,720)
        print("3")

        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]    
        print("init_done")

    def updateMotor(self,data):
        data=json.loads(data)
        print(data)
        if data['dir']=='l':
            self.motorControl.goLeft(20)
        elif data['dir']=='r':
            self.motorControl.goRight(30)
        elif data['dir']=='c':
            self.motorControl.cali()
        data
        self.motorControl.setDefSpeed(data['def_speed'])
        speed=data['speed']
        if speed==0:
            self.motorControl.stop()
        else:
            self.motorControl.setSpeed(speed)
    
    def getImageData(self):
        _, frame = self.cap.read()
        frame=cv2.resize(frame,(640,360))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame=cv2.flip(frame,1)
        _, frame = cv2.imencode('.jpeg', frame)
        b64data = base64.b64encode(frame)
        return b64data

    async def accept(self,websocket,a):
        print("Client Connected")
        await websocket.send(self.getImageData())
        while True:
            data=await websocket.recv()
            # print(data)
            self.updateMotor(data)
            # time.sleep(0.1)
            await websocket.send(self.getImageData())

aa=webControl(HOSTING_IP,HOSTING_PORT)
aa.run()
            
