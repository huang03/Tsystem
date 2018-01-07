
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
        threading.Thread(target=self.doTask()).start()
    def doTask(self):
        for obj in self._RUNLIST:
            threading.Thread(target=self.execute, args=(obj,)).start()
    def execute(self,runObj):
        pass
        # self.currThreadCount += 1
        while(True):
            runObj.run()
            time.sleep(1)
            print('aaaa');
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