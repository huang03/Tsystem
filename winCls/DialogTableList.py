import tkinter
from dbs.MysqlC import MysqlC
from tkinter.messagebox import *
# import json
class DialogTableList(tkinter.Toplevel):
    def __init__(self,parent):
        super().__init__()
        self.title('数据表')
        self.parent = parent
        self.geometry('%dx%d+%d+%d' % self.parent.center_window(500,250))

        Tlist = self.getTbls()
        row1 = tkinter.Frame(self)
        self.tbl = tkinter.StringVar()
        scrolly = tkinter.Scrollbar(row1)
        scrolly.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.lb = tkinter.Listbox(row1,listvariable=self.tbl,width=300,yscrollcommand=scrolly.set)
        scrolly.config(command=self.lb.yview)
        for tbl in Tlist:
            self.lb.insert(tkinter.END, list(tbl.values())[0])
        self.lb.pack()
        row1.pack(fill='x')
        row2 = tkinter.Frame(self)
        row2.pack(fill='x')
        tkinter.Button(row2,text='Choice',width=200,command=self.choiceTbl).pack(side=tkinter.RIGHT)
    def choiceTbl(self):
        if len(self.lb.curselection()) < 1:
            showwarning('TIP','choose one item please')
            self.lb.focus_force()
            return False
        self.parent.currTbl = self.lb.get(self.lb.curselection())

        self.destroy()
    def closeWin(self):
        self.destroy()

    def getTbls(self):
        operator = MysqlC()
        return operator.queryBySql('Show Tables')

    pass