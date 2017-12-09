from rules2._IRule import _IRule
from rules2.DB_IntegerRule import IntegerRule
class VarcharRule(_IRule):
    def __init__(self,params):
        super().__init__(params)
        self._currValue = None
        self._RInteger = IntegerRule(self.params);
    def validate(self):
        # RInteger = IntegerRule(self.params)
        if not self._RInteger.validate():
            self._setError(self._RInteger.getError())
            return False
        if not self.params.get('prefix'):
            self.params['prefix'] = 'tsys-'
        return True
    def getValue(self):
        if not self.params:
            self._currValue =None
        currValue = self._RInteger.getValue()
        if not currValue:
            self._currValue = self.params['prefix']
        self._currValue =  self.params['prefix'] + '%s' % currValue
        return self._currValue
    pass

if __name__ == '__main__':
    params = {'start':'1','end':10,'step':2}
    R = VarcharRule(params)
    if not R.validate():
        print(R.getError())
    else:
        print(R.getValue())
        print(R.getValue())
        print(R.getValue())
        print(R.getValue())