# Import socket module 
import socket                
import time  
import ast
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 27015
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
# while True:
#     pass  
# receive data from the server 
try:
    while True:
        st = s.recv(1024)
        try:
            dic = ast.literal_eval(str(st)[2:-1])
            print(dic)	    
            for key in dic.keys():
                print(key, dic[key] )
        except:
            print('failed to get a dictionary received bytes: {0}\n'.format(str(st)))
        time.sleep(1)
except KeyboardInterrupt:
    s.close()
# close the connection 
s.close()
print('exit')
