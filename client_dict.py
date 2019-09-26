# Import socket module 
import socket                
import time  
import ast
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 8080                
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
# while True:
#     pass  
# receive data from the server 
while True:
    try:
        print(ast.literal_eval(s.recv(1024).decode("utf-8"))) 
    except:
        pass
    time.sleep(1)
# close the connection 
s.close()
