from rules2.RuleFactory import RuleFactory
class _IValidate:
    def __init__(self):
        self._error = None
        self._properties = {}
        self._ruleFactory = RuleFactory()
    def addProperty(self,property,data):
        self._properties[property] =self._ruleFactory(data['type'],data['value'])
    def validate(self):
        pass
    def getError(self):
        return self._error
    def _setError(self,error):
        self._error = error

    pass