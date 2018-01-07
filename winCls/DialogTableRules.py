import tkinter
import json
from dbs.MysqlT import MysqlT
from dbs.MysqlC import MysqlC
from rules.RuleViews import *
from tkinter.messagebox import *
from winCls.DialogExtraRule import DialogExtraRule
from views.VarcharView import VarcharView
from views.IntegerView import IntegerView
from views.TimeStampView import TimeStampView
import time
class TableRules(tkinter.Toplevel):
    '''
    数据表，字段规则，展示一个数据表中，所有字段的规则说明
    '''
    def __init__(self,tbl,parent):
        super().__init__()
        self.parent = parent
        self.tbl = tbl
        self.title(tbl)
        self.columnLog = {}
        self.geometry('%dx%d+%d+%d' % self.parent.center_window(1000, 600))
        self._keyType = {}
        #self.geometry('1000x600')
        # self.renders = renderViews()
        self.params = {}
        # self.extras = {}
        operator = MysqlT()
        self.activeRow = operator.queryRow({ #查询某个表的字段规则
            'table':'tsys_insert_items as A',
            'select':'A.id,B.property,B.extras',
            'join':'LEFT JOIN tsys_insert_items_detail as B ON A.id = B.item_id ',
            'condition':"user_id=1 AND tbl='%s'" % self.tbl
        })

        # self.listColumnsRule(tbl)
        self.showColumn(tbl)

    def showColumn(self,tbl):
        columns = self.getTableColums(tbl)
        row = 0
        print(columns)

        for item in columns:
            if item['Extra'] == '':
                field = item['Field']
                if 'varchar' in item['Type']:
                    self._keyType[field] = 'Varchar'
                elif 'int' in item['Type']:
                    self._keyType[field] = 'Int'
                elif 'timestamp' in item['Type']:
                    self._keyType[field] = 'TimeStamp'

                self.params[field] = False
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
    def editField(self,event):
        tmpView = None
        field = self.lb.get(self.lb.curselection())
        if self._keyType[field] == 'Varchar':
            tmpView = VarcharView()
        elif self._keyType[field] == 'Int':
            tmpView = IntegerView()
        elif self._keyType[field] == 'TimeStamp':
            tmpView = TimeStampView()
            #...................TimeStamp
        if not tmpView:
            showinfo('TIP', '没有该类型的编辑配置设置')
            return False
        if self.activeRow: #如果具体数据，设置具体规则的参数数据
            property = json.loads(self.activeRow['property'])
            print(property[field])
            tmpView.setParams(property[field])


        self.withdraw()
        self.wait_window(tmpView)
        self.deiconify()
        self.params[field] = tmpView.getParams()
        print(self.params)
        tmpView.destroy()
    def summit(self):
        for item in self.params:
            if self.params[item] is False:
                showwarning('Tip','%s 未设置参数'% item)
                return False
        if self.activeRow:#如果存在，更新
            self.updateRule(self.params)
        else:
            self.insertRule(self.params)
        # self.insertRule(self.params)

    #以列表的形式，展示字段规则
    # def listColumnsRule(self,tbl):
    #
    #     columns = self.getTableColums(tbl)
    #
    #     navFrame = tkinter.Frame(self)
    #     tkinter.Button(navFrame,text='Ok',command=self.getParams).pack(side=tkinter.LEFT)
    #     navFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
    #     row = 0
    #     for item in columns:
    #
    #         # print(item)
    #         if item['Extra'] == '':
    #             field = item['Field']
    #             itemFrame = tkinter.Frame(self)
    #             # tkinter.Label(itemFrame,text=field).pack(side=tkinter.LEFT)
    #             tkinter.Label(itemFrame, text=field,width=20,bg='red').grid(row=row,column=0,sticky=tkinter.W)
    #             if 'varchar' in  item['Type']:
    #                 self.renders.render(field,'Varchar',itemFrame,row)
    #                 tkinter.Button(itemFrame, text='Extra', command=lambda: self.addExtra(field, 'Varchar')).grid(
    #                     row=row, column=9)
    #             elif 'int' in item['Type']:
    #                 self.renders.render(field,'Integer',itemFrame,row)
    #                 tkinter.Button(itemFrame, text='Extra', command=lambda: self.addExtra(field, 'Integer')).grid(
    #                     row=row, column=9)
    #             elif 'timestamp' in item['Type']:
    #                 self.renders.render(field,'TimeStamp',itemFrame,row)
    #                 tkinter.Button(itemFrame, text='Extra', command=lambda: self.addExtra(field, 'TimeStamp')).grid(row=row,column=9)
    #             itemFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
    #             self.params[item['Field']] = {}
    #             del itemFrame
    #             row += 1
    #     # print(self.activeRow)
    #     if self.activeRow: #如果具体数据，设置具体规则的参数数据
    #         property = json.loads(self.activeRow['property'])
    #         for prty in property:
    #             if property[prty].get('_TYPE_'):
    #                 self.extras[prty] = property[prty]
    #             self.renders.setParams(prty,property[prty])
    #     # print(self.extras)
    #     pass
    #设置额外规则 ， field 字段
    # def addExtra(self,field, type):
    #
    #     dialog = DialogExtraRule(self,field, type)
    #     self.withdraw()
    #     self.wait_window(dialog)
    #     self.deiconify()
    #     print(111)
    #     pass
    #获取规则的具体参数
    # def getParams(self):
    #    keys = list(self.params.keys())
    #    for key in keys:
    #        if self.extras.get(key):
    #            tmp = self.extras[key]
    #        else:
    #            tmp = self.renders.getParams(key)
    #            if not isinstance(tmp, dict):
    #                 showwarning('Warning',' %s %s' %(key,tmp))
    #                 return False
    #        self.params[key] = tmp
    #
    #    if self.activeRow:#如果存在，更新
    #         self.updateRule(self.params)
    #    else:
    #         self.insertRule(self.params)
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
    def updateRule(self,params):
        try:
            operator = MysqlT()
            # for key in self.extras:
            #     params[key] = self.extras[key]
                # print(extra)
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

    pass

# class TESTA:
#     def __init__(self,field):
#         print(field)