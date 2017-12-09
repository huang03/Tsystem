from rules2._IRule import _IRule

class DefaultValueRule(_IRule):
    def __init__(self,params):
        params = params.strip()
        super().__init__(params)

    def validate(self):

        return True
    def getValue(self):
        #self.params = self.params.strip()
        return self.params
    pass