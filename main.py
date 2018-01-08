import tkinter
import json
from rules.RuleViews import *

from dbs.MysqlC import MysqlC
from dbs.MysqlT import MysqlT
from winCls.DialogTableRules import TableRules
from winCls.DialogDbConnect import DialogDbConnect
from winCls.DialogTableList import DialogTableList
from winCls.DialogAPI import DialogAPI
from runs.APIRun import APIRun
from runs.DBRun import DBRun
from runs.Runs import Runs
from rules2.RuleFactory import RuleFactory
from VisitUrl import VisitUrl
import Constants

class RunTSystem(tkinter.Tk):
    '''
    主要运行函数
    '''
    def __init__(self):
        # self.RPG = RPackages()
        super().__init__()
        self.title('Tsystem')
        self.resizable(False,False)
        self.geometry('%dx%d+%d+%d' % self.center_window(800,500))

        self.currTbl = '' #记录当前选择表
        self.intervalTm = tkinter.StringVar() #记录任务执行频率
        self.initial()

    def center_window(self, w, h):
        # 获取屏幕 宽、高
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        return (w, h, x, y)
        # self.geometry('%dx%d+%d+%d' % (w, h, x, y))


    def initial(self):
        '''
        界面初始化
        :return:
        '''

        navsFrame =tkinter.Frame(bg='yellow',width=796,height=50)
        tkinter.Button(navsFrame, text='接口', width=10, command=self.openWindow).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='连接属性', width=10,command=lambda:self.openSetDdConnectWindow(self)).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='数据表', width=10,command=lambda:self.openTableListWindow(self)).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='RUN', width=10, command=self.runTasks).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='STOP',width=10, command=self.stopTasks).pack(side=tkinter.LEFT)
        tkinter.Label(navsFrame, text='Interval：').pack(side=tkinter.LEFT)
        tkinter.Entry(navsFrame,textvariable = self.intervalTm).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='SET', command=self.setIntervalTm).pack(side=tkinter.LEFT) #设置任务执行频率
        navsFrame.grid(row=0,column=0,pady=5,sticky=tkinter.W)

        self.taskFram = tkinter.Frame(bg='blue',width=796,height=200)
        self.taskFram.grid(row=1,column=0,pady=5,sticky=tkinter.W)
        self.taskFram.grid_propagate(0)

        self.RUNS = Runs()#运行规则类


        self.logsFrame = tkinter.Frame(bg='red',width=796,height=200)
        self.logsFrame.grid(row=2,column=0,sticky=tkinter.W)

        self.listInsertItem()
        self.logs = LogsList(self.logsFrame)



        # P = ApiItems(self.taskFram, self.RUNS)

        pass
    #运行任务
    def runTasks(self):
        self.RUNS.run()

    #停止任务
    def stopTasks(self):

        pass
    #设置任务执行频率
    def setIntervalTm(self):
        if self.intervalTm.get() == '':
            self.intervalTm.set(0.1)


    def openWindow(self):
        dialog = DialogAPI(self)
        pass

    #打开数据库，数据列表窗口，对数据表设置添加规则
    def openTableListWindow(self,parent):
        dialog = DialogTableList(parent)
        parent.withdraw()
        self.wait_window(dialog)

        if self.currTbl != '':
            dialogTR = TableRules(self.currTbl,parent) #规则设置窗口
            self.wait_window(dialogTR)
            parent.deiconify()
            self.currTbl = ''
        else:
            parent.deiconify()
        pass

    #数据库属性设置窗口
    def openSetDdConnectWindow(self,parent):
        dialog = DialogDbConnect(parent);
        parent.withdraw()
        self.wait_window(dialog)
        parent.update()
        parent.deiconify()
        pass

    #主界面展示已添加添加规则的数据表
    def listInsertItem(self):
        operator = MysqlT()
        result = operator.queryAll({
            'table':'tsys_insert_items',
            'select':'tbl,id,extra',
            'condtion':'user_id=1'
        })
        Items = InsertItems(self.taskFram,result,self.RUNS)


#运行记录
class LogsList:
    def __init__(self,parent):
        self.logs = tkinter.Listbox(parent,width=796)
        self.logs.pack(side=tkinter.RIGHT)
    def add(self,log):
        self.logs.insert(0,log)
    pass

class ApiItems:
    def __init__(self,parent,RUNS):
        self.createItem(parent)
        self._ruleFactory = RuleFactory()
        self._RUNS = RUNS
        self._VisitUrl = VisitUrl()
        # self._TMysql = MysqlT()
        pass
    def _getData(self):
        operator = MysqlT()
        result = operator.queryAll({
            'table':'tsys_api_items',
            'select':'id,title,api,type',
            'condition':'user_id=1'
        })
        operator.close()
        # print(result)
        return result
        pass
    def createItem(self,parent):
        items = self._getData();
        frm = tkinter.Frame(parent,height = 200,width = 400)
        row = 0;
        # print(items)
        for item in items:
            column = 0
            tkinter.Label(frm, text=row + 1).grid(row=row, column=column, padx=10, pady=5)
            column += 2
            tkinter.Label(frm, text=item['title']).grid(row=row, column=column, padx=20, pady=5)
            column += 1
            column += 1
            id = item['id']

            tkinter.Button(frm, text='Run',command=lambda :self.run(item)).grid(row=row, column=column, padx=10, pady=5)
            # tkinter.Label(frm,text=item['title']).pack(side=tkinter.TOP,fill='x')
            row += 1;

        frm.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        frm.pack_propagate(0)
        # frm
        pass
    def run(self,item):
        operator = MysqlT()
        result = operator.queryRow({
            'table': 'tsys_api_items_detail',
            'select': 'property',
            'condition': 'item_id=%d' % item['id']
        })
        properties = result['property']
        properties = json.loads(properties)
        runObj = APIRun(self._VisitUrl)
        runObj.addTaskParams(item['api'],item['type'])
        for key  in properties:
            property = properties[key]
            obj = self._ruleFactory.getAPIRule(property['type'],property['value'])
            runObj.addTask(key,obj)
        self._RUNS.addRunObj(runObj)
        operator.close()

        pass
class InsertItems:
    '''
    根据用户的设置规则，为每个表生成一个item,每个item包含表中，每个字段属性的数据生成规则，在点击运行，之后，可以根据该规则，生成每个字段的值，并且将数据插入到数据库
    '''
    def __init__(self,parent,items,RUNS):
        frm = tkinter.Frame(parent,height = 200,width = 400,bg='pink')
        frm.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
        frm.pack_propagate(0)
        self.createItem(frm,items,RUNS)
    def createItem(self,frm,items,RUNS):
        row = 0
        for item in items:
            obj = InsertItem(row,frm,item,RUNS)
            row += 1
        pass
class InsertItem:

    def __init__(self, row, parent, item, RUNS):
        column = 0
        self._RUNS = RUNS
        self.data = {}
        self._ruleFactory = RuleFactory()
        self._DB = MysqlC()
        tkinter.Label(parent, text=row+1).grid(row=row, column=column,padx=10,pady=5)
        column += 2
        tkinter.Label(parent, text=item['tbl']).grid(row=row, column=column,padx=20,pady=5)
        column += 1
        for key in item:
            self.data[key] = item[key]
        tkinter.Button(parent,text='Run',command=self.run).grid(row=row,column=column,padx=10,pady=5)
        pass
    def getData(self):
        return self.data
    def run(self): #需要设置重复加载
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
        runObj = DBRun(self._DB)
        runObj.addTaskParams(self.data['tbl'])
        # if self.data.get('tbl'):
        #     return False;

        #根据每个字段的属性，生成具体规则类,并加入到运行队列,等待运行
        for clm in tblClm:
            obj = None
            if clm['Extra'] != '':
                continue;
            if 'varchar' in clm['Type']:
                obj = self._ruleFactory.getAPIRule(Constants.API_RULE_TYPE['varchar'],detail[clm['Field']])
                # obj = VarcharRule(detail[clm['Field']])
            elif 'int' in clm['Type']:
                obj = self._ruleFactory.getAPIRule(Constants.API_RULE_TYPE['int'], detail[clm['Field']])
                # obj = IntegerRule(detail[clm['Field']])
            elif 'timestamp' in clm['Type']:
                obj = self._ruleFactory.getAPIRule(Constants.API_RULE_TYPE['timestamp'], detail[clm['Field']])

            if obj:
                runObj.addTask(clm['Field'],obj)

        print('add tbl:' + self.data['tbl'])
        self._RUNS.addRunObj(runObj)
    pass



if __name__ == '__main__':
    app = RunTSystem()
    app.mainloop()