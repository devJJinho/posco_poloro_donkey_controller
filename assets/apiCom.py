import requests

class apiCommunication:
    def __init__(self,url):
        self.URL=url
    
    def get(self,index):
        r=requests.get(url=self.URL+str(index),params=None)
        if r==None:
            return None
        data=r.json()
        return data
    
    def put(self,index,status,prePoint,dest):
        DATA={
            "index":index,
            "status":status,
            "destPoint":dest,
            "prePoint":prePoint
        }
        r=requests.put(url=self.URL,data=DATA)



