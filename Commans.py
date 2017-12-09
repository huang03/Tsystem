import json,os
# from dbs.MysqlC import MysqlC
class Comman:
    def getConfig(self):
        path = os.path.dirname(os.path.abspath(__file__))
        file_obj = open(path + '\config.txt', 'r')
        try:
            content = file_obj.read()
            content = json.loads(content)
            return content
        except Exception as e:
            print(e)
        finally:
            file_obj.close()

            def center_window(self, w, h):
                # 获取屏幕 宽、高
                ws = self.winfo_screenwidth()
                hs = self.winfo_screenheight()
                # 计算 x, y 位置
                x = (ws / 2) - (w / 2)
                y = (hs / 2) - (h / 2)
                self.geometry('%dx%d+%d+%d' % (w, h, x, y))
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