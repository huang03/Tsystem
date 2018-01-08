from dbs.MysqlC import MysqlC
import math,random
class _IRule:
    '''
        规则类接口

        params：{
            start: 开始值
            end: 结束值
            prefix:  字符串前缀
            sql: 查询的sql
            table: 表,属性
            list: 列表值  eg:1,2,3,4
            _TYPE_:类型
        }
        类型包括：常规 COMMAN  列表：LIST 表属性：TABLE  SQL:SQL  当前时间：NOW
    '''
    def __init__(self,params):
        self.params = params #需要验证的参数
        self._error = None #当前错误信息
        self._currValue = None #根据规则生成的值
        self._currValues = None #作为列名使用


    def getError(self):
        return self._error

    def _setError(self,error):
        self._error = error

    #根据规则产生值
    def getValue(self):
        if self.params['_TYPE_'] == 'COMMAN': #常规
            return self._getCommanValue()
        elif self.params['_TYPE_'] == 'LIST': #列表值
            return self._getListValue()
        elif self.params['_TYPE_'] == 'TABLE': #表属性值
            return self._getTableValue()
        elif self.params['_TYPE_'] == 'SQL': #SQL
            return self._getSqlValue()
        elif self.params['_TYPE_'] == 'NOW': #获取当前时间
            return self._getNowValue()
        return None
        pass
    #验证参数值
    def validate(self, type='COMMAN'):
        if type is 'COMMAN':
            return self._validateComman()
        elif type is 'LIST':
            return self._validateList()
        elif type is 'SQL':
            return self._validateSql()
        elif type is 'TABLE':
            return self._validateTable()
        elif type is 'NOW':
            return True
        return False;

    #验证表属性，数据要求  数据表,表属性   逗号分隔
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

    #验证SQL是否正确
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
    #验证列表值   数据规则   xx,xx,xxx 以逗号分隔
    def _validateList(self):
        if self.params.get('list') == '':
            self._setError('指定列表不能为空')
            return False
        return True
        pass

    #常规验证
    def _validateComman(self):
        return True

    #检查表属性是否存在
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

    #获取常规值
    def _getCommanValue(self):
        return False

    #获取当前时间
    def _getNowValue(self):
        pass

    #获取列表值
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

    #获取表属性值
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

    #获取SQL值
    def _getSqlValue(self):
        if self._currValues is None:
            self._currValues = True
            self.operator = MysqlC()
        self._currValue = self.operator.queryScalarBySql(self.params['sql'])
        return self._currValue
        pass