
import threading
import time
from logs.InsertLog import InsertLog
class Runs:
    def __init__(self,logParent=False):
        self._RUNLIST = []
        self._intervalTm = 0.1  # 默认时间间隔
        self.runFlag = {}
        self.LogOper = InsertLog(logParent)
       # self._batchNum = 10

    #设置任务执行
    def setRunFlag(self,key):
        self.LogOper.add(key)
        self.LogOper.update(key,status="执行中")
        self.runFlag[key] = True

    #停止任务
    def stopTask(self,key):
        self.LogOper.update(key, status="停止")
        self.runFlag[key] = False

    #移除任务
    def removeTask(self,key):
        self.LogOper.update(key, status="删除")
        del self.runFlag[key]

    #判断任务是否已经存在，如果存在直接开始
    def isExistRunObj(self,key):
        if self.runFlag.get(key) is not None:
            self.runFlag[key] = True
            return True
        else:
            False
    #添加任务
    def addRunObj(self,key,runObj):#runObj  为 IRUN 对象，及 子类对象
        self.setRunFlag(key);
        tmpThread = threading.Thread(target=self.execute,name=key, args=(key,runObj))
        tmpThread.start();

    def setInterval(self,tm):
        if tm<0:
            tm = 0.1
        self._intervalTm = tm

    # def autoLoadingLogs(self,logObj):
    #     pass

    def execute(self,key,runObj):
        pass
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
            self.LogOper.update(key, execute_ct=runObj.getExecuteNum(), total=runObj.getTotal())
            time.sleep(self._intervalTm)
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