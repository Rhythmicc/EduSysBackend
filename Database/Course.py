from Database import database, pymysql, pre_deal_string, APIFuncWrapper


class CourseAPI:
    addCourse = 'insert into courseinfo(name, score, weeks, time_ls, loc_ls) VALUES (%s, %s, %s, %s, %s)'
    addCourseScore = 'update studentcourse set score=%s where user_id=%s and course_id=%s'
    delCourse = 'delete from courseinfo where course_id=%s'
    delCourseScore = 'update studentcourse set score=-1 where user_id=%s and course_id=%s'
    altCourse = 'update courseinfo set name=%s, score=%s, weeks=%s, time_ls=%s, loc_ls=%s where course_id=%s'
    qryCourse = 'select * from courseinfo where course_id=%s'
    qryCourseNamed = 'select * from courseinfo where name like %s'
    qryActiveCourseWithStudent = 'select * from studentcourse where user_id=%s and score=-1'
    qryHistoryCourseWithStudent = 'select * from studentcourse where user_id=%s and score>0'
    qryActiveCourseWithTeacher = 'select * from teachercourse where user_id=%s and active'
    qryHistoryCourseWithTeacher = 'select * from teachercourse where user_id=%s and not active'
    qrySelectableCourse = 'select * from courseinfo where course_id in (select course_id from elective where rest>0)'
    qryAllCourse = 'select * from courseinfo'
    selectCourse = 'insert into studentcourse(user_id, course_id) VALUES (%s, %s)'

    @staticmethod
    @APIFuncWrapper
    def AddCourse(name: str, score: int, weeks: int, time_ls: list, loc_ls: list):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.addCourse % (pre_deal_string(name), score, weeks,
                                                     pre_deal_string(' '.join(time_ls)),
                                                     pre_deal_string(' '.join(loc_ls))))
            database.commit()
        return res

    @staticmethod
    @APIFuncWrapper
    def AddCourseScore(user_id: str, course_id: int, score: float):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.addCourseScore % (score, pre_deal_string(user_id), course_id))
            database.commit()
        return res

    @staticmethod
    @APIFuncWrapper
    def DelCourse(course_id: int):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.delCourse % course_id)
            database.commit()
        return res

    @staticmethod
    @APIFuncWrapper
    def DelCourseScore(user_id: str, course_id: int):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.delCourseScore % (pre_deal_string(user_id), course_id))
            database.commit()
        return res

    @staticmethod
    @APIFuncWrapper
    def AltCourse(course_id: int, name: str, score: int, weeks: int, time_ls: list, loc_ls: list):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.altCourse % (pre_deal_string(name), score, weeks,
                                                     pre_deal_string(' '.join(time_ls)),
                                                     pre_deal_string(' '.join(loc_ls)), course_id))
            database.commit()
        return res

    @staticmethod
    @APIFuncWrapper
    def QryCourse(couser_id: int):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.qryCourse % couser_id)
            if res:
                return cur.fetchall()[0]
            else:
                return {'status': False}

    @staticmethod
    @APIFuncWrapper
    def QryCourseNamed(name: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.qryCourseNamed % pre_deal_string(name))
            if res:
                return cur.fetchall()
            else:
                return {'status': False}

    @staticmethod
    @APIFuncWrapper
    def QryActiveCourseWithStudent(user_id: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.qryActiveCourseWithStudent % pre_deal_string(user_id))
            if res:
                return cur.fetchall()
            else:
                return {'status': False}

    @staticmethod
    @APIFuncWrapper
    def QryActiveCourseWithTeacher(user_id: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.qryActiveCourseWithTeacher % pre_deal_string(user_id))
            if res:
                return cur.fetchall()
            else:
                return {'status': False}

    @staticmethod
    @APIFuncWrapper
    def QryHistoryCourseWithStudent(user_id: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.qryHistoryCourseWithStudent % pre_deal_string(user_id))
            if res:
                return cur.fetchall()
            else:
                return {'status': False}

    @staticmethod
    @APIFuncWrapper
    def QryHistoryCourseWithTeacher(user_id: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.qryHistoryCourseWithTeacher % pre_deal_string(user_id))
            if res:
                return cur.fetchall()
            else:
                return {'status': False}

    @staticmethod
    @APIFuncWrapper
    def QryAllCourse():
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(CourseAPI.qryAllCourse)
            if res:
                return cur.fetchall()
            else:
                return {'status': False}

    @staticmethod
    @APIFuncWrapper
    def QrySelectableCourse():
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(CourseAPI.qrySelectableCourse)
            return cur.fetchall()

    @staticmethod
    @APIFuncWrapper
    def SelectCourse(user_id: str, course_id: int):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(CourseAPI.selectCourse % (pre_deal_string(user_id), course_id))
            database.commit()
        return True
