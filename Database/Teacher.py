from Database import database, pymysql, pre_deal_string, APIFuncWrapper


class TeacherAPI:
    """add or delete teacher"""
    addTeacher = 'insert into teacherinfo(user_id, name, gender, title, college) VALUES (%s, %s, %s, %s, %s)'
    delTeacher = '删除教师'
    altTeacher = '修改教师'
    qryTeacher = 'select * from teacherinfo where user_id like %s'
    """course arrangement"""
    queryActiveSchedule = '查询活跃课程表'
    queryNegativeSchedule = '查询非活跃课表'
    uploadScore = '上传学生成绩'

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
        return res == 1

    @staticmethod
    @APIFuncWrapper
    def QueryInfo(user_id: str):
        with database.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            res = cur.execute(TeacherAPI.qryTeacher % pre_deal_string(user_id))
            if res:
                return cur.fetchall()[0]
            else:
                return {'status': False}
