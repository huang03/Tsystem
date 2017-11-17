import tkinter
import json
from dbs.MysqlT import MysqlT
from dbs.MysqlC import MysqlC
from rules.RuleViews import *
from tkinter.messagebox import *
from winCls.DialogExtraRule import DialogExtraRule
class TableRules(tkinter.Tk):
    '''
    数据表，字段规则，展示一个数据表中，所有字段的规则说明
    '''
    def __init__(self,tbl):
        super().__init__()
        self.tbl = tbl
        self.title(tbl)
        self.geometry('1000x500')
        self.renders = renderViews()
        self.params = {}
        self.extras = {}
        operator = MysqlT()
        self.activeRow = operator.queryRow({ #查询某个表的字段规则
            'table':'tsys_insert_items as A',
            'select':'A.id,B.property,B.extras',
            'join':'LEFT JOIN tsys_insert_items_detail as B ON A.id = B.item_id ',
            'condition':"user_id=1 AND tbl='%s'" % self.tbl
        })
        self.listColumnsRule(tbl)
    #以列表的形式，展示字段规则
    def listColumnsRule(self,tbl):

        columns = self.getTableColums(tbl)
        navFrame = tkinter.Frame(self)
        tkinter.Button(navFrame,text='Ok',command=self.getParams).pack(side=tkinter.LEFT)
        navFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        for item in columns:
            if item['Extra'] == '':
                field = item['Field']
                itemFrame = tkinter.Frame(self)
                tkinter.Label(itemFrame,text=field).pack(side=tkinter.LEFT)

                if 'varchar' in  item['Type']:
                    self.renders.render(field,'Varchar',itemFrame)
                elif 'int' in item['Type']:
                    self.renders.render(field,'Integer',itemFrame)
                elif 'stamptime' in item['Type']:
                    self.renders.render(field,'StampTime',itemFrame)
                tkinter.Button(itemFrame, text='Extra',command=lambda:self.addExtra(field)).pack(side=tkinter.LEFT)
                itemFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH)
                self.params[item['Field']] = {}
                del itemFrame
        if self.activeRow: #如果具体数据，设置具体规则的参数数据
            property = json.loads(self.activeRow['property'])
            for prty in property:
                if property[prty].get('_TYPE_'):
                    self.extras[prty] = property[prty]
                self.renders.setParams(prty,property[prty])
        # print(self.extras)
        pass
    #设置额外规则 ， field 字段
    def addExtra(self,field):
        DialogExtraRule(self,field)
        # self.wait_window(dialog)
        pass
    #获取规则的具体参数
    def getParams(self):
       keys = list(self.params.keys())
       for key in keys:
           if self.extras.get(key):
               tmp = self.extras[key]
           else:
               tmp = self.renders.getParams(key)
               if not isinstance(tmp, dict):
                    showwarning('Warning',' %s %s' %(key,tmp))
                    return False
           self.params[key] = tmp

       if self.activeRow:#如果存在，更新
            self.updateRule(self.params)
       else:
            self.insertRule(self.params)
    def insertRule(self,params):

        try:
            # extra = 0
            # extras = ''
            # if self.extras:
            #     extra = 1
            #     extras = json.dumps(self.extras)

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
            print('DialogTableRules 108')
            print(e)
            operator.rollback()
        pass
    def updateRule(self,params):
        try:
            operator = MysqlT()
            for key in self.extras:
                params[key] = self.extras[key]
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
            print(E)
            operator.rollback()
            operator.close()
    def getTableColums(self,tbl):
        operator = MysqlC();
        return operator.queryBySql('desc '+tbl)

    pass