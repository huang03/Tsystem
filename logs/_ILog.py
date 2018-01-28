class _ILog:
    '''
        Log 记录操作
    '''
    def __init__(self, parent):
        self._list = {} #log记录列表
        self._parent = parent #记录需要显示在哪个布局
        self._rowNum = 0;
        pass;
    def add(self,key): #添加log
        pass
    def draw(self): #渲染布局
        pass
    def update(self,key): #更新log
        pass