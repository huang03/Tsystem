
from runs.IRun import IRun
from queue import Queue
import threading
import time
class Runs:
    def __init__(self):
        self._RUNLIST = []
        self._intervalTm = 0.1  # 默认时间间隔
        self.runFlag = {}
       # self._batchNum = 10


    def setAddLog(self,key):
        self.runFlag[key] = True

    def stopTask(self,key):
        self.runFlag[key] = False

    def removeTask(self,key):
        del self.runFlag[key]

    def isExistRunObj(self,key):
        if self.runFlag.get(key):
            return True;
        else:
            False;

    def addRunObj(self,key,runObj):#runObj  为 IRUN 对象，及 子类对象
        self.setAddLog(key);
        tmpThread = threading.Thread(target=self.execute,name=key, args=(key,runObj))
        tmpThread.start();
    # def clear(self):
    #     self.stop()
    #     self._RUNLIST = [];
    # def stop(self):
    #     pass
    def setInterval(self,tm):
        if tm<0:
            tm = 0.1
        self._intervalTm = tm
    #def setBatchNum(self,num):

        #self._batchNum = num
    def autoLoadingLogs(self,logObj):
        pass
    # def run(self):
    #     threading.Thread(target=self.doTask()).start()
    # def doTask(self):
    #     pass
        # for obj in self._RUNLIST:
        #     threading.Thread(target=self.execute, args=(obj,)).start()
    def execute(self,key,runObj):
        pass
        # self.currThreadCount += 1
        while(True):
            if self.runFlag.get(key) is None:
                print('remove')
                break;
            elif self.runFlag.get(key) is False:
                print('STOP')
                time.sleep(1)
                continue
            if runObj.isFinish():
                break
            runObj.run()
           # print(self._intervalTm)
            time.sleep(self._intervalTm)
           # print('aaaa1');
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