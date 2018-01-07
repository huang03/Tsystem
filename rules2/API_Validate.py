import Constants
from VisitUrl import VisitUrl
from rules2._IValidate import _IValidate

class APIValidate(_IValidate):
    def __init__(self):
        super().__init__()
        self._params = {}
        self.Visit = VisitUrl()
    def addExtraParams(self,title,url,requestType):
        self._params['title'] = title
        self._params['url'] = url
        self._params['requestType'] = requestType
    def validate(self):
        if self._checkTitle(self._params['title']) is False:
            return False

        for property in self._properties:
            params = {}
            if not self._properties[property].validate():
                self._setError(self._properties[property].getError())
                return False
            params[property] = self._properties[property].getValue()
        if self._checkUrl(self._params['url'],self._params['requestType'],params) is False:

            return False
        return True
    def addProperty(self,property,data):
       ruleObj = self.checkProperty(data)
       if self.checkProperty(data) is False:
            return False
       self._properties[property] = ruleObj
       return True

    def checkProperty(self,data):
        if type(data) is not type({}):
            self._setError('Params must be dict')
            return False
        if data.get('type') is None:
            self._setError('Type properties cannot be found in data ')
            return False
        if data.get('value') is None  or data.get('value') is '':
            self._setError('value can not be empty')
            return False
        ruleObj = self._ruleFactory.getAPIRule(data.get('type'), data.get('value'))
        if not ruleObj.validate():
            self._setError(ruleObj.getError())
            return False
        return ruleObj

        # obj = self.getAPIRule(data.get('type'))

        # if not None:
        #     self._setError('data Type is not exisit')
        #     return False
        # params = obj.parseParams(data.get('value'))
        # if params is False:
        # /    self._setError(obj.getError())
        #     return False
        # return params
    def _checkUrl(self, url, requestType, params={}):
        url = url.strip()
        if url is '':
            self._setError('Url can not be empty')
            return False
        if requestType is Constants.REQUEST_TYPE['GET']:
            paramsStr = ''
            for key in params:
                paramsStr = paramsStr + key + '=' + str(params[key]) +'&'

            paramsStr = paramsStr.strip('&')
            url = url + '?' + paramsStr
            print(url)
            self.Visit.getRequest(url)
        else:
            self.Visit.postRequest(url, params)

        response = self.Visit.getResponse()
        # print(self.Visit.getStatus())
        if response is None or self.Visit.getStatus() > 399:
            # print(self.Visit.getError())
            self._setError(self.Visit.getError())
            return False
        return True
        pass

    def _checkTitle(self, title):
        title = title.strip()
        if title is '':
            self._setError('Title can not be empty')
            return False
        return True
        pass


if __name__ == '__main__':
    V = APIValidate()
    V.addExtraParams('111','121',0)
    if V.addProperty('a1',{'type':1,'value':'1,5'}) is False:
        print(V.getError())
        # return False
    if V.validate() is False:
        print(V.getError())

    pass