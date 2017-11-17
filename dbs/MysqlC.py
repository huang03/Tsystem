from dbs.mysqlBase import MySQLBase
from Commans import Comman
# import pymysql
class MysqlC(MySQLBase):
    def __init__(self):
        comman = Comman()
        configs = comman.getConfig()
        super().__init__(host=configs['host'],port=configs['port'],user=configs['userName'],passwd=configs['passWord'],db=configs['db'])