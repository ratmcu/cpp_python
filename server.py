# first of all import the socket library 
import socket			 
import time  
# next create a socket object 
s = socket.socket()		 
print ("Socket successfully created")

# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 8080				

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind(('', port))		 
print ("socket binded to %s" %(port) )

# put the socket into listening mode 
s.listen(5)	 
print ("socket is listening")			

# a forever loop until we interrupt it or 
# an error occurs 
# Establish connection with client. 
c, addr = s.accept()	 
print ('Got connection from', addr )
while True: 
    # send a thank you message to the client. 
    try:
        c.send(b'Thank you for connecting') 
    except: 
        print('connection lost waiting for a client')
        c, addr = s.accept()	 
        print ('Got connection from', addr )
    time.sleep(1)
# Close the connection with the client 
c.close() 

