import time
import tkinter
from logs._ILog import _ILog
class InsertLog(_ILog):
    def __init__(self,parent):
        super().__init__(parent)
        self._listParams = {}
        tkinter.Label(self._parent, text='名称').grid(row=self._rowNum, column=0, padx=20, pady=5)
        tkinter.Label(self._parent, text='执行次数').grid(row=self._rowNum, column=1, padx=20, pady=5)
        tkinter.Label(self._parent, text='插入总数').grid(row=self._rowNum, column=2, padx=20, pady=5)
        tkinter.Label(self._parent, text='状态').grid(row=self._rowNum, column=3, padx=20, pady=5)
        tkinter.Label(self._parent, text='开始时间').grid(row=self._rowNum, column=4, padx=20, pady=5)
        self._rowNum +=1
    def add(self,key):
        if self._list.get(key) is None:
            self.draw(key)
        pass

    def update(self,key,execute_ct=False,total=False,status=False):
        '''

        :param key:表名
        :param execute_ct:执行次数
        :param total: 共插入数据的总数
        :param status: 当前状态
        :return:
        '''
        if self._list.get(key) is None:
            return False
        if execute_ct is not False:
            self._setExecuteCt(key, execute_ct)
        if total is not False:
            self._setTotal(key, total)
        if status is not False:
            self._setStataus(key, status)
    #设置执行次数
    def _setExecuteCt(self, key, execute_ct):
        self._list[key][0]['text'] = execute_ct

    #设置总数
    def _setTotal(self, key, total):
        self._list[key][1]['text'] = total

    #设置当前程序运行状态
    def _setStataus(self, key, status):
        self._list[key][2]['text'] = status

    #渲染布局
    def draw(self,key):
        tkinter.Label(self._parent,text=key).grid(row=self._rowNum, column=0, padx=20, pady=5)
        execute_ct = tkinter.Label(self._parent, text='0')
        execute_ct.grid(row=self._rowNum, column=1, padx=20, pady=5)
        total = tkinter.Label(self._parent, text='0')
        total.grid(row=self._rowNum, column=2, padx=20, pady=5)
        status =  tkinter.Label(self._parent, text='未开始')
        status.grid(row=self._rowNum, column=3, padx=20, pady=5)
        tkinter.Label(self._parent, text=time.strftime('%Y-%m-%d %H:%M:%S')).grid(row=self._rowNum, column=4, padx=20, pady=5)

        self._list[key] = (execute_ct,total,status)
        self._rowNum += 1
        pass