import tkinter
import json
import pymysql

from tkinter.messagebox import *
class DialogDbConnect(tkinter.Toplevel):
    def __init__(self,parrent):
        super().__init__()
        self.title('设置连接属性')
        self.parent = parrent
        self.host = tkinter.StringVar()
        self.userName = tkinter.StringVar()
        self.passWord = tkinter.StringVar()
        self.port = tkinter.IntVar()
        self.db = tkinter.StringVar()
        self.initConfig()
        row1 = tkinter.Frame(self)
        row1.pack(fill='x')
        tkinter.Label(row1, text='host:',width=8).pack(side=tkinter.LEFT)
        tkinter.Entry(row1,width=20, textvariable=self.host).pack(side=tkinter.LEFT)

        row1_1 = tkinter.Frame(self)
        row1_1.pack(fill='x')
        tkinter.Label(row1_1, text='Port:',width=8).pack(side=tkinter.LEFT)
        tkinter.Entry(row1_1,width=20, textvariable=self.port).pack(side=tkinter.LEFT)

        row1_2 = tkinter.Frame(self)
        row1_2.pack(fill='x')
        tkinter.Label(row1_2, text='db:', width=8).pack(side=tkinter.LEFT)
        tkinter.Entry(row1_2, width=20, textvariable=self.db).pack(side=tkinter.LEFT)

        row2 = tkinter.Frame(self)
        row2.pack(fill='x')
        tkinter.Label(row2, text='Username:',width=8).pack(side=tkinter.LEFT)
        tkinter.Entry(row2,width=20,textvariable=self.userName).pack(side=tkinter.LEFT)

        row3 = tkinter.Frame(self)
        row3.pack(fill='x')
        tkinter.Label(row3, text='Password:',width=8).pack(side=tkinter.LEFT)
        tkinter.Entry(row3,width=20,textvariable=self.passWord).pack(side=tkinter.LEFT)

        row4 = tkinter.Frame(self)
        row4.pack(fill='x')
        tkinter.Button(row4, text="连接测试", command=self.testConfig).pack(side=tkinter.LEFT)
        tkinter.Button(row4, text="取消",command=self.cancel).pack(side=tkinter.RIGHT)
        tkinter.Button(row4, text="确定",command=self.ok).pack(side=tkinter.RIGHT)
    def ok(self):
        data = {
            'userName':self.userName.get(),
            'passWord':self.passWord.get(),
            'host':self.host.get(),
            'port':self.port.get(),
            'db':self.db.get()
        }
        # self.testConfig(data['host'],3306,data['userName'],data['passWord'],'xmis')
        print(data)
        jdata = json.dumps(data)
        file_obj = open('config.txt','w')
        file_obj.write(jdata)
        file_obj.close()
        showinfo('Success','OK')
        self.destroy()
    def cancel(self):
        self.destroy()
    def initConfig(self):
        file_obj = open('config.txt','r')
        try:
            content = file_obj.read()
            content = json.loads(content)
            self.passWord.set(content['passWord'])
            self.host.set(content['host'])
            self.userName.set(content['userName'])
            self.port.set(content['port'])
            self.db.set(content['db'])
        finally:
            file_obj.close()
    def testConfig(self):
        host = self.host.get()
        port = self.port.get()
        user = self.userName.get()
        passwd = self.passWord.get()
        db = self.db.get()
        try:
            self._conn = pymysql.Connect(host=host, port=port,user=user,passwd=passwd,db=db,charset='utf8')
            self._cursor = self._conn.cursor(cursor=pymysql.cursors.DictCursor)
            self._cursor.execute('Show Tables')
            result = self._cursor.fetchone()
            if result:
                showinfo('Success', 'Connect Ok')
        except Exception as E:
            showerror('Error',str(E))