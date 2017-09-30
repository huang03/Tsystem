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

    def add(self,tbl,rules):
        pass

    def addRule(self,tbl,rule):
        pass

    def delete(self,tbl):
        pass

    def runs(self):
        pass;

    def getRules(self):
        return self._rules

class RPackages(_IPackages):
    def __init__(self):
        super().__init__()
        self._errors = []
    def add(self,tbl,rules={}):
        '''
            tbl:集合的key eg {tbl:{id:rule,....}}
            rules:具体的规则集合
        '''
        self._rules[tbl] = rules
    def addRule(self,tbl, key, rule):
        '''
            tbl: 集合的key
            key:规则的key
            rule: key的规则
        '''
        #print(type(self._rules.get(tbl)))
        if not isinstance(self._rules.get(tbl),dict):
            self._rules[tbl] = {}
        self._rules[tbl][key] = rule;
    def delete(self,tbl):
        '''
            tbl:集合的key
        '''
        if self._rules.get(tbl):
            del self._rules[tbl]

    def runs(self):
        run = rules.RulesRun.Runs(self._rules)
        run.run(self._errors)

    def getError(self):
        return self._errors

    def setError(self,error):
        self._errors.append(error)