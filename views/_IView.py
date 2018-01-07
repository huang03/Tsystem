import tkinter
class _IView(tkinter.Toplevel):

    def center_window(self, w, h):
        # 获取屏幕 宽、高
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        return (w, h, x, y)
    def getParams(self):
        pass
    def setParams(self):
        pass

    def _validate(self):
        pass