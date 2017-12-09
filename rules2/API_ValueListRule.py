from rules2._IRule import _IRule

class ValueListRule(_IRule):
    def __init__(self,params):
        params = params.strip()
        self.len = 0
        if params is not '':
            params = params.split(',')
            self.len = len(params)
        super().__init__(params)
        self.index = 0;
    def validate(self):
        if self.len < 1:
            self._setError('the value can not be empty')
            return False
        return True
        # if len(self.params) > 0:
        #     return self.params[0]
        # else:
        #     self._setError('the value can not be empty')
        # return False
        pass
    def getValue(self):
        tmp = None;
        if self.index >= self.len:

            self.index = 0
        tmp = self.params[self.index]
        self.index += 1
        return tmp
        # tmp = self.params.split(',')
        # if len(tmp)>0:
        #     return tmp[0]
        # return False
    pass