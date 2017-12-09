class IRun:
    def __init__(self,operator):
        self._rules = {}
        self._operator = operator
        self._error = None
    def addTask(self,property,rule,url=None,requestType=None):

        self._rules[property] = rule;
    def deleteTask(self,property):
        if self._rules.get(property):
            del self._rules[property]
    def run(self):

        pass
    def _setError(self,error):
        self._error = error
    def getError(self):
        return self._error