import tkinter
from tkinter import ttk
from views._IView import _IView
from rules2.DB_VarcharRule import VarcharRule
from tkinter.messagebox import *
class VarcharView(_IView):
    def __init__(self):
        super().__init__()
        self.title('hello')
        self.geometry('%dx%d+%d+%d' % self.center_window(500, 250))
        self.params = {}

        self._type = tkinter.StringVar()
        typeChosen = ttk.Combobox(self, width=50, textvariable=self._type)
        typeChosen.pack(side=tkinter.TOP)

        self._commonFrm = tkinter.Frame(self)
        self._commonFrm.pack(side=tkinter.TOP,fill='x')
        self._prefix = tkinter.StringVar()
        tkinter.Label(self._commonFrm,text='前缀：').grid(row=0,column=0)
        tkinter.Entry(self._commonFrm,textvariable=self._prefix).grid(row=0,column=1)

        self._start = tkinter.IntVar()
        tkinter.Label(self._commonFrm,text='开始值：').grid(row=1,column=0)
        tkinter.Entry(self._commonFrm,textvariable=self._start).grid(row=1,column=1)

        self._end = tkinter.IntVar()
        tkinter.Label(self._commonFrm,text='结束值：').grid(row=2,column=0)
        tkinter.Entry(self._commonFrm,textvariable=self._end).grid(row=2,column=1)

        self._step = tkinter.IntVar()
        tkinter.Label(self._commonFrm,text='步长：').grid(row=3,column=0)
        tkinter.Entry(self._commonFrm,textvariable=self._step).grid(row=3,column=1)

        self._listFrm = tkinter.Frame(self)
        self._list = tkinter.StringVar()
        tkinter.Label(self._listFrm,text='指定列表：').grid(row=1,column=0) #TYPE LIST
        tkinter.Entry(self._listFrm,textvariable=self._list).grid(row=1,column=1)
        self._listFrm.pack(side=tkinter.TOP, fill='x')

        self._tableFrm = tkinter.Frame(self)
        self._table = tkinter.StringVar()
        tkinter.Label(self._tableFrm,text='表中属性：').grid(row=1,column=0) #TYPE TABLE
        tkinter.Entry(self._tableFrm,textvariable=self._table).grid(row=1,column=1)
        self._tableFrm.pack(side=tkinter.TOP, fill='x')

        #separator.pack(fill=X, padx=5, pady=5)
        self._sqlFrm = tkinter.Frame(self)
        self._sql = tkinter.StringVar()
        tkinter.Label(self._sqlFrm,text='SQL：').grid(row=1,column=0) # SQL
        tkinter.Entry(self._sqlFrm,textvariable=self._sql).grid(row=1,column=1)
        self._sqlFrm.pack(side=tkinter.TOP, fill='x')

        self._okBtn = tkinter.Button(self,text='OK',command=self.getParams)
        self._okBtn.pack(side=tkinter.TOP)

        self._typeList = {
            '常规':self._commonFrm,
            '指定列表':self._listFrm,
            '表属性':self._tableFrm,
            'SQL':self._sqlFrm
        }

        typeChosen['values'] = ('常规', '指定列表', '表属性', 'SQL')  # 设置下拉列表的值
        typeChosen.current(0)
        typeChosen.bind("<<ComboboxSelected>>",self.choiceType)
        self.choiceType()
    def choiceType(self,*args):  # 处理事件，*args表示可变参数
        type = self._type.get();
        self._okBtn.pack_forget()
        for key in self._typeList:
            if key == type:
                self._typeList[key].pack(side=tkinter.TOP, fill='x')
            else:
                self._typeList[key].pack_forget()
        self._okBtn.pack(side=tkinter.TOP)

    def getParams(self):
        if not self._validate():
            return False
        return self.params
        pass
    def setParams(self,params):
        mapType = { 'COMMAN':'常规',  'LIST':'指定列表',  'TABLE':'表属性', 'SQL': 'SQL'}
        self._prefix.set(params['prefix'])
        self._start.set(params['start'])
        self._end.set(params['end'])
        self._step.set(params['step'])
        self._list.set(params['list'])
        self._table.set(params['table'])
        self._sql.set(params['sql'])
        self._type.set(mapType[params['_TYPE_']])
        self.choiceType()
        # typeChosen.current(self.mapIndex[params['_TYPE']])
        pass
    def _validate(self):
        mapType = {'常规': 'COMMAN', '指定列表': 'LIST', '表属性': 'TABLE', 'SQL': 'SQL'}
        try:
            self.params = {
                'prefix':self._prefix.get(),
                'start':self._start.get(),
                'end':self._end.get(),
                'step':self._step.get(),
                'list':self._list.get(),
                'table':self._table.get(),
                'sql':self._sql.get(),
                '_TYPE_':mapType[self._type.get()]
            }
        except Exception as E:
            return False
            print(E)

        V = VarcharRule(self.params);
        if not V.validate(mapType[self._type.get()]):
            showwarning('Warning', ' %s' % V.getError() )
            return False
        else:
            return True

# if __name__ == '__main__':
#     root = tkinter.Tk()
#     a = VarcharView()
#     a.mainloop()