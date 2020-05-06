import datetime
import math
import sys

import pymysql

sys.path.append('..')

database = None
try:
    database = pymysql.connect(
        host='rm-2ze17saovz0800382ao.mysql.rds.aliyuncs.com',
        user='edu_sys_client',
        password='P7pXAFKXbMLB3D5vTdmhnT4OX96XFQBd',
        database='softwaredesign',
        charset='utf8'
    )
except Exception as e:
    print(repr(e))
    exit('Link Database failed!')
else:
    with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
        res = cur.execute('select start_day from timeinfo where year=2020 and semester=1')
        if res:
            start_day = cur.fetchall()[0]['start_day']
        else:
            start_day = False


def autoCalWeek():
    if not start_day:
        return False
    today = datetime.date.today()
    assert isinstance(start_day, datetime.date)
    return math.ceil(((today - start_day).days + 1) / 7)


def pre_deal_string(string):
    return '"%s"' % string.strip('"')


def APIFuncWrapper(func):
    def wrapper(*args, **kwargs):
        try:
            database.ping()
        except:
            database.connect()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(repr(e))
            return False
    return wrapper


def CloseDatabase():
    database.close()
