from VisitUrl import VisitUrl
from dbs.mysqlBase import MySQLBase
class APIRule:
    def __init__(self):
        self.Visit = VisitUrl()
        self._error = None
        self.propertis = {}

    def checkProperty(self,type,value):
        # if self.Visit is None:
        #     self.Visit = VisitUrl()
        obj = None
        if type is 'DEFAULT':
            obj = DefaultValueRule()
        elif type is 'LIST':
            obj = ValueListRule()
        elif type is 'RANGE':
            obj = RangeRule()
        elif type is 'TABLE':
            obj = TableRule()
        params = obj.parseParams(value)
        if not params:
            self._setError(obj.getError())
            return False
        return True
        # if obj is not None:
            # obj.setVisitObj(self.Visit)
        # return obj

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
        if requestType == 0:
            # url = url + '?' + self.params
            # print(url)
            self.Visit.getRequest(url)
        else:
            self.Visit.postRequest(url, params)

        response = self.Visit.getResponse()
        print(self.Visit.getStatus())
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

    def validates(self, title, url, requestType, params):
        pass
        if self.Visit is None:
            self._setError('Visit is None')
            return False
        # self._setParams(params, requestType)
        if not self._checkTitle(title) or not self._checkUrl(url, requestType, params):
            return False
        return True
    # def
        # return False
    pass
class IAPIRule:
    def __init__(self):
        self._error = None
        # self.Visit = None
        self.params = ''
        pass
    # def setVisitObj(self,obj):
    #     self.Visit = obj
    # def _checkUrl(self,url,requestType,params={}):
    #     url = url.strip()
    #     if url is '':
    #         self._setError('Url can not be empty')
    #         return False
    #     if requestType == 0:
    #        url = url + '?' + self.params
    #        print(url)
    #        self.Visit.getRequest(url)
    #     else:
    #        self.Visit.postRequest(url,params)
    #
    #     response = self.Visit.getResponse()
    #
    #     print(self.Visit.getStatus())
    #     if response is None or self.Visit.getStatus()>399:
    #         self._setError(self.Visit.getError())
    #         return False
    #     return True
    #     pass

    # def _setParams(self,values,requestType):
    #     params = self._parseParams(values);
    #     if requestType == 0:
    #         tmp = ''
    #         for key in params:
    #             tmp = tmp + key + '=' + params[key] + '&'
    #         self.params = tmp.strip('&')
    #     else:
    #         self.params = params
    #     pass
    def parseParams(self,values):
        pass
    # def _getParams(self):
    # def _checkTitle(self,title):
    #     title = title.strip()
    #     if title is '':
    #         self._setError('Title can not be empty')
    #         return False
    #     return True
    #     pass
    def _setError(self,error):
        self._error = error
        pass
    def getError(self):
        return self._error
        pass
    # def validates(self,title,url,requestType,params):
    #     pass
    #     if self.Visit is None:
    #         self._setError('Visit is None')
    #         return False
    #     self._setParams(params,requestType)
    #     if not self._checkTitle(title) or not self._checkUrl(url,requestType,params):
    #         return False
    #     return True


class DefaultValueRule(IAPIRule):
    def parseParams(self,values):
        values = values.strip()
        if values is '':
            self._setError('value can not be empty')
            return False
        return values
        pass

    pass

class ValueListRule(IAPIRule):
    def parseParams(self,values):
        pass

    pass

class RangeRule(IAPIRule):
    def parseParams(self,values):
        pass
    pass

class TableRule(IAPIRule):
    def parseParams(self,values):
        pass

    pass

if __name__ == '__main__':
    Rules = APIRule()
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