from ORM.Tables import Elective, CourseInfo
from . import APIFuncWrapper, Session, autoCalWeek


class ElectiveActivity:
    @staticmethod
    @APIFuncWrapper
    def enable(session: Session = None):
        week = autoCalWeek()
        ls = session.query(Elective).all()
        for i in ls:
            session.delete(i)
        cid = session.query(CourseInfo.course_id).filter(CourseInfo.start_week > week).all()
        for i in cid:
            session.add(Elective(course_id=i[0], rest=100))
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def disable(session: Session = None):
        session.delete(session.query(Elective).all())
        return {'status': True}
