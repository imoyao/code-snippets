import threading
import time


# def writetoTxt(txtFile):
#     id = threading.currentThread().getName()
#     mutex.acquire(1)
#     with open(txtFile, 'a') as f:
#         print "Thread {0} acquire lock".format(id)
#         f.write("write from thread {0} \n".format(id))
#         # time.sleep(3)
#     mutex.release()
#     print "Thread {0} exit".format(id)

class WriteFileThread(threading.Thread):
    def run(self):
        global wf_name, write_data,i
        mutex.acquire(1)
        data = write_data + str(i) + '\n'
        write_f(wf_name, data)
        print(('{name} write text: {data}'.format(name=self.name, data=data)))
        mutex.release()


def write_f(filename, data):
    with open(filename, 'a+') as f:
        f.write(data)


def write_text():
    for i in range(5):
        thr = WriteFileThread()
        thr.setDaemon(True)
        thr.start()
    thr.join()


mutex = threading.Lock()
wf_name = 'wftest.txt'
write_data = 'hello,world'
write_text()
# for i in range(50):
#     myThread = threading.Thread(target=writetoTxt, args=("test.txt",))
#     myThread.start()