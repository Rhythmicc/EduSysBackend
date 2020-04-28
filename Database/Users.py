from Database import database, pymysql, pre_deal_string, APIFuncWrapper


class UserAPI:
    login = 'select password,role from users where user_id like %s'
    count = 'select user_id from users where user_id like %s'
    insert = 'insert into users(user_id, password, role) VALUES (%s, %s, %s)'
    delete = 'delete from users where user_id=%s'

    @staticmethod
    @APIFuncWrapper
    def query(user_id, password):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(UserAPI.login % pre_deal_string(user_id))
            if res:
                res = cur.fetchall()[0]
                status = res['password'] == password
                return status, res['role']
            else:
                status = False
                return status, '-1'

    @staticmethod
    @APIFuncWrapper
    def exists(user_id):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(UserAPI.count % user_id)
        return res

    @staticmethod
    @APIFuncWrapper
    def register(user_id, password, role):
        user_id = pre_deal_string(user_id)
        if UserAPI.exists(user_id):
            return False
        else:
            with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
                res = cur.execute(UserAPI.insert % (user_id, pre_deal_string(password), role))
            database.commit()
            return res == 1

    @staticmethod
    @APIFuncWrapper
    def unregister(user_id):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(UserAPI.delete % pre_deal_string(user_id))
        database.commit()
        return res == 1
