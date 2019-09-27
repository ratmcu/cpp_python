# Import socket module 
import socket                
import time  
import ast
import os
import queue
from mp_saver import SavingThreadMP


if __name__ == "__main__":
    s = socket.socket()          
    # Define the port on which you want to connect 
    port = 27015
    # connect to the server on local computer 
    s.connect(('127.0.0.1', port)) 
    dic = []
    sp = SavingThreadMP()
    sp.start()
    startTime = time.time()
    root = 'D:\\kinect_data\\'
    dir_name = time.strftime(u"%Y%m%d")
    path = root + dir_name
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        while True:
            st = s.recv(1024)
            try:
                dictt = ast.literal_eval(str(st)[2:-1])
                # print(dictt)
                for key in dictt.keys():
                    # print(key, dictt[key] )
                    pass
                dic.append(dictt)	    
            except:
                print('failed to get a dictionary received bytes: {0}\n'.format(str(st)))
            if time.time() - startTime > 10:
                print('queueing a set of frames')
                timeString = time.strftime(u"%Y%m%d-%H%M%S")
                file_name = path + '\\' + 'kinect_frame_' + timeString + '.csv'
                kinectData = {}
                kinectData['filename'] = file_name
                kinectData['data'] = dic.copy()
                sp.DataQ.put(kinectData)
                startTime = time.time()
            # time.sleep(1)
    except KeyboardInterrupt:
        s.close()
    # close the connection 
    s.close()
    sp.shutdown()
    # sp.join()
    print('exit')
