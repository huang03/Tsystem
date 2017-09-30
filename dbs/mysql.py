import pymysql
from dbs.IBase import Base


class Mysql(Base):
    '''
        mysql 数据库操作类
        queryAll: 查找所有
        queryRow: 查找单行
        queryScalar: 查找第一行第一列的值
        delete: 删除
        add: 添加
        addBatch: 批量添加
        update: 更新
        getSql: 获取执行的Sql
        setSql: 设置执行的Sql #需要改，没有判断是否有设置
        close: 关闭连接

        其中参数params 为 dict 类型；值
            table:数据表
            field:字段  tuple
            value:绑定是格式 eg (%s,%s,...) 
            binds:具体的value绑定值 eg('szx','ff',...)

            condition: 条件。可以是字符串，可以是list,tuple
            set:更新条件的 set tuple
            order: 排序
            limit: 查询条数限制
            join: 表连接
            select: 需要查询的字段 字符串 or list tuple

    '''
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_DB'):
            cls._DB = super().__new__(cls)
        return cls._DB
    def __init__(self,host='127.0.0.1',port=3306,user='func',passwd='passwd',db='mysql',charset='utf8'):
        self._sql = ''
        self._conn = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        #self._cursor = self._conn.cursor()  # 字典类查询
        self._cursor = self._conn.cursor(cursor=pymysql.cursors.DictCursor)  # 字典类查询

    def __del__(self):
        self.close()
    def queryAll(self,params):
        '''
            params需要 table select 
                  可选：condtion limit order join
        '''
        self._selectPackage(params)
        self._execute(params)
        return self._cursor.fetchall()
    def queryRow(self,params):
        '''
            params需要 table select 
                  可选：condtion limit order join
        '''
        self._selectPackage(params)
        self._execute(params)
        return self._cursor.fetchone()
    def queryScalar(self,params):
        '''
            params需要 table select 
                  可选：condtion limit order join
        '''
        result = self.queryRow(params);
        if result:
            return list(result.values())[0];
        return None

    def delete(self,params):
        '''
            params需要 table condition 
                  可选：limit
        '''
        if not params.get('table'):
            raise ValueError('lack of table')
        if params.get('condition'):
            if type(params['condition']) != type('a'):
                params['condition'] = ' AND '.join(params['condition'])
        else:
            raise ValueError('lack of conditon')
        self._sql = 'DELETE FROM '+ params['table']  + ' WHERE ' + params['condition']
        self._execute(params)
        self._conn.commit()
        return self._cursor.rowcount
    def add(self,params,test=False):
        '''
            params需要 table field value binds 
        '''
        self._addPackage(params)
        if test:
            return self._sql

        else:
            self._execute(params)
            self._conn.commit()
            return self._cursor.rowcount
    def addBatch(self,params):
        '''
            params需要 table field value binds 
        '''
        try:
            #参数类型貌似只能是%
            self._addPackage(params);
            print(self._sql)
            self._cursor.executemany(self._sql,params['binds'])
            self._conn.commit()
            return self._cursor.rowcount
        except Exception as e:
            print(e)
    #set xx=%s,aa=%d..
    def update(self,params):
        '''
            params需要 table condition set
                  可选：limit 
        '''
        if not params.get('table'):
            raise ValueError('lack of table')

        if params.get('condition'):
            if type(params['condition']) != type('a'):
                params['condition'] = ' AND '.join(params['condition'])
        else:
            raise ValueError('lack of conditon')


        if params.get('set'):
            if type((1,)) != type(params.get('set')):
                raise ValueError('set must be tuple')
            params['set'] = ','.join(params['set'])
        else:
            raise ValueError('lack of value')

        if params.get('binds'):
            if type((1,)) != type(params.get('binds')):
                raise ValueError('value must be tuple ')
        # else:
        #     raise ValueError('lack of value')
        self._sql = 'UPDATE '+ params['table'] + ' SET ' + params['set']  + ' WHERE ' + params['condition']
        print(self._sql)
        self._execute(params)
        self._conn.commit()
        return self._cursor.rowcount
        #self._sql = self._sql + ' WHERE ' + params['condition']

    def _execute(self,parmas):
        try:
            if parmas.get('binds'):
                self._cursor.execute(self._sql % parmas.get('binds'))
            else:
                self._cursor.execute(self._sql)
        except Exception as e:
            print(e)
            raise Exception('error')
    def getSql(self):
        return self._sql
    def setSql(self,sql):
        self._sql = sql
    def _addPackage(self,params):
        if not params.get('table'):
            raise ValueError('lack of ')

        if not params.get('field'):
            raise ValueError('lack of field')
        elif type((1,)) != type(params.get('field')):
            raise ValueError('field must be tuple')


        if params.get('value'):
            if type((1,)) != type(params.get('value')):
                raise ValueError('the value must be tuple eg(%s,%s,...)')
        else:
            ct = len(params['field'])
            print(ct)
            params['value'] = ['%s' for i in range(ct)]

        if not params.get('binds'):
           raise ValueError('lack of binds')
        elif type(('1')) == type(params.get('binds')):
           raise ValueError('binds must be tuple or the list of tuple')



        params['value'] = ','.join(params['value'])
        params['field'] = ','.join(params.get('field'))
        self._sql = 'INSERT INTO ' + params.get('table') +'(' + params['field'] +')' +'VALUES(' + params['value'] + ')'


    def _selectPackage(self,params):
        if not params.get('table'):
            raise Exception('lack table key')
        if not params.get('select'):
            raise Exception('lack  select key')
       # package = ('SELECT')
        self._sql = 'SELECT '
        if type(params['select']) != type('a'):
            params['select'] = '`,`'.join(params['select'])
            params['select'] = '`'+params['select']+'`'

        self._sql = self._sql + params['select']
        self._sql = self._sql + ' FROM ' + params['table']

        if params.get('join'):
            self._sql = self._sql + ' '+params.get('join') + ' '

        if params.get('condition'):
            if type(params['condition']) != type('a'):
                params['condition'] = ' AND '.join(params['condition'])
                # print(params['condition'])
            self._sql = self._sql + ' WHERE ' + params['condition']

        if params.get('order'):
            self._sql = self._sql + ' ' + params.get('order') + ' '

        if params.get('limit'):
            self._sql = self._sql + ' ' + params.get('limit')

    def close(self):
        self._DB = None
        self._cursor.close()
        self._conn.close()

