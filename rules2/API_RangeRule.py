from rules2._IRule import _IRule
import random
class RangeRule(_IRule):
    def __init__(self,params):
        params = params.strip()
        self.len = 0
        if params is not '':
            params = params.split(',')
            self.len = len(params)
        super().__init__(params)

    def validate(self):
        if self.len<2:
            self._setError('the format of Range Value is xx,xx and  Integer')
            return False
        return True
        pass
    def getValue(self):
        start = int(self.params[0])
        end = int(self.params[1])

        return random.randint(start, end)
        pass
    pass