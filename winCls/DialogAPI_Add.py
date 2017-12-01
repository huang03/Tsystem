import tkinter,json
from tkinter.messagebox import *
from dbs.MysqlT import MysqlT
class DialogAPI_Add(tkinter.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('API ADD')
        self.geometry('600x400')
        navsFrame = tkinter.Frame(self)
        tkinter.Button(navsFrame,text='add property',command=self.add).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame,text='delete').pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame, text='Ok',command=self.submit).pack(side=tkinter.LEFT)
        navsFrame.pack(side=tkinter.TOP,fill='x')



        tFrame = tkinter.Frame(self)
        self.title = tkinter.StringVar(tFrame)
        tkinter.Label(tFrame,text='Name',width=10).pack(side=tkinter.LEFT)
        tkinter.Entry(tFrame,textvariable=self.title).pack(side=tkinter.LEFT)
        tFrame.pack(side=tkinter.TOP,fill='x')

        uFrame = tkinter.Frame(self)
        self.url = tkinter.StringVar(uFrame)
        tkinter.Label(uFrame,text='API',width=10).pack(side=tkinter.LEFT)
        tkinter.Entry(uFrame,textvariable=self.url).pack(side=tkinter.LEFT)
        uFrame.pack(side=tkinter.TOP,fill='x')

        rFrame = tkinter.Frame(self)
        self.requestType = tkinter.StringVar(rFrame)
        tkinter.Label(rFrame,text='TYPE',width=10).pack(side=tkinter.LEFT)
        Options = ["GET", "POST"]
        self.requestType.set(Options[0])
        tkinter.OptionMenu(rFrame,self.requestType,*Options).pack(side=tkinter.LEFT)
        # tkinter.Entry(rFrame,textvariable=self.url).pack(side=tkinter.LEFT)
        rFrame.pack(side=tkinter.TOP,fill='x')


        self.apis = tkinter.Frame(self)
        tkinter.Label(self.apis,text='Property:').pack(side=tkinter.TOP,fill='x')
        self.apis.pack(side=tkinter.TOP,fill='x')
        self.row = 0


        # self.choices = [];
        self.values = [];
        # self.Apis = tkinter.Listbox(self,width=500,height=200)
        # self.Apis.pack(side=tkinter.TOP,fill='x')

    def add(self):
        print(self.isEmpty())
        if not self.isEmpty():
            showinfo('Tip','please to sure the data of the last row is complete ')
            return False
        frm = tkinter.Frame(self.apis)
        choice = tkinter.StringVar(frm)
        var = tkinter.StringVar(frm)
        name = tkinter.StringVar(frm)
        self.values.append({'type':choice,'value':var,'name':name});

        tkinter.Label(frm,text='Name：').grid(row=self.row,column=0)
        tkinter.Entry(frm,textvariable=name).grid(row=self.row, column=1)

        Options = ["定值", "范围", "默认"]
        tkinter.OptionMenu(frm,choice,*Options).grid(row=self.row,column=2)
        tkinter.Entry(frm,textvariable=var).grid(row=self.row, column=3)
        row = self.row
        tkinter.Button(frm,text='delete',command=lambda :self.delete(frm,row)).grid(row=self.row, column=4)
        frm.pack(side=tkinter.TOP,fill='x')
        self.row += 1
        pass
    def delete(self,parent,row):
        parent.destroy()
        del self.values[row]
        self.row -= 1
        pass
    def isEmpty(self):
        for v in self.values:
            if v['name'].get() is '':
                return False
            if v['value'].get() is '':
                return False
            if v['type'].get() is '':
                return False
        return True
    def submit(self):
        if self.title.get() is '':
            showinfo('Tip','Name must input')
            return False
        if self.url.get() is '':
            showinfo('Tip','API must input')
            return False
        if len(self.values)<1:
            showinfo('Tip','At least one property ')
            return False
        if not self.isEmpty():
            showinfo('Tip','please full with data for all')
            return False
        datas = {}
        for v in self.values:
            key = v['name'].get()
            datas[key] = {
                'type':v['type'].get(),
                'value':v['value'].get()
            }
        operator = MysqlT()
        RTYPES = {'POST':1,'GET':0}
        data = ('1', self.url.get(), self.title.get(),RTYPES[self.requestType.get()])
        # return True;
        try:
            result0 = operator.add({
                'table':'tsys_api_items',
                'field': ('user_id', 'api', 'title','type'),
                'binds': data
            })
        except Exception as E:
            print(E)
        id = operator.getLastId()
        if result0:
            result1 = operator.add({
                'table':'tsys_api_items_detail',
                'field':('property','item_id'),
                'binds':(json.dumps(datas),id)
            })
            if result1:
                showinfo('Tip','Success')
                operator.commit()
                self.destroy()
                return True
        operator.rollback()
        return False
    def rendFixedValue(self,parent):
        tkinter.Entry(parent).grid(row=self.row,column=3)
        pass
    def rendview(self):
        pass
