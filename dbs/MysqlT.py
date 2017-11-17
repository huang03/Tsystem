from dbs.mysql import Mysql
from  Commans import Comman
class MysqlT(Mysql):
    def __init__(self):
        # comman = Comman()
        # configs = comman.getConfig()
        super().__init__(host='127.0.0.1',port=3306,user='func',passwd='passwd',db='tsys')