import Commans
from runs.IRun import IRun
from dbs.MysqlC import MysqlC
from rules2.DB_VarcharRule import VarcharRule

class DBRun(IRun):
    def __init__(self,DB):
        super().__init__(DB)
        self._batchNum = 10
        self._totalNum = 0
        self._executeNum = 0
        self._params = {}

    #获取执行次数
    def getExecuteNum(self):
        return self._executeNum;
    #获取插入总数
    def getTotal(self):
        return self._executeNum*self._batchNum

    def addTaskParams(self,tbl):
        self._params = {'tbl':tbl}

    def setTotal(self,num):
        self._totalNum = num

    def setBatchNum(self,num):
        if type(1) != type(num):
            return False
        if num<1:
            num = 1
        elif num>200:
            num = 200
        self._batchNum = num;
        print(num);
    def isFinish(self):
        if self._totalNum != 0 and self._executeNum > self._totalNum:
            return True
        return False
    def run(self):
        self._fields = tuple(self._rules)
        try:


            #print(self._rules)
            values = []
            # print(self._batchNum)
            for i in range (0,self._batchNum):
               values.append(tuple(self._rules[v].getValue() for v in self._fields))

            values = tuple(values);
            #return False;
            params = {
                'table': self._params['tbl'],
                'binds': values,
                'field': self._fields
            }
            # print(params)
            if not self._operator.addBatch(params):
                self._setError(self._operator.getError())
            self._executeNum +=1
            print('executeNum %s'%self._executeNum)
            # print(self._params['tbl']);

        except Exception as E:
            self._setError(str(E))
            print('DB Run 38')
            print(E)
        pass

if __name__ == '__main__':
    # c=Commans.Comman()
    # c.getConfig()
    RUN = DBRun(MysqlC())
    varOBJ = VarcharRule({"end": 1000, "step": 2, "start": 1, "prefix": "XXX"})
    RUN.addTaskParams('liv_dog_info')
    RUN.addTask('context',varOBJ)
    RUN.run()
    # {"context": {"end": 1000, "step": 2, "start": 1, "prefix": "XXX"}}
