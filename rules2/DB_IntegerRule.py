from rules2._IRule import _IRule
class IntegerRule(_IRule):
    def __init__(self,params):
        super().__init__(params)
        self._currValue = None
    def validate(self):
        # isinstance()
        if type(self.params.get('start')) is not type(1) and not self.params.get('start').isdigit():
            self._setError('start must be Interger')
            return False
        if type(self.params.get('end')) is not type(1) and not self.params.get('end').isdigit():
            self._setError('end must be Interger')
            return False
        if type(self.params.get('step')) is not type(1) and not self.params.get('step').isdigit():
            self._setError('step must be Interger')
            return False
        self.params['start'] = int(self.params['start'])
        self.params['end'] = int(self.params['end'])
        self.params['step'] = int(self.params['step'])
        if self.params.get('start') > self.params.get('end'):
            self.setError('end must bigger than start ')
            return False
        # del params
        # self.setMetas(params)
        return True
    def getValue(self):
        if not self.params:
            self._currValue = None
            return False
        if self._currValue:
            self._currValue += self.params['step']
        else:
            self._currValue = self.params['start']
        if self._currValue > self.params['end']:
            self._currValue = self.params['start']
        return self._currValue
    pass


if __name__ == '__main__':
    params = {'start':1,'end':10,'step':2}
    R = IntegerRule(params)
    if not R.validate():
        print(R.getError())
    else:
        print(R.getValue())
        print(R.getValue())
        print(R.getValue())
        print(R.getValue())


