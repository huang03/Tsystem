import pymysql
from dbs.IBase import Base
from dbs.mysqlBase import MySQLBase

class Mysql(MySQLBase):

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
