import tkinter

class _IView(tkinter.Toplevel):
    '''
     类型配置界面
    '''

    #设计弹出框居中显示
    def center_window(self, w, h):
        # 获取屏幕 宽、高
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        return (w, h, x, y)
    #获取参数
    def getParams(self):
        pass
    #设置参数
    def setParams(self):
        pass
    #验证用户设置参数的有效性
    def _validate(self):
        pass