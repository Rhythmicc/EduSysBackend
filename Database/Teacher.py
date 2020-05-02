from Database import database, pymysql, pre_deal_string, APIFuncWrapper


class TeacherAPI:
    """add or delete teacher"""
    addTeacher = 'insert into teacherinfo(user_id, name, gender, title, college) VALUES (%s, %s, %s, %s, %s)'
    delTeacher = 'delete from teacherinfo where user_id like %s'
    altTeacher = 'update teacherinfo set name=%s, gender=%s, title=%s, college=%s where user_id like %s'
    qryTeacher = 'select * from teacherinfo where user_id like %s'

    @staticmethod
    @APIFuncWrapper
    def AddTeacher(user_id: str, name: str, gender: bool,
                   title: str, college: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(TeacherAPI.addTeacher % (
                pre_deal_string(user_id),
                pre_deal_string(name), gender,
                pre_deal_string(title),
                pre_deal_string(college)
            ))
        database.commit()
        return res

    @staticmethod
    @APIFuncWrapper
    def DelTeacher(user_id: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(TeacherAPI.delTeacher % pre_deal_string(user_id))
            database.commit()
        return res

    @staticmethod
    @APIFuncWrapper
    def AltTeacher(user_id: str, name: str, gender: bool,
                   title: str, college: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(TeacherAPI.altTeacher % (
                pre_deal_string(name), gender,
                pre_deal_string(title),
                pre_deal_string(college),
                pre_deal_string(user_id)
            ))
        database.commit()
        return res

    @staticmethod
    @APIFuncWrapper
    def QueryInfo(user_id: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(TeacherAPI.qryTeacher % pre_deal_string(user_id))
            if res:
                return cur.fetchall()[0]
            else:
                return {'status': False}
