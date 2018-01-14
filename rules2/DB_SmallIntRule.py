from rules2._IRule import _IRule
class SmallIntRule(_IRule):
    def __init__(self,params):
        super().__init__(params)
        self._currValue = None

    def _validateComman(self):
        if not self.params.get('start') or (
                type(self.params.get('start')) is not type(1) and not self.params.get('start').isdigit()):
            self._setError('start must be Interger')
            return False
        if type(self.params.get('end')) is not type(1) and not self.params.get('end').isdigit():
            self._setError('end must be Interger')
            return False

        if int(self.params.get('end'))>32767:
            self._setError('the range of SmallInt is 0 between to 32767')
            return False

        if type(self.params.get('step')) is not type(1) and not self.params.get('step').isdigit():
            self._setError('step must be Interger')
            return False

        self.params['start'] = int(self.params['start'])
        self.params['end'] = int(self.params['end'])
        self.params['step'] = int(self.params['step'])
        if self.params.get('start') > self.params.get('end'):
            self._setError('end must bigger than start ')
            return False
        return True
    def _getCommanValue(self):
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


