import rules.RulesRun
from rules.GenerateData import *
class _IPackages:
    '''
        规则集合包。
        add: 添加规则集合
        addRule: 对某一个集合添加规则
        delete: 删除规矩集合
        runs:运行
        getError: 获取错误集合
        setError:
    '''
    def __init__(self):
        self._rules={}# eg {tbl:[id:rule,type:rule,...]}
        self.logsObj = None
        self._errors = []
        self.RUN = None #具体执行类
    # def add(self,tbl,rules):
    #     pass


    def addRule(self,tbl,key,rule):
        '''
        :param tbl: 表名
        :param rule: 表的字段规则
        :return:
        '''
        if not isinstance(self._rules.get(tbl),dict):
            self._rules[tbl] = {}
        self._rules[tbl][key] = rule;
        pass

    def delete(self,tbl):
        if self._rules.get(tbl):
            del self._rules[tbl]
        pass

    def runs(self):
        pass;

    def getRules(self):
        return self._rules

    def setLogsObj(self,obj):
        # print(obj)
        self.logsObj = obj
        pass

class APIRPackages(_IPackages):
    def __init__(self):
        super().__init__()
        # self._errors = []
        # self.RUN = None

    def runs(self):
        if self.RUN is None:
            self.RUN = rules.RulesRun.Runs(self._rules)
            self.RUN.setLogsObj(self.logsObj)
        self.RUN.run(self._errors)
    # def addRule(self,tbl, key, rule):
    #     if not isinstance(self._rules.get(tbl),dict):
    #         self._rules[tbl] = {}
    #     self._rules[tbl][key] = rule;

class RPackages(_IPackages):
    def __init__(self):
        super().__init__()
        # self._errors = []
        # self.RUN = None #具体执行类
    # def add(self,tbl,rules={}):
    #     '''
    #         tbl:集合的key eg {tbl:{id:rule,....}}
    #         rules:具体的规则集合
    #     '''
    #     self._rules[tbl] = rules
    def addRule(self,tbl, key, rule):
        '''
            tbl: 集合的key
            key:规则的key
            rule: key的规则
        '''
        # if not isinstance(self._rules.get(tbl),dict):
        #     self._rules[tbl] = {}
        #
        # self._rules[tbl][key] = rule;

    # def delete(self,tbl):
    #     '''
    #         tbl:集合的key
    #     '''
    #     if self._rules.get(tbl):
    #         del self._rules[tbl]

    #运行
    def runs(self):
        if self.RUN is None:
            self.RUN = rules.RulesRun.Runs(self._rules)
            self.RUN.setLogsObj(self.logsObj)
        self.RUN.run(self._errors)
    #停止运行
    def stopRuns(self):
        if self.RUN:
            self.RUN.stopRuns()
        pass

    def setInterval(self,intervalTm):
        '''

        :param intervalTm: 数据插入的时间间隔
        :return:
        '''
        if self.RUN is not None:
            intervalTm = float(intervalTm)
            self.RUN.setIntervalTm(intervalTm)

    def getError(self):
        return self._errors

    def setError(self,error):
        self._errors.append(error)