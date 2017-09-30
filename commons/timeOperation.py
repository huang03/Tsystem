import time,datetime
class TmOperation:
    """
        时间操作函数，
         validTime 验证字符串的时间，是否符合规定的设时间格式
         getDeltatime 根据给点的时间，进行时间增量
         getDateTimeByStr 根据给订的时间字符串，转换成 datetime的类型
         compareTime 时间比较，比较第一时间是否大于第二个时间
    """
    def validTime(self,str,format='%Y-%m-%d %H:%M:%S'):
        '''
            验证时间有效性：
                str:给点时间字符串
                format:时间格式

                返回值：False or datetime
        '''
        try:
            formats = '%Y-%m-%d %H:%M:%S'
            return time.strptime(str, format)
        except Exception:

            raise Exception('the format of time is error %s %s' % (str,formats))
            return False
    def getDeltatime(self,currTimeStr, key='S', delta=0):
        '''
            时间增量计算
            currTimeStr：给点时间 str or datetime
            key:以什么单位进行增量
                S：秒
                M：分
                H：时
                d: 天
            delta：增加量数 int

            返回值：返回增量后的时间
        '''
        if isinstance(currTimeStr,str):
            currDate = self.getDateTimeByStr(currTimeStr)
        else:
            currDate = currTimeStr
        if key == 'S':
            return currDate - datetime.timedelta(seconds=delta)
        elif key == 'M':
            return currDate - datetime.timedelta(minutes=delta)
        elif key == 'H':
            return currDate - datetime.timedelta(hours=delta)
        elif key == 'd':
            return currDate - datetime.timedelta(days=delta)
        return currDate

    def getDateTimeByStr(self,str):
        '''
            根据时间字符串返回 datetime的类型的时间
        '''
        if  isinstance(str,datetime.datetime):
            return str
        ptime = self.validTime(str)
        if not ptime:
            return False
        return datetime.datetime(ptime.tm_year, ptime.tm_mon, ptime.tm_mday, ptime.tm_hour, ptime.tm_min, ptime.tm_sec)
    #a = datetime.datetime(a.tm_year,a.tm_mon,a.tm_mday,a.tm_hour,a.tm_min,a.tm_sec)
    #timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999)。
    #datetime(year,month,day,hour,minute,secode)
    #print(a-datetime.timedelta(minutes=1))
   
    def compareTime(self,tm1, tm2):
        '''
            比较tm1 是否 大于 tm2
            返回值：True/False
        '''
        tm1 = self.validTime(tm1)
        tm2 = self.validTime(tm2)
        tm1 = datetime.datetime(tm1.tm_year, tm1.tm_mon, tm1.tm_mday, tm1.tm_hour, tm1.tm_min,
                                     tm1.tm_sec)
        tm2 = datetime.datetime(tm2.tm_year, tm2.tm_mon, tm2.tm_mday, tm2.tm_hour, tm2.tm_min,
                                tm2.tm_sec)
        if tm1 >= tm2:
            return True
        return False

    pass