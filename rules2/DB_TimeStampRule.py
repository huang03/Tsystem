import time
import Constants
from rules2._IRule import _IRule
from commons.timeOperation import TmOperation

class TimeStampRule(_IRule):
    def __init__(self,params):
        super().__init__(params)
        self._tmOperator = TmOperation()
        # self._currValue = None
        self._isInit = False

    def _validateComman(self):

        # if self.params.get('now'):
        #     return True
        if self.params.get('start'):
            try:
                self._tmOperator.validTime(self.params.get('start'))
            except:
                self._setError('the format is xxxx-xx-xx xx:xx:xx for start')
                return False
        if self.params.get('end'):
            try:
                self._tmOperator.validTime(self.params.get('end'))
            except:
                self._setError('the format is xxxx-xx-xx xx:xx:xx for end')
                return False

        if type(self.params.get('step')) is not type(1) and not self.params.get('step').isdigit():
            self._setError('step must be Interger')
            return False
        if not self.params.get('unit'):
            self.params['unit'] = 'M'

        return True

    def _getCommanValue(self):
        if not self._isInit:
            self.init()
        # if self.params.get('now'):
        #     self._currValue = time.strftime('%Y-%m-%d %H:%M:%S')
        # else:
        if not self._currValue:
            self._currValue = self.params['start']
        else:
            self._currValue = self._tmOperator.getDeltatime(self._currValue, self.params['unit'], self.params['step'])
            if(self._currValue > self.params['end']):
                self._currValue = Constants.OVAER_FLAG
        return self._currValue

    def _getNowValue(self):
        self._currValue = time.strftime('%Y-%m-%d %H:%M:%S')
        return self._currValue
    # def validate(self):
    #     if self.params.get('now'):
    #         return True
    #
    #     if self.params.get('start'):
    #         try:
    #             self._tmOperator.validTime(self.params.get('start'))
    #         except:
    #             self._setError('the format is xxxx-xx-xx xx:xx:xx for start')
    #             return False
    #     if self.params.get('end'):
    #         try:
    #             self._tmOperator.validTime(self.params.get('end'))
    #         except:
    #             self._setError('the format is xxxx-xx-xx xx:xx:xx for end')
    #             return False
    #
    #     if  type(self.params.get('step')) is not type(1) and not self.params.get('step').isdigit():
    #         self._setError('step must be Interger')
    #         return False
    #     if not self.params.get('unit'):
    #         self.params['unit'] = 'M'
    #     return True
    #     pass
    def init(self):
        if(self.params.get('step')):
            self.params['step'] = int(self.params['step'])*-1

        if self.params.get('end'):
            self.params['end'] = self._tmOperator.getDateTimeByStr(self.params['end'])
        self._isInit = True
    # def getValue(self):
    #
    #     if not self._isInit:
    #         self.init()
    #     if self.params.get('now'):
    #         self._currValue = time.strftime('%Y-%m-%d %H:%M:%S')
    #     else:
    #         if not self._currValue:
    #             self._currValue = self.params['start']
    #         else:
    #             self._currValue = self._tmOperator.getDeltatime(self._currValue, self.params['unit'], self.params['step'])
    #             if(self._currValue > self.params['end']):
    #                 self._currValue = Constants.OVAER_FLAG
    #     return self._currValue
    #     pass
    # pass

if __name__ == '__main__':
    params = {'start':'2017-12-09 08:00:00','end':'2017-12-09 20:00:00','step':2}
    R = TimeStampRule(params)
    if not R.validate():
        print(R.getError())
    else:
        print(R.getValue())
        print(R.getValue())
        print(R.getValue())
        print(R.getValue())