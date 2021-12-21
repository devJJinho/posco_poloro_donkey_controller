import asyncio;
import websockets;

class socket_server:
        def __init__(self,IP,PORT):
                self.HOSTING_IP=IP
                self.HOSTING_PORT=PORT
        
        async def accept(self,websocket):
                print("연결완료")
                while True:
                        data = await websocket.recv()
                        print("receive : " + data)
                        await websocket.send("echo : " + data)

        def run(self):
                start_server = websockets.serve(self.accept, self.HOSTING_IP, self.HOSTING_PORT)
                asyncio.get_event_loop().run_until_complete(start_server)
                asyncio.get_event_loop().run_forever()
                

