class _IRule:
    '''
        规则类接口
        validate: 验证规则合法性
        getError
        setError

        getValue:根据规则生成数据

        属性
         _metas:元数据
         _error:错误列表
         _GrtData:生成数据的类
    '''
    def __init__(self,params):
        self.params = params
        self._error = None
    def validate(self):
        pass
    def getError(self):
        return self._error
    def _setError(self,error):
        self._error = error
    #
    # def getMetas(self):
    #     return self.params
    #
    # def setMetas(self,params):
    #     self._metas = params
    #     del params
    def getValue(self):
        return self.params
        pass;
