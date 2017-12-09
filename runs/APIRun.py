import Constants
from runs.IRun import IRun
from rules2.API_RangeRule import RangeRule
from rules2.API_ValueListRule import ValueListRule
from rules2.API_DefaultValueRule import DefaultValueRule
from VisitUrl import VisitUrl
from runs.Runs import Runs
class APIRun(IRun):
    def __init__(self,operator):
        super().__init__(operator)
        self._params = {}
    def addTaskParams(self,url,requestType):
        self._params = {'url':url,'requestType':requestType}
    def run(self):
        params = ''
        if self._params['requestType'] is Constants.REQUEST_TYPE['GET']:
            params = self._getParamsOfGet()
            url = self._params['url'] + params
            if not self._operator.getRequest(url):
                self._setError(self._operator.getError())
            print(self._operator.getContent())
        else:
            params = self._getParamsOfPost()
            if not self._operator.postRequest(self._params['url'],params):
                self._setError(self._operator.getError())
            # print(self._VisitUrl.getContent())
            pass
        return True
        pass
    def _getParamsOfGet(self):
         data = '?';
         for property in self._rules:
             # print(property)
             ruleObj = self._rules[property]
             value = str(ruleObj.getValue())
             # print(ruleObj.getValue())
             data = data + property + '=' + value + '&'
         data = data.strip('&')
         return data;
    def _getParamsOfPost(self):
        data = {}
        for property in self._rules:
            ruleObj = self._rules[property]
            data[property] = ruleObj.getValue
        return data
    pass

if __name__ == '__main__':
    visit = VisitUrl()
    RUN = APIRun(visit)
    DObj = DefaultValueRule('1121')
    Vojb = ValueListRule('1,2,3,4')
    RObj = RangeRule('1,10')
    RUN.addTaskParams('http://127.0.0.1/py_test.php',0)
    RUN.addTask('a',DObj)
    RUN.addTask('b',Vojb)
    RUN.addTask('c',RObj)

    RS = Runs()
    RS.addRunObj(RUN)
    RS.run()
    RUN.run()
