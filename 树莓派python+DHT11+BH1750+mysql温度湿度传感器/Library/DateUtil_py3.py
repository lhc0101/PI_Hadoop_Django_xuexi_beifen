# -*- encoding:utf8 -*-
'''
@author: crazyant
@version: 2017-06-15
'''
import datetime, time

#定义的日期的格式，可以自己改一下，比如改成"$Y年$m月$d日"
format_date = "%Y-%m-%d"
format_datetime = "%Y-%m-%d %H:%M:%S"

def getCurrentDate():
    '''
            %Y-%m-%d 获取当前日期：2017-06-15这样的日期字符串
    '''
    return time.strftime(format_date, time.localtime(time.time()))

def getCurrentDateTime():
    '''
            %Y-%m-%d %H:%M:%S 获取当前时间：2017-06-15 14:21:11这样的时间年月日时分秒字符串
    '''
    return time.strftime(format_datetime, time.localtime(time.time()))

def getCurrentHour(date):
    '''
            %H 获取当前时间的小时数，比如如果当前是下午14时，则返回14
    '''
    currentDateTime=getCurrentDateTime()
    return currentDateTime[-8:-6] 

def getCurrentMour(date):
    '''
            %M 获取当前时间的分数，比如如果当前是下午14:20时，则返回:20
    '''
    currentDateTime=getCurrentDateTime()
    return currentDateTime[-5:-3] 

def getCurrentDD(date):
    '''
            %M 获取当前时间的日，比如如果当前是2017-06-15时，则返回 15
    '''
    currentDateTime=getCurrentDateTime()
    return currentDateTime[8:10] 

def getCurrentMM(date):
    '''
            %m 获取当前时间的日，比如如果当前是2017-06-15时，则返回 06
    '''
    currentDateTime=getCurrentDateTime()
    return currentDateTime[5:7] 

def getCurrentYY(date):
    '''
            %Y 获取当前时间的日，比如如果当前是2017-06-15时，则返回 2017
    '''
    currentDateTime=getCurrentDateTime()
    return currentDateTime[0:4]

def getCurrentYYMM(date):
    """
            %Y-%m获取当前时间的日，比如如果当前是2017-06-15时，则返回 2017-06
    """
    currentDateTime=getCurrentDateTime()
    return currentDateTime[0:7] 


def get_week_day_(date):    
    """
            代码入库日期：2017-06-28
            输入：0
            返回：单个输出:星期一
    """
    week_day_dict = {
        0 : '星期一',
        1 : '星期二',
        2 : '星期三',
        3 : '星期四',
        4 : '星期五',
        5 : '星期六',
        6 : '星期日',
    }
    day = date.weekday()
    return week_day_dict[day]


def get_week_day_w(date):
    """
            代码入库日期：2017-06-28
            输入：0
            返回：单个输出:w1
    """
    week_day_dict_w = {        
        0 : 'w1',
        1 : 'w2',
        2 : 'w3',
        3 : 'w4',
        4 : 'w5',
        5 : 'w6',
        6 : 'w7',
    }
    day = date.weekday()
    return week_day_dict_w[day]

def getDateElements(sdate):
    """
            输入日期字符串，返回一个结构体组，包含了日期各个分量
            输入：2016-09-10或者2016-09-10 22:11:22
            返回：time.struct_time(tm_year=2013, tm_mon=4, tm_mday=1, tm_hour=21, tm_min=22, tm_sec=33, tm_wday=0, tm_yday=91, tm_isdst=-1)
    """
    dformat = ""
    if judgeDateFormat(sdate) == 0:
        return None
    elif judgeDateFormat(sdate) == 1:
        dformat = format_date
    elif judgeDateFormat(sdate) == 2:
        dformat = format_datetime
    sdate = time.strptime(sdate, dformat)
    return sdate

def getDateToNumber(date1):
    """
            将日期字符串中的减号冒号去掉: 
            输入：2016-04-05，返回20160405
            输入：2016-04-05 22:11:23，返回20160405221123
    """
    return date1.replace("-","").replace(":","").replace("","")

##添加代码20170628
def getDateToNumberYM(date1):
    """
            代码入库日期：2017-06-28
            将日期字符串中的减号冒号去掉: 
            输入：2017-06-28，返回201706
            输入：2017-06-28 00:11:23，返回201706
    """    
    return (date1.replace("-","").replace(":","").replace("",""))[0:6]

def getDateToNumberYMD(date1):
    """
            代码入库日期：2017-06-28
            将日期字符串中的减号冒号去掉: 
            输入：2017-06-28，返回20170628
            输入：2017-06-28 00:11:23，返回20170628
    """    
    return (date1.replace("-","").replace(":","").replace("",""))[0:8]

def getDateToNumberYMDnext(date1):
    """
            代码入库日期：2017-06-28
            将日期字符串中的减号冒号去掉: 
            输入：2017-06-28，返回下一个月20170728
            输入：2017-06-28 00:11:23，返回下一个月20170728
    """
    _ccv = get_1st_of_next_month() #读取下一月日期
    ccv = (_ccv.replace("-","").replace(":","").replace("",""))[0:8]    
    return ccv

def getDateToNumberYMnext(date1):
    """
            代码入库日期：2017-06-28
            将日期字符串中的减号冒号去掉: 
            输入：2017-06-28，返回下一个月201707
            输入：2017-06-28 00:11:23，返回下一个月201707
    """
    _ccv = get_1st_of_next_month() #读取下一月日期
    ccv = (_ccv.replace("-","").replace(":","").replace("",""))[0:6]    
    return ccv


######

def judgeDateFormat(datestr):
    """
            判断日期的格式，如果是"%Y-%m-%d"格式则返回1，如果是"%Y-%m-%d %H:%M:%S"则返回2，否则返回0
            参数 datestr:日期字符串
    """
    try:
        datetime.datetime.strptime(datestr, format_date)
        return 1
    except:
        pass

    try:
        datetime.datetime.strptime(datestr, format_datetime)
        return 2
    except:
        pass

    return 0

def minusTwoDate(date1, date2):
    """
            将两个日期相减，获取相减后的datetime.timedelta对象
            对结果可以直接访问其属性days、seconds、microseconds
    """
    if judgeDateFormat(date1) == 0 or judgeDateFormat(date2) == 0:
        return None
    d1Elements = getDateElements(date1)
    d2Elements = getDateElements(date2)
    if not d1Elements or not d2Elements:
        return None
    d1 = datetime.datetime(d1Elements.tm_year, d1Elements.tm_mon, d1Elements.tm_mday, d1Elements.tm_hour, d1Elements.tm_min, d1Elements.tm_sec)
    d2 = datetime.datetime(d2Elements.tm_year, d2Elements.tm_mon, d2Elements.tm_mday, d2Elements.tm_hour, d2Elements.tm_min, d2Elements.tm_sec)
    return d1 - d2

def dateAddInDays(date1, addcount):
    """
            日期加上或者减去一个数字，返回一个新的日期
            参数date1：要计算的日期
            参数addcount：要增加或者减去的数字，可以为1、2、3、-1、-2、-3，负数表示相减
    """
    try:
        addtime=datetime.timedelta(days=int(addcount))
        d1Elements=getDateElements(date1)
        d1 = datetime.datetime(d1Elements.tm_year, d1Elements.tm_mon, d1Elements.tm_mday)
        datenew=d1+addtime
        return datenew.strftime(format_date)
    except Exception as e:
        print(e)
        return None

def is_leap_year(pyear):
    """
            判断输入的年份是否是闰年 
    """  
    try:                     
        datetime.datetime(pyear, 2, 29)
        return True          
    except ValueError:       
        return False         

def dateDiffInDays(date1, date2):
    """
            获取两个日期相差的天数，如果date1大于date2，返回正数，否则返回负数
    """
    minusObj = minusTwoDate(date1, date2)
    try:
        return minusObj.days
    except:
        return None

def dateDiffInSeconds(date1, date2):
    """
            获取两个日期相差的秒数
    """
    minusObj = minusTwoDate(date1, date2)
    try:
        return minusObj.days * 24 * 3600 + minusObj.seconds
    except:
        return None

def getWeekOfDate(pdate):
    """
            获取日期对应的周，输入一个日期，返回一个周数字，范围是0~6、其中0代表周日
    """
    pdateElements=getDateElements(pdate)

    weekday=int(pdateElements.tm_wday)+1
    if weekday==7:
        weekday=0
    return weekday

##添加代码20170628
#############################

def get_1st_of_last_month():
    """
    代码入库日期：2017-06-28
    获取上个月第一天的日期，然后加27天就是28号的日期
    :return: 返回日期 2017-06-28 00:00:00
    """
    today=datetime.datetime.today()
    year=today.year
    month=today.month
    if month==1:
        month=12
        year-=1
    else:
        month-=1
    res=datetime.datetime(year,month,1)+datetime.timedelta(days=27)
    #print(datetime.datetime(year,month,27))
    return str(res)

def get_1st_of_next_month():
    """
    代码入库日期：2017-06-28
    获取下个月的28号的日期
    :return: 返回日期 2017-06-28 00:00:00
    """
    today=datetime.datetime.today()
    year=today.year
    month=today.month
    if month==12:
        month=1
        year+=1
    else:
        month+=1
    res=datetime.datetime(year,month,1)+datetime.timedelta(days=27)
    return str(res)

def time_s_to_stamp(args):
    """
    代码入库日期：2017-06-28
    将datetime日期格式，先timetuple()转化为struct_time格式
    然后time.mktime转化为时间戳
    :param args:    datetime时间格式数据
    :return:    时间戳格式数据
    """
    res=time.mktime(args.timetuple())
    return res


#if __name__=="__main__":
    """
            测试代码
    """
    #print judgeDateFormat("2013-04-01")
    #print judgeDateFormat("2013-04-01 21:22:33")
    #print judgeDateFormat("2013-04-31 21:22:33")
    #print judgeDateFormat("2013-xx")
    #print "--"
    #print datetime.datetime.strptime("2013-04-01", "%Y-%m-%d")
    #print 'elements'
    #print getDateElements("2013-04-01 21:22:33")
    #print 'minus'
    #print minusTwoDate("2013-03-05", "2012-03-07").days
    #print dateDiffInSeconds("2013-03-07 12:22:00", "2013-03-07 10:22:00")
    #print type(getCurrentDate())
    #print getCurrentDateTime()
    #print dateDiffInSeconds(getCurrentDateTime(), "2013-06-17 14:00:00")
#    print getCurrentHour(datetime.datetime.now())
#    print getCurrentMour(datetime.datetime.now())
#    print getCurrentYYMM(datetime.datetime.now())
#    print get_week_day_(datetime.datetime.now())
    #print dateAddInDays("2013-04-05",-5)
    #print getDateToNumber("2013-04-05")
    #print getDateToNumber("2013-04-05 22:11:33")
    #print (get_1st_of_last_month()) ##添加代码20170628    
    #print (get_1st_of_next_month()) ##添加代码20170628
    #print getWeekOfDate("2013-10-01")

##    print (getDateToNumberYMD("2017-06-28 12:11:33")) ##添加代码20170628
##    print (getDateToNumberYMD(get_1st_of_last_month())) ##添加代码20170628
##    print (getDateToNumberYMD(get_1st_of_next_month())) ##添加代码20170628
##    print (getDateToNumberYMDnext("2017-06-29 12:11:33")) ##添加代码20170628 输出下一个今天
##    print (getDateToNumberYMnext("2017-06-29 12:11:33")) ##添加代码20170628 输出下一个今天
#    print (getDateToNumberYMDnext(getCurrentDateTime())) ##添加代码20170628 输出下一个今天
#    print (getDateToNumberYMnext(getCurrentDateTime())) ##添加代码20170628 输出下一个今天
#    print (getDateToNumberYMD(getCurrentDateTime()))
#    print (getDateToNumberYM(getCurrentDateTime()))
    

