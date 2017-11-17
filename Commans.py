import json
# from dbs.MysqlC import MysqlC
class Comman:
    def getConfig(self):
        file_obj = open('config.txt', 'r')
        try:
            content = file_obj.read()
            content = json.loads(content)
            return content
        finally:
            file_obj.close()
    # def getTableColums(self,tbl):
    #     pass
        # operator = MysqlC();
        # return operator.queryBySql('desc '+tbl)
        # configs = self.getConfig();
        # self._conn = pymysql.Connect(host=configs['host'], port=configs['port'],user=configs['userName'],passwd=configs['passWord'],db=configs['db'],charset='utf8')
        # self._cursor = self._conn.cursor(cursor=pymysql.cursors.DictCursor)
        # self._cursor.execute('desc '+tbl)
        # colums = self._cursor.fetchall()
        # return colums
    pass