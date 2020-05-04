from . import database, pymysql, pre_deal_string, APIFuncWrapper


class StudentAPI:
    """query"""
    qryGrade = 'select courseinfo.name, studentcourse.score ' \
               'from courseinfo, studentcourse ' \
               'where courseinfo.course_id=studentcourse.course_id ' \
               'and studentcourse.score>0 and studentcourse.user_id like %s'
    qrySchedule = 'select name, weeks from courseinfo where course_id in ' \
                  '(select course_id from studentcourse where user_id like %s)'
    """add student"""
    addStudent = 'insert into studentinfo(user_id, name, gender, college, profession, grade) ' \
                 'VALUES (%s, %s, %s, %s, %s, %s)'
    delStudent = 'delete from studentinfo where user_id like %s'
    altStudent = 'update studentinfo set name=%s, gender=%s, college=%s, profession=%s, grade=%s where user_id like %s'
    qryStudent = 'select * from studentinfo where user_id like %s'

    @staticmethod
    @APIFuncWrapper
    def AddStudent(user_id: str, name: str, gender: bool,
                   college: str, profession: str, grade: int):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(StudentAPI.addStudent % (
                pre_deal_string(user_id),
                pre_deal_string(name),
                gender,
                pre_deal_string(college),
                pre_deal_string(profession), grade
            ))
        database.commit()
        return True

    @staticmethod
    @APIFuncWrapper
    def DelStudent(user_id: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(StudentAPI.delStudent % pre_deal_string(user_id))
            database.commit()
        return res

    @staticmethod
    @APIFuncWrapper
    def AltStudent(user_id: str, name: str, gender: bool,
                   college: str, profession: str, grade: int):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(StudentAPI.addStudent % (
                pre_deal_string(name),
                gender,
                pre_deal_string(college),
                pre_deal_string(profession), grade,
                pre_deal_string(user_id)
            ))
        database.commit()
        return True

    @staticmethod
    @APIFuncWrapper
    def QrySchedule(user_id):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(StudentAPI.qrySchedule % pre_deal_string(user_id))
            return cur.fetchall()

    @staticmethod
    @APIFuncWrapper
    def QueryInfo(user_id):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(StudentAPI.qryStudent % pre_deal_string(user_id))
            if res:
                return cur.fetchall()[0]
            else:
                return {'status': False}

    @staticmethod
    @APIFuncWrapper
    def QryGrade(user_id):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(StudentAPI.qryGrade % pre_deal_string(user_id))
            return cur.fetchall()
