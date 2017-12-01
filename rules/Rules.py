import time
from commons.timeOperation import TmOperation
from rules.GenerateData import *
class _IRule:
    '''
        规则类接口
        validate: 验证规则合法性
        getError
        setError
        setMetas:设置元数据
        getValue:根据规则生成数据

        属性
         _metas:元数据
         _error:错误列表
         _GrtData:生成数据的类
    '''
    def __init__(self,params):
        self._metas = params
        self._error = None
        self._GrtData = None
    def validate(self):
        pass

    def getError(self):
        return self._error

    def setError(self,error):
        self._error = error

    def getMetas(self):
        return self._metas

    def setMetas(self,params):
        self._metas = params
        del params
    def getValue(self):
        pass;


def validateExtras(parent):
    '''
    验证额外规则
    设置额外规则的标志为存在 _TYPE_
    :param parent: 父对象
    :return:
    '''
    if not parent._metas.get('_TYPE_'):
        return 1
    if parent._metas.get('_TYPE_') == 'LIST':
        return validateExtras(parent)
    else:
        return validateTbl(parent)
    pass
#验证固定列表数据
def validateValueList(parent):
    if parent._metas.get('list') == '':
        return False
    return True
    pass
#验证数据表，字段
def validateTbl(parent):
    if parent._metas.get('tbl') == '':
        return False
    if parent._metas.get('property') == '':
        return False

    return True

class IntegerRule(_IRule):
    '''
        整数规则验证:
        params dict:
            start:开始值
            end:结束值
            step:步长
    '''
    def __init__(self,params):
        super().__init__(params)
    def validate(self):
        isOk = validateExtras(self)
        if isOk != 1:
            return isOk
        params = self._metas
        if not params.get('start').isdigit():
            self.setError('start must Interger')
            return False
        if not params.get('end').isdigit():
            self.setError('end must Interger')
            return False
        if not params.get('step').isdigit():
            self.setError('step must Interger')
            return False
        params['start'] = int(params['start'])
        params['end'] = int(params['end'])
        params['step'] = int(params['step'])
        if params.get('start') > params.get('end'):
            self.setError('end must bigger than start ')
            return False
        del params
        #self.setMetas(params)
        return True
    def getValue(self):
        if not self._GrtData:
            self._GrtData = IntegerGenerate(self)
        return self._GrtData.getValue()
class VarcharRule(_IRule):
    '''
        验证字符字符串格式:
            params dict:
                prefix: 字符串前缀 (字符串的生成是通过 前缀+数字)
                start:开始值
                end:结束值
                step:步长
    '''
    def __init__(self,params):
        super().__init__(params)
    def validate(self):
        isOk = validateExtras(self)
        if isOk != 1:
            return isOk
        params = self._metas
        RInteger = IntegerRule(params)
        if not RInteger.validate():
            self.setError(RInteger.getError())
            self.setMetas(None)
            return False
        if not params.get('prefix'):
            params['prefix'] = 'tsys-'


        del RInteger
        del params
        return True
    def getValue(self):
        if not self._GrtData:
            self._GrtData = VarcharGenerate(self)
        return self._GrtData.getValue()
class TimeStampRule(_IRule):
    '''
        验证时间:
            params dict:
                now:是否直接获取当前时间 如果为真，其他选项无效
                start:开始时间 时间格式 xxxx-xx-xx xx:xx:xx
                end:结束时间
                step:步长
                unit:增长单位  M：分 H：时 S:秒 d:天
    '''
    def __init__(self,params):
        super().__init__(params)
    def validate(self):
        # print(1111)
        params = self._metas
        if params.get('now'):
            self.setMetas(params)
            return True
        tm = TmOperation()
        if params.get('start'):
            try:
                tm.validTime(params.get('start'))
            except:
                self.setError('the format is xxxx-xx-xx xx:xx:xx for start')
                return False
        if params.get('end'):
            try:
                tm.validTime(params.get('end'))
            except:
                self.setError('the format is xxxx-xx-xx xx:xx:xx for end')
                return False

        if not params.get('step').isdigit():
            self.setError('step must Interger')
            return False
        if not params.get('unit'):
            params['unit'] = 'M'
        del  params
        return True
    def getValue(self):
        if not self._GrtData:
            self._GrtData = TimeStampGenerate(self)
        return self._GrtData.getValue()