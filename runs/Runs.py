
from runs.IRun import IRun
from queue import Queue
import threading
import time
class Runs:
    def __init__(self):
        self._RUNLIST = []
        self.intervalTm = 0.1  # 默认时间间隔
        self.RunThreads = {}  # 线程集合，一个表一个线程  {table:Thread}
        self.maxThread = 20;
        self.currThreadCount = 0;
        # self.RunThreadsLog = {}  # 记录表是否生成了线程对象，避免重复生成
    def addRunObj(self,runObj):#runObj  为 IRUN 对象，及 子类对象
        self._RUNLIST.append(runObj)
        # if not self._RUNLIST.get(key):
        #     self._RUNLIST[key] = runObj
        # pass
    # def addObjTask(self,key,):
    #     pass
    def clear(self):
        self.stop()
        self._RUNLIST = [];
    def stop(self):
        pass
    def setInterval(self,tm):
        self.intervalTm = tm
    def autoLoadingLogs(self,logObj):
        pass
    def run(self):
        # index = 20;
        taskQueue = Queue(1000)
        print(111)
        while(True):
            # rlen = len(self._RUNLIST)
            for obj in self._RUNLIST:
                # print(obj)
                taskQueue.put(obj)

            while not taskQueue.empty():
                if self.currThreadCount< self.maxThread:
                    threading.Thread(target=self.execute, args=(taskQueue.get(),)).start()

                else:
                    time.sleep(0.5)
            time.sleep(2)
            # time.sleep(1)
            pass
            # for
            # taskQueue = Queue.Queue()
        # if self
        # isinstance()
        pass
    def execute(self,runObj):
        self.currThreadCount += 1
        runObj.run()
        print('aaaa');
        self.currThreadCount -= 1;
    pass

if __name__ == '__main__':
    R = Runs()
    R.addRunObj(1)
    R.addRunObj(2)
    R.addRunObj(3)
    R.addRunObj(4)
    R.addRunObj(5)
    R.run()


    pass