import Constants

from rules2.API_RangeRule import RangeRule
from rules2.API_ValueListRule import ValueListRule
from rules2.API_DefaultValueRule import DefaultValueRule
from rules2.API_TableRule import TableRule
from rules2.DB_VarcharRule import VarcharRule
from rules2.DB_IntegerRule import IntegerRule
from rules2.DB_SmallIntRule import SmallIntRule
from rules2.DB_TinyIntRule import TinyIntRule
from rules2.DB_TimeStampRule import TimeStampRule
from rules2.DB_DateRule import DateRule

TYPES = {
    "定值":0,
    "范围":1,
    "默认":2,
    'VARCHAR':3,
    'INT':4,
    'TIMESTAMP':5,
    'DATE':6,
    'SMALLINT':7,
    'TINYINT':8,
    'TABLE':9
}
class RuleFactory:
    def getAPIRule(self, key,value):
        key = key.upper();
        type = self.choiceType(key)
        obj = None
        # if type is Constants.API_RULE_TYPE['默认']:
        #     obj = DefaultValueRule(value)
        # elif type is Constants.API_RULE_TYPE['定值']:
        #     obj = ValueListRule(value)
        # elif type is Constants.API_RULE_TYPE['范围']:
        #     obj = RangeRule(value)
        if type is 3:
            obj = VarcharRule(value)
        elif type is 4:
            obj = IntegerRule(value)
        elif type is 7:
            obj = SmallIntRule(value)
        elif type is 8:
            obj = TinyIntRule(value)
        elif type is 5:
            obj = TimeStampRule(value)
        elif type is 6:
            obj = DateRule(value)
        elif type is 9:
            obj = TableRule()
        return obj

    def choiceType(self,type):
        for key in TYPES:
            if key in type:
                return TYPES[key]
        return None