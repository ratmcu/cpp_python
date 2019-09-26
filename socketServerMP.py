import time
import multiprocessing
import socket
import json
class SocketServerMP(multiprocessing.Process):
    def __init__(self, port, dataQueue = None):
        multiprocessing.Process.__init__(self)
        self.dataQ = dataQueue
        self.port  = port	
        self.exit = multiprocessing.Event()
    def run(self):
        #try:
        self.sock = socket.socket()		 
        print ("Socket successfully created")		
        self.sock.bind(('', self.port))		 
        print ("socket binded to %s" %(self.port) )
        self.sock.listen(5)	 
        print ("socket is listening")
        c, addr = self.sock.accept()	 
        print ('Got connection from', addr )
        #except:
        #    return
        while not self.exit.is_set():
            while self.dataQ.empty():
                pass
            payload = str.encode(json.dumps(self.dataQ.get()))
            try:
                c.send(payload) 
            except: 
                print('connection lost waiting for a client')
                c, addr = self.sock.accept()	 
                print ('Got connection from', addr )
        c.close()
    def shutdown(self):
        print ("Shutdown of radar process initiated")
        self.exit.set()
