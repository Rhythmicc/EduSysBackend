from . import database, pymysql, pre_deal_string, APIFuncWrapper


class AdminAPI:
    """增删改查"""
    addAdmin = 'insert into admininfo(user_id, name, gender) VALUES (%s, %s, %s)'
    delAdmin = 'delete from admininfo where user_id like %s'
    altAdmin = 'update admininfo set name=%s, gender=%s where user_id like %s'
    qryAdmin = 'select * from admininfo where user_id like %s'

    @staticmethod
    @APIFuncWrapper
    def AddAdmin(user_id: str, name: str, gender: bool):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(AdminAPI.addAdmin % (
                pre_deal_string(user_id),
                pre_deal_string(name), gender
            ))
            database.commit()
        return True

    @staticmethod
    @APIFuncWrapper
    def DelAdmin(user_id: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(AdminAPI.delAdmin % pre_deal_string(user_id))
            database.commit()
        return True

    @staticmethod
    @APIFuncWrapper
    def AltAdmin(user_id: str, name: str, gender: bool):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(AdminAPI.altAdmin % (
                pre_deal_string(name), gender,
                pre_deal_string(user_id)
            ))
            database.commit()
        return True

    @staticmethod
    @APIFuncWrapper
    def QueryInfo(user_id: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(AdminAPI.qryAdmin % pre_deal_string(user_id))
            if res:
                return cur.fetchall()[0]
            else:
                return {'status': False}
