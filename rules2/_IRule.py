from dbs.MysqlC import MysqlC
import math
class _IRule:
    '''
        规则类接口
        validate: 验证规则合法性
        getError
        setError

        getValue:根据规则生成数据

        属性
         _metas:元数据
         _error:错误列表
         _GrtData:生成数据的类
    '''
    def __init__(self,params):
        self.params = params
        self._error = None
        self._currValue = None
        self._currValues = None
    def validate(self):
        pass
    def getError(self):
        return self._error
    def _setError(self,error):
        self._error = error
    #
    # def getMetas(self):
    #     return self.params
    #
    # def setMetas(self,params):
    #     self._metas = params
    #     del params
    def getValue(self):
        if self.params['_TYPE_'] == 'COMMAN':
            return self._getCommanValue()
        elif self.params['_TYPE_'] == 'LIST':
            return self._getListValue()
        elif self.params['_TYPE_'] == 'TABLE':
            return self._getTableValue()
        elif self.params['_TYPE_'] == 'SQL':
            return self._getSqlValue()
        return None
        pass

    def validate(self, type='COMMAN'):

        if type is 'COMMAN':
            return self._validateComman()
        elif type is 'LIST':
            return self._validateList()
        elif type is 'SQL':
            return self._validateSql()
        elif type is 'TABLE':
            return self._validateTable()
        return False;

    def _validateTable(self):
        if self.params.get('table')  == '':
            self._setError('表属性不能为空:格式为：table,propery')
            return False
        tmp = self.params.get('table')
        tmps = tmp.split(',')
        if(len(tmps)<2):
            self._setError('格式为：table,propery')
            return False
        return self._checkTableProperty(tmps[0], tmps[1])
        return True
        pass

    def _validateSql(self):
        if self.params.get('sql')  == '':
            self._setError('请输入正确的SQL语句')
            return False
        try:
            operator = MysqlC()
            result = operator.queryBySql(self.params['sql'])
            return True
        except Exception as E:
            self._setError(str(E))
        return False
        pass

    def _validateList(self):
        if self.params.get('list') == '':
            self._setError('指定列表不能为空')
            return False
        return True
        pass

    def _validateComman(self):
        # RInteger = IntegerRule(self.params)
        # if not self._RInteger.validate():
        #     self._setError(self._RInteger.getError())
        #     return False
        # if not self.params.get('prefix'):
        #     self.params['prefix'] = 'tsys-'
        return True

    def _checkTableProperty(self,table,property):
        try:
            operator = MysqlC()
            sql = "SHOW TABLES LIKE '%s'" % table
            result = operator.queryBySql(sql)
            if (len(result)) < 1:  # 判断表是否存在
                self._setError('数据表 %s 不存在'% table)
                return False
            sql = "show columns from `%s` like '%s' " % (table, property)
            result = operator.queryBySql(sql)
            if len(result) < 1:  # 判断字段是否存在
                self._setError('数据表 %s 不存在 %s' % (table, property))
                return False
            return True
        except Exception as E:
            self._setError(str(E))
        return False

    def _getCommanValue(self):
        return False

    def _getListValue(self):
        if self._currValues is None:
            self._currValues = self.params.get('list').split(',')
            self._len = len(self._currValues)
            self._currValue = 0
        if self._currValue >= self._len:
            self._currValue = 0
        tmp =  self._currValues[self._currValue]
        self._currValue += 1
        return tmp

    def _getTableValue(self):
        try:
            if self._currValues is None:
                self._currValues = self.params.get('table').split(',')
                self._count = 50;
                self.operator = MysqlC()
                sql = 'SELECT COUNT(*) FROM %s' % self._currValues[0];
                self._ct = self.operator.queryScalarBySql(sql)
            offset = math.floor(self._ct * random.random())
            self._currValue = self.operator.queryScalar({
                'table': self._currValues[0],
                'select': (self._currValues[1],),
                'limit': '%s,1'% offset
            })
            self._count -= 1
            if(self._count<1): #重新刷新总数
                sql = 'SELECT COUNT(*) FROM %s' % self._currValues[0];
                self._ct = self.operator.queryScalarBySql(sql)
                self._count = 50
            return self._currValue
        except Exception as E:
            print(E)

        pass
    def _getSqlValue(self):
        if self._currValues is None:
            self._currValues = True
            self.operator = MysqlC()
        self._currValue = self.operator.queryScalarBySql(self.params['sql'])
        return self._currValue
        pass