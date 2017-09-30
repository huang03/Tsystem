
from rules.Rules import *
from rules.RulePackages import RPackages
from rules.GenerateData import IntegerGenerate,VarcharGenerate,TimeStampGenerate
from rules.DefaultValue import *
from rules.RuleViews import *
import tkinter
import time
import threading
# go = True
# def printHello():
#     global go
#     while go:
#         print('Hello')
#         print(go)
#         time.sleep(1)
# def goRun():
#     t1 = threading.Thread(target=printHello)
#     t1.start()
# def setGo():
#     global go
#     go = False
#     print(go)


#Show Tables 查询数据库的所有表
#show columns from tbl_role  查询表中的所有字段属性
def openWindow():
    print('1111')
    top = tkinter.Toplevel()
    top.title('Hello')
    top.iconify()
def main():
    root = tkinter.Tk()
    root.title('hello world')
    root.geometry('800x200')
    navsFrame =  tkinter.Frame(root)

    tkinter.Button(navsFrame, text='接口', width=10, command=openWindow).pack(side=tkinter.LEFT)

    rulesFrame = tkinter.Frame(root)
    logsFrame = tkinter.Frame(root)

    #navFrame.grid(row=0)
    #ruleFrame.grid(row=1)

    # tkinter.Button(root, text='press', command=goRun).pack()
    # tkinter.Button(root, text='close', command=setGo).pack()
    renders = renderViews();
   # renders.render('Integer',navsFrame)
    renders.render('Varchar',rulesFrame)
    renders.render('StampTime', logsFrame)
    navsFrame.pack(side=tkinter.TOP,fill=tkinter.BOTH)
    rulesFrame.pack(side=tkinter.TOP,fill=tkinter.BOTH)
    logsFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH)

    root.mainloop()
    pass
    # params = {
    #     'start':'2017-09-20 10:10:10',
    #     'end':'2017-09-25 11:10:10',
    #     'step':-1,
    #     'unit':'d'
    # }
    # params1 = {
    #     'start':'2017-09-20 10:10:10',
    #     'end':'2017-09-25 11:10:10',
    #     'step':-1,
    #     'unit':'d'
    # }
    # packages = RPackages()
    # packages.add('xt_key')
    # A = TimeStampRule(params)
    # print(A.validate())
    # return True
    # A1 = TimeStampRule(params)
    # print(A1.validate())
    # packages.addRule('xt_key','tm',A)
   # print(params)
   #  packages.addRule('xt_key2', 'tm', A1)
    # params = {
    #     'start':1,
    #     'end':20,
    #     'step':1,
    # }
    # B = IntegerRule(params)
    # B1 = IntegerRule(params)
    # packages.addRule('xt_key', 'role', B)
    # packages.addRule('xt_key2', 'role', B1)
    # #print(packages.getRules())
    # packages.runs()
    # print(packages.getError())
    #AA = {'a':1}
    #a = 'a'
    #print(AA.get[a])
    # A = TimeStampRule()
    # if A.validate(params):
    #     B = TimeStampGenerate(A)
    #     print(B.getValue())
    #     print(B.getValue())
    #    # print(B.getValue())
    #     #print(B.getValue())
    # else:
    #     print(A.getError())
if __name__ == '__main__':
    main()