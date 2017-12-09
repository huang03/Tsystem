import  Constants
from VisitUrl import VisitUrl

from dbs.mysqlBase import MySQLBase
class APIRule:
    def __init__(self):
        self.Visit = VisitUrl()
        self._error = None
        self.propertis = {}
    def getAPIRule(self,type):
        obj = None
        if type is Constants.API_RULE_TYPE['默认']:
            obj = DefaultValueRule()
        elif type is Constants.API_RULE_TYPE['定值']:
            obj = ValueListRule()
        elif type is Constants.API_RULE_TYPE['范围']:
            obj = RangeRule()
        elif type is 'TABLE':
            obj = TableRule()
        return obj
    def checkAPI(self,url,requestType,title,datas):
        requestParams = {};
        if self._checkTitle(title) is False:
            return False
        for key in datas:
            print(key)
            result = self.checkProperty(datas[key])
            if result is False:
                return False
            requestParams[key] = result
        if self._checkUrl(url, requestType, requestParams) is False:
            return False
        return True
        pass
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
        obj = self.getAPIRule(data.get('type'))
        if not None:
            self._setError('data Type is not exisit')
            return False
        # obj = None
        # if data.get('type') is 2:
        #     obj = DefaultValueRule()
        # elif data.get('type') is 0:
        #     obj = ValueListRule()
        # elif data.get('type') is 1:
        #     obj = RangeRule()
        # elif data.get('type') is 'TABLE':
        #     obj = TableRule()
        params = obj.parseParams(data.get('value'))
        if params is False:
            self._setError(obj.getError())
            return False
        return params
    def _setError(self,error):
        self._error = error
        pass

    def getError(self):
        return self._error
        pass

    def _checkUrl(self, url, requestType, params={}):
        url = url.strip()
        if url is '':
            self._setError('Url can not be empty')
            return False
        if requestType is Constants.REQUEST_TYPE['GET']:
            paramsStr = ''
            for key in params:
                paramsStr = paramsStr + key + '=' + params[key]+'&'

            paramsStr = paramsStr.strip('&')
            url = url + '?' + paramsStr
            print(url)
            self.Visit.getRequest(url)
        else:
            self.Visit.postRequest(url, params)

        response = self.Visit.getResponse()
        # print(self.Visit.getStatus())
        if response is None or self.Visit.getStatus() > 399:
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

    pass
class IAPIRule:
    def __init__(self):
        self._error = None
        self.params = ''
        pass
    def parseParams(self,values):
        pass
    def _setError(self,error):
        self._error = error
        pass
    def getError(self):
        return self._error
        pass

class DefaultValueRule(IAPIRule):
    def parseParams(self,values):
        values = values.strip()
        return values
        pass

    pass

class ValueListRule(IAPIRule):
    def parseParams(self,values):
        tmp = values.split(',')
        if len(tmp)>0:
            return tmp[0]
        return False
        pass

    pass

class RangeRule(IAPIRule):
    def parseParams(self,values):
        tmp = values.split(',')
        if len(tmp)>1:
            return tmp[0]
        else:
            self._setError('the format of Range Value is xx,xx and  Integer')
            return False
        pass
    pass

class TableRule(IAPIRule):
    def parseParams(self,values):
        pass

    pass

if __name__ == '__main__':
    pass
    Rules = APIRule()
    result = Rules.checkAPI('http://127.0.0.1/py_test.php',0, 'Title',{'a1':{'value':'2,5','type':1},'a2':{'value':'2,5','type':2}})
    print(result)
    if result is False:
        print(Rules.getError())
    print(121212)
    # result = Rules.checkProperty({'value':'2,5','type':1})
    # if not result:
    #     print(Rules.getError())
    #     # print(result)
    # print(result)
    #每个属性需要验证,需要解析value,和生成 value 值， 提交是，需要结合参数，验证url的可行性
    #需要验证 DefaultRule...的规则，然后验证提交的，url的正确性
    # Rules = V
    # obj = Rules.getRuleObj('DEFAULT')
    # result = Rules.validates('12','http://127.0.0.1/py_test.php',0,{'a':'vv'})

    # a = ['a','b','c','d','2']
    # del a[2]
    # print(a[2])
    # print(len(a))
    # if not result:
    #     print(Rules.getError())
    # MT = MySQLBase(host='127.0.0.1',port=3306,user='func',passwd='passwd',db='xmes_yc',charset='utf8')
    # pre = '172.16.'
    # IPS = ['51','52','53']
    # Machines = [0,72,144,222]
    # index = 0
    # fieds = ('id','name','dest','type_id','collector_id')
    # for ip in IPS:
    #     tmpIp = '%s%s' %(pre,ip)
    #     for i in range(Machines[index]+1,Machines[index+1]+1):
    #         name = ''
    #         if i<10:
    #             name = '00'+str(i)
    #         elif i<100:
    #             name = '0'+str(i)
    #         else:
    #             name = str(i)
    #         dest = tmpIp+'.'+str(i)
    #         ms = (i,name,dest,1,1)
    #         try:
    #             MT.add({
    #                 'table':'tbl_machine',
    #                 'field':fieds,
    #                 'binds':ms
    #             })
    #         except Exception as e:
    #             print(e)
    #         print(ms)
    #         # print(i)
    #     # break
    #     # print(ip)
    #     index += 1
    #
    # for i in range(1,223):
    #     try:
    #         MT.add({
    #             'table':'tbl_machine_group',
    #             'field':('id','group_id','machine_id'),
    #             'binds':(i,1,i)
    #         })
    #         print(i)
    #     except Exception as e:
    #         print(e)