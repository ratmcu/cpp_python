from socketServerMP import SocketServerMP
import multiprocessing
import time
if __name__=='__main__':
    dataQ = multiprocessing.Queue()
    smp = SocketServerMP(8080, dataQ)
    smp.start()
    data = {}
    while smp.is_alive():
        data['time'] = time.strftime(u"%Y%m%d-%H%M%S")
        dataQ.put(data)
        time.sleep(1)
    smp.shutdown()
