import time
# from rules.Rules import _IRule
from  commons.timeOperation import  TmOperation
from rules.DefaultValue import *
class IGenerate:
    '''
        根据Rules中的规则生成数据
        generateValue：生成数据
        getValue: 获取数据
        setRule：设置规则

        属性：
            _metas:规则的原始参数
            _currValue 当前值
    '''
    def __init__(self,rule):
        self.__initial(rule)
    def __initial(self,rule):
        # if not isinstance(rule,_IRule):
        #     raise Exception('rule must be the son of _IRule')
        self._metas = rule.getMetas()
        self._rule = rule
        self._currValue = None
    def generateValue(self):
        pass
    def getValue(self):
        if self._currValue == OVAER_FLAG:
            return False
        self.generateValue()
        return self._currValue
    def setRule(self,rule):
        self.__initial(rule)

class IntegerGenerate(IGenerate):
    '''
        整数生成
    '''
    def __init__(self,rule):
        super().__init__(rule)

    def generateValue(self):
        if not self._metas:
            self._currValue = None
            return False
        if self._currValue:
            self._currValue += self._metas['step']
        else:
            self._currValue = self._metas['start']
        if self._currValue > self._metas['end']:
            self._currValue = self._metas['start']

class VarcharGenerate(IGenerate):
    '''
        字符串数据生成
    '''
    def __init__(self, rule):
        super().__init__(rule)
        self._GInteger = IntegerGenerate(rule)

    def generateValue(self):
        if not self._metas:
            self._currValue =None
        currValue = self._GInteger.getValue()

       # print(self._metas)
        if not currValue:
            self._currValue = self._metas['prefix']
        self._currValue =  self._metas['prefix'] + '%s' % currValue


class TimeStampGenerate(IGenerate):
    '''
        时间数据生成
    '''
    def __init__(self, rule):
        super().__init__(rule)
        self.TmOpr = TmOperation();
        if self._metas.get('end'):
            self._metas['end'] = self.TmOpr.getDateTimeByStr(self._metas['end'])

    def generateValue(self):
        #print(self._metas)
        if self._metas.get('now'):
            self._currValue = time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            if not self._currValue:
                self._currValue = self._metas['start']
            else:
                self._currValue = self.TmOpr.getDeltatime(self._currValue, self._metas['unit'], self._metas['step'])
                if(self._currValue > self._metas['end']):
                    self._currValue = OVAER_FLAG

