import tkinter
import json
from dbs.MysqlT import MysqlT
from dbs.MysqlC import MysqlC
from rules.RuleViews import *
from tkinter.messagebox import *
from views.VarcharView import VarcharView
from views.IntegerView import IntegerView
from views.TimeStampView import TimeStampView
from views.DateView import DateView
class TableRules(tkinter.Toplevel):
    '''
    数据表，字段规则，展示一个数据表中，所有字段的规则说明
    '''
    def __init__(self,tbl,parent):
        super().__init__()
        self.parent = parent
        self.tbl = tbl
        self.title(tbl)
        self.geometry('%dx%d+%d+%d' % self.parent.center_window(1000, 600))
        self._keyType = {}#键类型隐射

        self.params = {}

        operator = MysqlT()
        self.activeRow = operator.queryRow({ #查询某个表的字段规则
            'table':'tsys_insert_items as A',
            'select':'A.id,B.property,B.extras',
            'join':'LEFT JOIN tsys_insert_items_detail as B ON A.id = B.item_id ',
            'condition':"user_id=1 AND tbl='%s'" % self.tbl
        })

        self.showColumn(tbl)

    #显示表中，需要编辑的属性字段，可自动添加的除外
    def showColumn(self,tbl):
        columns = self.getTableColums(tbl)
        if self.activeRow:
            property = json.loads(self.activeRow['property'])
        for item in columns:
            if item['Extra'] == '':
                field = item['Field']
                if 'varchar' in item['Type']:
                    self._keyType[field] = 'Varchar'
                elif 'int' in item['Type'] or 'smallint' in item['Type']:
                    self._keyType[field] = 'Int'
                elif 'tinyint' in item['Type']:
                    self._keyType[field] = 'TinyInt'
                elif 'smallint' in item['Type']:
                    self._keyType[field] = 'SmallInt'
                elif 'timestamp' in item['Type']:
                    self._keyType[field] = 'TimeStamp'
                elif 'date' in item['Type']:
                    self._keyType[field] = 'Date'
                if not self.activeRow:
                    self.params[field] = False
                else:
                    self.params[field] = property[field]
        row1 = tkinter.Frame(self)
        scrolly = tkinter.Scrollbar(row1)
        scrolly.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.lb = tkinter.Listbox(row1, width=300, yscrollcommand=scrolly.set)
        self.lb.bind('<Double-Button-1>', self.editField)
        scrolly.config(command=self.lb.yview)
        for key in self._keyType:
            self.lb.insert(tkinter.END, key )
        self.lb.pack()
        row1.pack(fill='x')
        row2 = tkinter.Frame(self)
        row2.pack(fill='x')
        tkinter.Button(row2,text='OK',width=200,command=self.summit).pack(side=tkinter.RIGHT)
        print(self.params)
    #编辑属性参数
    def editField(self,event):
        tmpView = None
        field = self.lb.get(self.lb.curselection())
        #根据字段类型，选择编辑框
        if self._keyType[field] == 'Varchar':
            tmpView = VarcharView()
        elif self._keyType[field] == 'Int':
            tmpView = IntegerView()
        elif self._keyType[field] == 'SmallInt':
            tmpView = IntegerView('SmallInt')
        elif self._keyType[field] == 'TinyInt':
            tmpView = IntegerView('TinyInt')
        elif self._keyType[field] == 'TimeStamp':
            tmpView = TimeStampView()
        elif self._keyType[field] == 'Date':
            tmpView = DateView()


        if not tmpView:
            showinfo('TIP', '没有该类型的编辑配置设置')
            return False

        if self.activeRow: #如果具体数据，设置具体规则的参数数据
            property = json.loads(self.activeRow['property'])
            tmpView.setParams(property[field])


        self.withdraw()
        self.wait_window(tmpView)
        self.deiconify()
        self.params[field] = tmpView.getParams()
        tmpView.destroy()


    #提交参数
    def summit(self):
        for item in self.params:
            if self.params[item] is False:
                showwarning('Tip','%s 未设置参数'% item)
                return False
        if self.activeRow:#如果存在，更新
            self.updateRule(self.params)
        else:
            self.insertRule(self.params)

    #插入规则
    def insertRule(self,params):

        try:
            operator = MysqlT()
            result = operator.add({
                'table':'tsys_insert_items',
                'field':('user_id','tbl','title'),
                'binds':('1',self.tbl,'test')
            },False)
            if result:
                id =operator.getLastId()
                result2 = operator.add({
                    'table':'tsys_insert_items_detail',
                    'field':('property','item_id'),
                    'binds':(json.dumps(params),id)
                })
                if result2:
                    showinfo('info','OK')
                    operator.commit()
            operator.close()
        except Exception as e:
            print('InsertRule')
            print(e)
            operator.rollback()
        pass

    #更新规则
    def updateRule(self,params):
        try:
            operator = MysqlT()
            result = operator.update({
                'table':'tsys_insert_items_detail',
                'set':('property=%s',),
                'condition':'item_id=%d' % self.activeRow['id'],
                'binds':(json.dumps(params),)
            })
            if result:
                showinfo('Info','Ok')
            else:
                operator.rollback()
                showerror('Error','Error Update')
                operator.close()
        except Exception as E:
            print('updateRule')
            print(E)

            operator.rollback()
            operator.close()
    def getTableColums(self,tbl):
        operator = MysqlC();
        return operator.queryBySql('desc '+tbl)


# class TESTA:
#     def __init__(self,field):
#         print(field)