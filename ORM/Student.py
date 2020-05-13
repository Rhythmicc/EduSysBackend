from ORM.Tables import StudentInfo, StudentCourse
from . import APIFuncWrapper, to_dict, Session


class StudentAPI:
    @staticmethod
    @APIFuncWrapper
    def AddStudent(user_id: str, name: str, gender: bool,
                   college: str, profession: str, grade: int, session: Session = None):
        stu = StudentInfo(user_id=user_id, name=name, gender=gender,
                          college=college, profession=profession, grade=grade)
        session.add(stu)
        return True

    @staticmethod
    @APIFuncWrapper
    def DelStudent(user_id: str, session: Session = None):
        stu = session.query(StudentInfo).filter(StudentInfo.user_id.like(user_id)).first()
        session.delete(stu)
        return True

    @staticmethod
    @APIFuncWrapper
    def AltStudent(user_id: str, name: str, gender: bool,
                   college: str, profession: str, grade: int, session: Session = None):
        stu = session.query(StudentInfo).filter(StudentInfo.user_id.like(user_id)).first()
        if stu:
            stu.name = name
            stu.gender = gender
            stu.college = college
            stu.profession = profession
            stu.grade = grade
        return True

    @staticmethod
    @APIFuncWrapper
    def QryStudent(user_id: str, session: Session = None):
        stu = session.query(StudentInfo).filter(StudentInfo.user_id.like(user_id)).first()
        return to_dict(stu)

    @staticmethod
    @APIFuncWrapper
    def SelectAllStudentByCourse(course_id: int, session: Session = None):
        sls = session.query(StudentCourse.user_id)\
            .filter(StudentCourse.course_id == course_id)\
            .filter(StudentCourse.score < 0)\
            .all()
        res = session.query(StudentInfo).filter(StudentInfo.user_id.in_([i[0] for i in sls])).all()
        return [to_dict(i) for i in res] if res else {'status': False}
