'''
created on May 17, 2019
@author: rajitha 
'''
import time
import threading
import queue
import csv

import queue
import copy
import multiprocessing
import pandas as pd

class SavingThreadMP(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.DataQ = multiprocessing.Queue()
        self.exit = multiprocessing.Event()
        
        
    def run(self):
        while not self.exit.is_set():
            if not self.DataQ.empty():
                # print('got Data')
                self.writeData(self.DataQ.get())
        exit(0)

    def framesToPd(self, kinect_list):
        pos_list = ['x','y','z']
        ori_list = ['w','ox','oy','oz']
        # cols = ['index', 'person', 'Joint', 'x', 'y', 'z', 'w', 'ox', 'oy', 'oz']
        df = pd.DataFrame()
        for i, dic in enumerate(kinect_list):
            pd_dic = {}
            pd_dic['index'] = [i]
            for key in dic.keys():
                if key == 'Position' or key == 'Orientation':
                    if key == 'Position':
                        for val, la in zip(dic[key],pos_list):
                            pd_dic[la] = [val] 
                    if key == 'Orientation':
                        for val, la in zip(dic[key],ori_list):
                            pd_dic[la] = [val] 
                else:
                    pd_dic[key] = [dic[key]]
            # print(pd_dic)
            # print(pd.DataFrame(pd_dic))
            df = df.append(pd.DataFrame(pd_dic))
        return df
        
    def writeData(self, data):
        self.framesToPd(data['data']).to_csv(data['filename'], encoding='utf-8', index=False)
        # self.framesToPd(data['data']).to_excel(data['filename'], encoding='utf-8', index=False)
        print('kinect data written to the disk')
    
    def shutdown(self):
        print ("Shutdown of writer process initiated")
        self.exit.set()
        exit(0)
