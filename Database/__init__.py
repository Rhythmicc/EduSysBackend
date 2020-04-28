import pymysql
import sys
sys.path.append('..')

database = None
try:
    database = pymysql.connect(
        host='rm-2ze17saovz0800382ao.mysql.rds.aliyuncs.com',
        user='rhythmlian',
        password='19980501',
        database='softwaredesign',
        charset='utf8'
    )
except Exception as e:
    print(repr(e))
    exit('Link Database failed!')


def pre_deal_string(string):
    string = string.strip('"')
    return '"' + string + '"'


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
