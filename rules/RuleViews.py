# -*- coding: utf-8 -*-
import tkinter
class renderViews:
    def __init__(self):
        self._objs = {}
    def render(self,key,node):
        obj = self.getViewObj(key)
        obj.render(node)
    def getViewObj(self,key):
        if not self._objs.get(key):
            if key == 'Integer':
                self._objs[key] = IntegerView()
            elif key == 'Varchar':
                self._objs[key] = VarcharView()
            elif key == 'StampTime':
                self._objs[key] = StampTimeView()
            else:
                return None

        return self._objs.get(key)

class _RView:

    def render(self,node):
        self._draw(node)
        pass
    def _draw(self,node):
        pass

class IntegerView(_RView):
    def _draw(self,node):
        frm = tkinter.Frame(node)
        startVar = tkinter.IntVar()
        endVar = tkinter.IntVar()
        stepVar = tkinter.IntVar()
        tkinter.Label(frm,text='开始值').pack(side=tkinter.LEFT)
        tkinter.Entry(frm,textvariable = startVar).pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='结束值').pack(side=tkinter.LEFT)
        tkinter.Entry(frm,textvariable = endVar).pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='步长').pack(side=tkinter.LEFT)
        tkinter.Entry(frm,textvariable = stepVar).pack(side=tkinter.LEFT)
        frm.pack(side=tkinter.TOP,fill=tkinter.BOTH)
        pass
    pass

class VarcharView(_RView):
    def _draw(self,node):
        frm = tkinter.Frame(node)
        prefixVar = tkinter.StringVar()
        startVar = tkinter.IntVar()
        endVar = tkinter.IntVar()
        stepVar = tkinter.IntVar()
        tkinter.Label(frm,text='前缀字符').pack(side=tkinter.LEFT)
        tkinter.Entry(frm, textvariable=prefixVar).pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='开始值').pack(side=tkinter.LEFT)
        tkinter.Entry(frm,textvariable = startVar).pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='结束值').pack(side=tkinter.LEFT)
        tkinter.Entry(frm,textvariable = endVar).pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='步长').pack(side=tkinter.LEFT)
        tkinter.Entry(frm,textvariable = stepVar).pack(side=tkinter.LEFT)
        frm.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        pass

class StampTimeView(_RView):
    def _draw(self,node):
        frm = tkinter.Frame(node)
        startVar = tkinter.StringVar()
        endVar = tkinter.StringVar()
        stepVar = tkinter.IntVar()
        tkinter.Label(frm,text='开始时间').pack(side=tkinter.LEFT)
        tkinter.Entry(frm,textvariable = startVar).pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='结束时间').pack(side=tkinter.LEFT)
        tkinter.Entry(frm,textvariable = endVar).pack(side=tkinter.LEFT)
        tkinter.Label(frm,text='步长').pack(side=tkinter.LEFT)
        tkinter.Entry(frm,textvariable = stepVar).pack(side=tkinter.LEFT)
        frm.pack(side=tkinter.TOP,fill=tkinter.BOTH)
        pass