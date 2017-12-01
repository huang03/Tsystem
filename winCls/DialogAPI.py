import tkinter
from winCls.DialogAPI_Add import DialogAPI_Add
class DialogAPI(tkinter.Toplevel):
    def __init__(self,parent):
        super().__init__()
        self.title('API')
        self.parent = parent
        self.geometry('%dx%d+%d+%d' % self.parent.center_window(800,400))
        navsFrame = tkinter.Frame(self)
        tkinter.Button(navsFrame,text='add',command=self.add).pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame,text='delete').pack(side=tkinter.LEFT)
        tkinter.Button(navsFrame,text='update').pack(side=tkinter.LEFT)
        navsFrame.pack(side=tkinter.TOP,fill='x')


    def add(self):
        dialog = DialogAPI_Add()
        pass
    def delete(self):
        pass
    def update(self):
        pass