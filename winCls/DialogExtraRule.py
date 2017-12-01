import tkinter
from dbs.MysqlC import MysqlC
from tkinter.messagebox import *
class DialogExtraRule(tkinter.Toplevel):
    '''
    额外规则视图：
    额外规则包括：固定值列表，数据生成，从这个列表中选择  LIST
                  数据表数据生成，从数据表中，取得某个字段值作为该字段的值  TBL
    额外规则关键参数：_TYPE_ 该参数视为额外参数设定标志
    '''
    def __init__(self,parent,field,type='Varchar'):
        super().__init__()
        self.parent = parent
        self.title('Extra property')
        self.geometry('420x300')
        self.geometry('%dx%d+%d+%d' % self.center_window(420, 300))
        extras = tkinter.StringVar(value=('value list','Table'))
        self.extrasList= tkinter.Listbox(self,listvariable=extras)
        self.extrasList.grid(row=0,column=0)
        self.extrasList.bind('<Double-Button-1>', self.selectExtra)
        self.frm = tkinter.Frame(self)
        self.frm.grid(row=0,column=1)

        self.field = field
        self.type = type
        if type == 'TimeStamp':
            extras.set(('当前时间'))
        if self.parent.extras.get(self.field):
            if self.parent.extras[self.field].get('_TYPE_')=='LIST':
                self.extrasList.select_set(0)
                self.createValuesWin()
            elif self.parent.extras[self.field].get('_TYPE_')=='TBL':
                self.extrasList.select_set(1)
                self.createTblWin()
            elif self.parent.extras[self.field].get('_TYPE_') == 'TIME':
                self.extrasList.select_set(0)
                self.createTimeStampWin()
                # if type == 'TimeStamp':
                #     extras.set(('当前时间'))
                #     pass
                pass
        pass
    def center_window(self, w, h):
        # 获取屏幕 宽、高
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        return (w, h, x, y)
    #选择某个额外规则
    def selectExtra(self,event):
        sel = self.extrasList.curselection()[0]
        self.frm.destroy()
        if self.type == 'TimeStamp':
            self.createTimeStampWin()
            return True
        if sel == 0:
            self.createValuesWin()
        elif sel == 1:
            self.createTblWin()
        print(sel)
    #创建固定列表窗口
    def createTimeStampWin(self):
        self.frm = tkinter.Frame(self)
        self.frm.grid(row=0,column=1)
        self.isNow = tkinter.BooleanVar()
        if self.parent.extras.get(self.field):
            self.isNow.set(self.parent.extras[self.field].get('now'))
        tkinter.Label(self.frm,text='Now:').pack(side=tkinter.LEFT)
        tkinter.Checkbutton(self.frm,variable=self.isNow).pack(side=tkinter.LEFT)
        tkinter.Button(self.frm, text='Ok', command=lambda: self.getTimeStamp()).pack(side=tkinter.LEFT)
        pass
    def getTimeStamp(self):
        if self.isNow.get():
            self.parent.extras[self.field] = {'_TYPE_': 'TIME', 'now': self.isNow.get()}
        else:
            self.parent.extras[self.field] = {}

        print(self.parent.extras)
    def createValuesWin(self):
        self.frm = tkinter.Frame(self)
        self.frm.grid(row=0,column=1)
        val = None
        if self.parent.extras.get(self.field):
            if self.parent.extras[self.field].get('list'):
                val = self.parent.extras[self.field].get('list').split(',')
                val = tuple(val)
        vlist = tkinter.StringVar(value=val)
        vList = tkinter.Listbox(self.frm,listvariable=vlist)
        vList.pack(side=tkinter.TOP,fill='x')
        tkinter.Button(self.frm,text='add',command=lambda :self.addValue(vList)).pack(side=tkinter.BOTTOM)
        tkinter.Button(self.frm, text='delete',command=lambda :self.deleteValue(vList)).pack(side=tkinter.BOTTOM)
        tkinter.Button(self.frm, text='Ok', command=lambda: self.getValues(vList)).pack(side=tkinter.BOTTOM)

    #添加列表数据
    def addValue(self,vList):
        addV = tkinter.Toplevel()
        var = tkinter.StringVar()

        tkinter.Entry(addV,textvariable=var).pack(side=tkinter.TOP,fill='x')
        tkinter.Button(addV,text='OK',command=addV.destroy ).pack(side=tkinter.TOP,fill=tkinter.X)
        self.wait_window(addV)
        vList.insert(tkinter.END,var.get())
    #删除列表数据
    def deleteValue(self,vList):
        cselect = vList.curselection()
        if len(cselect) > 0:
            vList.delete(cselect[0],cselect[0])
        pass
    #获取额外规则参数
    def getValues(self,vList):
        vl = vList.get(0,tkinter.END)
        self.parent.extras[self.field] = {'_TYPE_':'LIST','list':','.join(vl)}
        pass

    #创建数据表窗口
    def createTblWin(self):
        self.frm = tkinter.Frame(self)
        self.frm.grid(row=0,column=1)
        tbl = tkinter.StringVar()
        property = tkinter.StringVar()
        if self.parent.extras.get(self.field):

            tbl.set(self.parent.extras[self.field].get('tbl'))
            property.set(self.parent.extras[self.field].get('property'))

        frm0 = tkinter.Frame(self.frm)
        tkinter.Label(frm0,text='Table').pack(side=tkinter.LEFT)
        tkinter.Entry(frm0,textvariable=tbl).pack(side=tkinter.LEFT)
        frm0.pack(side=tkinter.TOP,fill='x')

        frm1 = tkinter.Frame(self.frm)
        tkinter.Label(frm1,text='property').pack(side=tkinter.LEFT)
        tkinter.Entry(frm1,textvariable=property).pack(side=tkinter.LEFT)
        frm1.pack(side=tkinter.TOP,fill='x')
        tkinter.Button(self.frm,text='OK',command=lambda :self.getTblProperty(tbl,property)).pack(side=tkinter.TOP)
        pass
    #获取TBL 属性
    def getTblProperty(self,tbl,property):
        try:
            operator = MysqlC()
            sql = "SHOW TABLES LIKE '%s'" % tbl.get()
            result = operator.queryBySql(sql)
            if(len(result)) < 1: #判断表是否存在

                tbl.set('')
                showwarning('Warning','table is not exist')
                return False
            sql = "show columns from `%s` like '%s' " %(tbl.get(),property.get())
            result = operator.queryBySql(sql)
            if len(result) < 1:#判断字段是否存在
                property.set('')
                showwarning('Warning', 'property is not exist')
                return False
        except Exception as E:
            print(E)
        self.parent.extras[self.field] = {'_TYPE_':'TBL','tbl':tbl.get(),'property':property.get()}
        pass
