from dbs.MysqlC import MysqlC
import threading
import time
class Runs:
    '''
        执行规则，通过设定的规则，根据继承_RUN中类中的具体方式，生成数据，执行具体操作
        _setValids 设置有效集合的元素
        validates  验证rule集合的有效性
        _rules 规则集合 dict   eg {'tbl':{id:rule,name:rule,type:rule}}
    '''
    def __init__(self,rules):
        self._rules = rules
        self._valids = {}
        self.insertRun = None #插入数据的运行类

    #运行
    def run(self, errors):
        if self.insertRun is None:
            self.validates(errors)
            self.insertRun = InsertDBRun(self._valids)
        self.insertRun.run()

    #停止运行
    def stopRuns(self):
        self.insertRun.stopRuns()
    #设置执行频率(插入数据的时间间隔)
    def setIntervalTm(self,tm):
        self.insertRun.setIntervalTm(tm)
    def _setValids(self, key, ele):
        '''
            设置有效集合
                key: eg:tbl1
                ele: eg： {id:rule,nane:rule}
        '''
        self._valids[key] = ele

    def validates(self,errors):
        '''
            验证集合有效性：
                errors:错误集合
        '''
        for tbl in self._rules:
            keys = self._rules[tbl]
            isOk = True
            for key in keys:
                pass
                # 下面代码会产生 AttributeError: 'int' object has no attribute 'isdigit'
                # if not keys[key].validate():
                #     #if not isinstance(self._errors.get(tbl),dict):
                #      #   self._errors[tbl] = {}
                #     msg = tbl + ' '+ keys[key].getError()
                #     errors.append(msg)
                #     isOk = False

            if isOk:
                self._setValids(tbl, keys)
        self._rules = {}
                    #self._errors[tbl][key] = keys[key].getError()


RunThreads = {} #线程集合，一个表一个线程  {table:Thread}
RunThreadsLog = {} #记录表是否生成了线程对象，避免重复生成

class _IRUN:
    '''
        有效规矩集合的具体操作
    '''
    def __init__(self, tasks):
        '''
            tasks:有效集合
        '''
        self._tasks = tasks
        self.isRun = True
        self.runEvent = threading.Event() # 线程控制对象类型
        self.intervalTm = 0.1 #默认时间间隔

    #停止运行
    def stopRuns(self):
        self.runEvent.clear()

    #设置执行频率
    def setIntervalTm(self,tm):
        self.intervalTm = tm

    def run(self):
        '''
            具体执行过程
        '''
        pass

class InsertDBRun(_IRUN):
    '''
        根据设定的规则，生成数据，插入到数据库中
    '''
    def __init__(self,tasks):
        super().__init__(tasks)


    def run(self):
        print(self.isRun)
        self.runEvent.set()
        # self.isRun = True
        global RunThreads
        global RunThreadsLog

        for tbl in self._tasks: #为每个表的规则生成一个线程对象,如果已经生成，跳过
            if not RunThreads.get(tbl):
                RunThreads[tbl] = threading.Thread(target=self.startInsert,args=(tbl,self._tasks[tbl]))


        for tbl in RunThreads:#启动启动所有线程，如果已经开启，跳过
            if not RunThreadsLog.get(tbl):
                RunThreads[tbl].start()
                RunThreadsLog[tbl] = 1 #记录线程已经开启

    def startInsert(self,tbl,task):
        '''
        线程执行函数
        tbl:数据表名称
        task：属性规则集合
        '''
        global  RunThreadsLog
        global  RunThreads
        index = 0;
        db = MysqlC()

        fields = tuple(task.keys())

        #主循环
        while True:
            index +=1
            try:
                values = tuple(task[v].getValue() for v in task)
                params = {
                    'table': tbl,
                    'binds': values,
                    'field': fields
                }
                if not db.add(params):
                    break
                print(tbl+'--'+str(index))
                time.sleep(self.intervalTm)

                if not self.runEvent.isSet(): #判断是否需要要停止循环
                    self.runEvent.wait()

            except Exception as E:
                print('Rules Run 117')
                print(E)
                break
            finally:
                pass
        del RunThreadsLog[tbl] #删除已执行完成的线程
        del RunThreads[tbl]
        pass;
