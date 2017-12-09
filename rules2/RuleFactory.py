import Constants

from rules2.API_RangeRule import RangeRule
from rules2.API_ValueListRule import ValueListRule
from rules2.API_DefaultValueRule import DefaultValueRule
from rules2.API_TableRule import TableRule
from rules2.DB_VarcharRule import VarcharRule
from rules2.DB_IntegerRule import IntegerRule
from rules2.DB_TimeStampRule import TimeStampRule
class RuleFactory:
    def getAPIRule(self, type,value):
        obj = None
        if type is Constants.API_RULE_TYPE['默认']:
            obj = DefaultValueRule(value)
        elif type is Constants.API_RULE_TYPE['定值']:
            obj = ValueListRule(value)
        elif type is Constants.API_RULE_TYPE['范围']:
            obj = RangeRule(value)
        elif type is Constants.API_RULE_TYPE['varchar']:
            obj = VarcharRule(value)
        elif type is Constants.API_RULE_TYPE['int']:
            obj = IntegerRule(value)
        elif type is Constants.API_RULE_TYPE['timestamp']:
            obj = TimeStampRule(value)
        elif type is 'TABLE':
            obj = TableRule()
        return obj