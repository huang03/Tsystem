import tkinter
import json
from rules.RuleViews import *
from rules.Rules import *
from rules.RulePackages import RPackages
from dbs.MysqlC import MysqlC
from dbs.MysqlT import MysqlT
from winCls.DialogTableRules import TableRules
from winCls.DialogDbConnect import DialogDbConnect
from winCls.DialogTableList import DialogTableList
#Show Tables 查询数据库的所有表
#show columns from tbl_role  查询表中的所有字段属性
def openWindow():
    top = tkinter.Toplevel()
    top.title('Hello')
    top.focus_set()
    # top.attributes("-toolwindow", 1)
    # top.wm_attributes("-topmost", 1)
    # top.iconify()
    # top.withdraw()
    # top.deiconify()


class RunTSystem(tkinter.Tk):
    '''
    主要运行函数
    '''
    def __init__(self):
        self.RPG = RPackages()
        super().__init__()
        self.title('Tsystem')
        self.geometry('800x500')
        self.currTbl = '' #记录当前选择表
        self.intervalTm = tkinter.StringVar() #记录任务执行频率
        self.initial()
        self.listInsertItem()
    def initial(self):
        '''
        界面初始化
        :return:
        '''
        navsFrame = tkinter.Frame(self)
        tkinter.Button(navsFrame, text='接口', width=10, command=openWindow).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='连接属性', width=10,command=lambda:self.openSetDdConnectWindow(self)).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='数据表', width=10,command=lambda:self.openTableListWindow(self)).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='RUN', width=10, command=self.runTasks).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='STOP',width=10, command=self.stopTasks).pack(side=tkinter.LEFT)
        tkinter.Label(navsFrame, text='Interval：').pack(side=tkinter.LEFT)

        tkinter.Entry(navsFrame,textvariable = self.intervalTm).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='SET', command=self.setIntervalTm).pack(side=tkinter.LEFT) #设置任务执行频率
        navsFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH)

        pass
    #运行任务
    def runTasks(self):
        self.RPG.runs()
    #停止任务
    def stopTasks(self):
        self.RPG.stopRuns()
        pass
    #设置任务执行频率
    def setIntervalTm(self):
        self.RPG.setInterval(self.intervalTm.get())
    #打开数据库，数据列表窗口，对数据表设置添加规则
    def openTableListWindow(self,parent):
        dialog = DialogTableList(parent)
        self.wait_window(dialog)
        if self.currTbl != '':
            TableRules(self.currTbl) #规则设置窗口
        pass
    #数据库属性设置窗口
    def openSetDdConnectWindow(self,parent):
        dialog = DialogDbConnect(parent);
        self.wait_window(dialog)
        pass
    #主界面展示已添加添加规则的数据表
    def listInsertItem(self):
        operator = MysqlT()
        result = operator.queryAll({
            'table':'tsys_insert_items',
            'select':'tbl,id,extra',
            'condtion':'user_id=1'
        })
        Items = InsertItems(self,result,self.RPG)

class InsertItems:
    '''
    根据用户的设置规则，为每个表生成一个item,每个item包含表中，每个字段属性的数据生成规则，在点击运行，之后，可以根据该规则，生成每个字段的值，并且将数据插入到数据库
    '''
    def __init__(self,parent,items,RPG):
        self._objs = []
        self.items = items
        frm = tkinter.Frame(parent)
        frm.pack(side=tkinter.TOP,fill='x')
        self.createItem(frm,items,RPG)

    def createItem(self,frm,items,RPG):
        row = 0
        for item in items:
            obj = InsertItem(row,frm,item,RPG)
            row += 1
        pass
class InsertItem:
    def __init__(self, row, parent, item, RPG):
        column = 0
        # ct = len(item)
        self.RPG = RPG
        self.data = {}
        for key in item:
            tkinter.Label(parent,text=item[key]).grid(row=row,column=column)
            self.data[key] = item[key]
            column += 1
        tkinter.Button(parent,text='Run',command=self.run).grid(row=row,column=column)
        pass
    def getData(self):
        return self.data
    def run(self):
        '''
        将该表的数据生成规则，实例化具体的规则类，并加入的运行队列，等待执行
        :return:
        '''
        operator = MysqlT()
        #获取具体执行的数据生成规则
        detail = operator.queryRow({
            'table':'tsys_insert_items_detail',
            'select':'property',
            'condition':'item_id=%d' % self.data['id']
        })
        detail = json.loads(detail['property'])
        operatorC = MysqlC()
        tblClm = operatorC.queryBySql('desc '+self.data['tbl'])
        # print(self.data['tbl'])
        #根据每个字段的属性，生成具体规则类,并加入到运行队列,等待运行
        for clm in tblClm:
            obj = None
            if clm['Extra'] != '':
                continue;
            if 'varchar' in clm['Type']:
                obj = VarcharRule(detail[clm['Field']])
            elif 'int' in clm['Type']:
                obj = IntegerRule(detail[clm['Field']])
            elif 'stamptime' in clm['Type']:
                obj = TimeStampRule(detail[clm['Field']])
            self.RPG.addRule(self.data['tbl'],clm['Field'],obj)
    pass
if __name__ == '__main__':
    app = RunTSystem()
    app.mainloop()