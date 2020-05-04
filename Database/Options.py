from Database import database, pymysql, pre_deal_string, APIFuncWrapper


class OptionAPI:
    setStartDay = 'update timeinfo set start_day=%s where year=%s and semester=%s'
    addStartDay = 'insert into timeinfo(year, semester, start_day) VALUES (%s, %s, %s)'

    @staticmethod
    @APIFuncWrapper
    def SetStartDay(year: int, semester: int, start_day: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(OptionAPI.setStartDay % (start_day, year, semester))
            if res:
                database.commit()
        return res

    @staticmethod
    @APIFuncWrapper
    def AddStartDay(year: int, semester: int, start_day: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(OptionAPI.addStartDay % (year, semester, start_day))
            if res:
                database.commit()
        return res
