# -*- coding: utf-8 -*-
import tkinter
from rules.Rules import IntegerRule,VarcharRule,TimeStampRule
class renderViews:
    '''
        为每个表的字段属性，生成具体的UI，以便用户为每个字段输入具体执行规则
    '''
    def __init__(self):
        self._params = {} #记录字段生成数据的具体规则对象
    def render(self,key,type,node):
        obj = self.getViewObj(type)
        obj.render(node)
        self._params[key] = obj
    #根据具体字段类型，生成具体的规则对象
    def getViewObj(self,type):
        if type == 'Integer':
            return IntegerView()

        elif type == 'Varchar':
            return VarcharView()

        elif type == 'StampTime':
            return StampTimeView()

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
    def render(self,node):
        self._draw(node)
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
    def _draw(self,node):

        frm = tkinter.Frame(node)
        tkinter.Label(frm,text='开始值').pack(side=tkinter.LEFT)
        self.start = tkinter.Entry(frm,textvariable=self.startVar)
        self.start.pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='结束值').pack(side=tkinter.LEFT)
        self.end = tkinter.Entry(frm,textvariable=self.endVar)
        self.end.pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='步长').pack(side=tkinter.LEFT)
        self.step = tkinter.Entry(frm,textvariable=self.stepVar)
        self.step.pack(side=tkinter.LEFT)
        frm.pack(side=tkinter.TOP,fill=tkinter.BOTH)
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
    def _draw(self,node):
        frm = tkinter.Frame(node)
        tkinter.Label(frm,text='前缀字符').pack(side=tkinter.LEFT)
        self.prefix = tkinter.Entry(frm)
        self.prefix.pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='开始值').pack(side=tkinter.LEFT)
        self.start = tkinter.Entry(frm)
        self.start.pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='结束值').pack(side=tkinter.LEFT)
        self.end = tkinter.Entry(frm)
        self.end.pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='步长').pack(side=tkinter.LEFT)
        self.step = tkinter.Entry(frm)
        self.step.pack(side=tkinter.LEFT)
        frm.pack(side=tkinter.TOP, fill=tkinter.BOTH)
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


class StampTimeView(_RView):
    '''
    时间生成规则 视图
    参数包括:开始时间，结束时间，步长
    '''
    def _draw(self,node):
        frm = tkinter.Frame(node)
        tkinter.Label(frm,text='开始时间').pack(side=tkinter.LEFT)
        self.start = tkinter.Entry(frm)
        self.start.pack(side=tkinter.LEFT)

        tkinter.Label(frm,text='结束时间').pack(side=tkinter.LEFT)
        self.end = tkinter.Entry(frm)
        self.end.pack(side=tkinter.LEFT)

        tkinter.Label(frm,text='步长').pack(side=tkinter.LEFT)
        self.step = tkinter.Entry(frm)
        self.step.pack(side=tkinter.LEFT)

        frm.pack(side=tkinter.TOP,fill=tkinter.BOTH)
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
        return {
            'start':self.start.get(),
            'end':self.end.get(),
            'step':self.step.get()
        }