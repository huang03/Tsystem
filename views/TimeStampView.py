import tkinter
from tkinter import ttk
from views._IView import _IView
from rules2.DB_TimeStampRule import TimeStampRule
from tkinter.messagebox import *
class TimeStampView(_IView):
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

        self._start = tkinter.IntVar()
        tkinter.Label(self._commonFrm,text='开始时间：').grid(row=0,column=0)
        tkinter.Entry(self._commonFrm,textvariable=self._start).grid(row=0,column=1)

        self._end = tkinter.IntVar()
        tkinter.Label(self._commonFrm,text='结束时间：').grid(row=1,column=0)
        tkinter.Entry(self._commonFrm,textvariable=self._end).grid(row=1,column=1)

        self._step = tkinter.IntVar()
        tkinter.Label(self._commonFrm,text='步长：').grid(row=2,column=0)
        tkinter.Entry(self._commonFrm,textvariable=self._step).grid(row=2,column=1)

        self._uint = tkinter.StringVar()
        tkinter.Label(self._commonFrm, text='单位：').grid(row=3, column=0)
        tmpUnit =  ttk.Combobox(self._commonFrm,  textvariable=self._uint)
        tmpUnit.grid(row=3,column=1)
        #S：秒 M：分 H：时 d: 天
        tmpUnit['values'] = ('秒','分','时','天')
        tmpUnit.current(0)

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

            '表属性':self._tableFrm,
            'SQL':self._sqlFrm
        }

        typeChosen['values'] = ('常规','当前时间', '表属性', 'SQL')  # 设置下拉列表的值
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
        mapType = { 'COMMAN':'常规',  'NOW':'当前时间',  'TABLE':'表属性', 'SQL': 'SQL'}
        self._start.set(params['start'])
        self._end.set(params['end'])
        self._step.set(params['step'])
        self._table.set(params['table'])
        self._sql.set(params['sql'])
        self._uint.set(params['unit'])
        self._type.set(mapType[params['_TYPE_']])
        self.choiceType()
        pass
    def _validate(self):
        mapType = {'常规': 'COMMAN', '当前时间': 'NOW', '表属性': 'TABLE', 'SQL': 'SQL'}
        try:
            self.params = {
             #   'prefix':self._prefix.get(),
                'start':self._start.get(),
                'end':self._end.get(),
                'step':self._step.get(),
                #'list':self._list.get(),
                'table':self._table.get(),
                'sql':self._sql.get(),
                'unit':self._uint.get(),
                '_TYPE_':mapType[self._type.get()]
            }
        except Exception as E:
            return False
            print(E)

        V = TimeStampRule(self.params);
        if not V.validate(mapType[self._type.get()]):
            showwarning('Warning', ' %s' % V.getError() )
            return False
        else:
            return True
