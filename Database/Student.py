from Database import database, pymysql, pre_deal_string, APIFuncWrapper


class StudentAPI:
    """query"""
    queryGrade = 'select courseinfo.name, studentcourse.score ' \
                 'from courseinfo, studentcourse ' \
                 'where courseinfo.course_id=studentcourse.course_id ' \
                 'and studentcourse.score>0 and studentcourse.user_id like %s'
    querySchedule = 'select name, weeks from courseinfo where course_id in ' \
                    '(select course_id from studentcourse where user_id like %s)'
    """CurriculaVariable"""
    validCourses = 'select * from courseinfo where course_id in (select course_id from elective where rest>0)'
    chooseCourse = 'insert into studentcourse(user_id, course_id) VALUES (%s, %s)'
    """add student"""
    addStudent = 'insert into studentinfo(user_id, name, gender, college, profession, grade) ' \
                 'VALUES (%s, %s, %s, %s, %s, %s)'
    delStudent = 'delete from studentinfo where user_id like %s'
    altStudent = '修改学生'
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
    def ChooseCourse(user_id, course_id):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(StudentAPI.chooseCourse % (pre_deal_string(user_id), course_id))
        database.commit()
        return True

    @staticmethod
    @APIFuncWrapper
    def ValidCourses():
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(StudentAPI.validCourses)
            return cur.fetchall()

    @staticmethod
    @APIFuncWrapper
    def QuerySchedule(user_id):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(StudentAPI.querySchedule % pre_deal_string(user_id))
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
    def QueryGrade(user_id):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(StudentAPI.queryGrade % pre_deal_string(user_id))
            return cur.fetchall()
