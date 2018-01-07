# -*- coding: utf-8 -*-
import tkinter
from rules.Rules import IntegerRule,VarcharRule,TimeStampRule
class renderViews:
    '''
        为每个表的字段属性，生成具体的UI，以便用户为每个字段输入具体执行规则
    '''
    def __init__(self):
        self._params = {} #记录字段生成数据的具体规则对象
    def render(self,key,type,node,row):
        obj = self.getViewObj(type)
        obj.render(node,row)
        self._params[key] = obj
    #根据具体字段类型，生成具体的规则对象
    def getViewObj(self,type):
        if type == 'Integer':
            return IntegerView()

        elif type == 'Varchar':
            return VarcharView()

        elif type == 'TimeStamp':
            return TimeStampView()

        else:
            return None
    #获取所有规则对象
    def getParams(self,key):
        return self._params[key].getParams()
    #为某个具体字段属性，设置具体的规则参数
    def setParams(self,key,params):
        self._params[key].setParams(params)


class _RView:
    '''
    规则UI，接口
    '''
    #渲染
    def render(self,node,row):
        self._draw(node,row)
        pass
    #具体元素
    def _draw(self,node):
        pass

    #获取规则参数
    def getParams(self):
        pass
    #设置规则参数
    def setParams(self,params):
        pass

class IntegerView(_RView):
    '''
    整数生成规则 视图模板
    参数包括 开始值，结束值，步长
    '''
    def __init__(self):
        pass
        self.startVar = tkinter.IntVar()
        self.endVar = tkinter.IntVar()
        self.stepVar = tkinter.IntVar()
    def _draw(self,node,row):

        # frm = tkinter.Frame(node)
        # tkinter.Label(frm,text='开始值').pack(side=tkinter.LEFT)
        # self.start = tkinter.Entry(frm,textvariable=self.startVar)
        # self.start.pack(side=tkinter.LEFT)
        # tkinter.Label(frm,text='结束值').pack(side=tkinter.LEFT)
        # self.end = tkinter.Entry(frm,textvariable=self.endVar)
        # self.end.pack(side=tkinter.LEFT)
        # tkinter.Label(frm,text='步长').pack(side=tkinter.LEFT)
        # self.step = tkinter.Entry(frm,textvariable=self.stepVar)
        # self.step.pack(side=tkinter.LEFT)
        # frm.pack(side=tkinter.LEFT)


        tkinter.Label(node,text='开始值').grid(row=row,column=1)
        self.start = tkinter.Entry(node,textvariable=self.startVar)
        self.start.grid(row=row,column=2)
        tkinter.Label(node,text='结束值').grid(row=row,column=3)
        self.end = tkinter.Entry(node,textvariable=self.endVar)
        self.end.grid(row=row,column=4)
        tkinter.Label(node,text='步长').grid(row=row,column=5)
        self.step = tkinter.Entry(node,textvariable=self.stepVar)
        self.step.grid(row=row,column=6)

        pass
    def getParams(self):
        params ={
            'start':self.start.get(),
            'end':self.end.get(),
            'step':self.step.get()
        }
        V = IntegerRule(params)
        if(V.validate()): # 验证数据是否符合规则
            return params
        return V.getError()
    def setParams(self,params):
        if(params.get('start')):
            self.start.insert(0,params.get('start'))
            self.end.insert(0,params.get('end'))
            self.step.insert(0,params.get('step'))

class VarcharView(_RView):
    '''
    字符串生成规则 视图
    参数包括 字符串前缀，开始值，结束值，步长
    '''
    def _draw(self,node,row):
        tkinter.Label(node,text='开始值').grid(row=row,column=1)
        self.start = tkinter.Entry(node)
        self.start.grid(row=row,column=2)
        tkinter.Label(node,text='结束值').grid(row=row,column=3)
        self.end = tkinter.Entry(node)
        self.end.grid(row=row,column=4)
        tkinter.Label(node,text='步长').grid(row=row,column=5)
        self.step = tkinter.Entry(node)
        self.step.grid(row=row,column=6)
        tkinter.Label(node,text='前缀字符').grid(row=row,column=7)
        self.prefix = tkinter.Entry(node)
        self.prefix.grid(row=row,column=8)
    def getParams(self):
        params = {
            'prefix':self.prefix.get(),
            'start':self.start.get(),
            'end':self.end.get(),
            'step':self.step.get()
        }
        V = VarcharRule(params)
        if(V.validate()):
            return params
        return V.getError()
    def setParams(self,params):
        if params.get('prefix'):
            self.prefix.insert(0,params.get('prefix'))
            self.start.insert(0,params.get('start'))
            self.end.insert(0,params.get('end'))
            self.step.insert(0,params.get('step'))


class TimeStampView(_RView):
    '''
    时间生成规则 视图
    参数包括:开始时间，结束时间，步长
    '''
    def _draw(self,node,row):
        tkinter.Label(node, text='开始时间').grid(row=row,column=1)
        self.start = tkinter.Entry(node)
        self.start.grid(row=row,column=2)

        tkinter.Label(node,text='结束时间').grid(row=row,column=3)
        self.end = tkinter.Entry(node)
        self.end.grid(row=row,column=4)

        tkinter.Label(node,text='步长').grid(row=row,column=5)
        self.step = tkinter.Entry(node)
        self.step.grid(row=row,column=6)

        pass
    def getParams(self):
        '''
            验证时间:
                params dict:
                    now:是否直接获取当前时间 如果为真，其他选项无效
                    start:开始时间 时间格式 xxxx-xx-xx xx:xx:xx
                    end:结束时间
                    step:步长
                    unit:增长单位  M：分 H：时 S:秒 d:天
        '''
        params = {
            'start':self.start.get(),
            'end':self.end.get(),
            'step':self.step.get()
        }
        V = TimeStampRule(params)
        if(V.validate()):
            return params
        return V.getError()
    def setParams(self,params):
        if params.get('start'):
            # self.prefix.insert(0,params.get('prefix'))
            self.start.insert(0,params.get('start'))
            self.end.insert(0,params.get('end'))
            self.step.insert(0,params.get('step'))