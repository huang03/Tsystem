from dbs.mysql import Mysql
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
        # self._errors = []

    # def getErrors(self):
    #     return self._errors

    def run(self, errors):
        self.validates(errors)
        dbs = InsertDBRun(self._valids)
        dbs.run()
       # print(self._valids)
        pass
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
                if not keys[key].validate():
                    #if not isinstance(self._errors.get(tbl),dict):
                     #   self._errors[tbl] = {}
                    msg = tbl + ' '+ keys[key].getError()
                    errors.append(msg)
                    isOk = False

            if isOk:
                self._setValids(tbl, keys)
        self._rules = {}
                    #self._errors[tbl][key] = keys[key].getError()



class _IRUN:
    '''
        有效规矩集合的具体操作
    '''
    def __init__(self, tasks):
        '''
            tasks:有效集合
        '''
        self._tasks = tasks

    def run(self):
        '''
            具体执行过程
        '''
        pass

class InsertDBRun(_IRUN):
    '''
        规矩设定的规则，生成数据，插入到数据库中
    '''
    def __init__(self,tasks):
        super().__init__(tasks)
        self.db = Mysql()
    def run(self):
        for i in range(1,5):
            for tbl in self._tasks:

                currRuel = self._tasks[tbl]

                fields = tuple(currRuel.keys())
                values = tuple([currRuel[v].getValue() for v in currRuel])
                params = {
                    'table': tbl,
                    'binds':values,
                    'field':fields
                }
                print(params)
                #print(self.db.add(params,True))
                pass;
        pass