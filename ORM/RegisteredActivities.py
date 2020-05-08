from ORM.Tables import Elective, CourseInfo
from . import APIFuncWrapper, Session, autoCalWeek


class ElectiveActivity:
    status: bool = False

    @staticmethod
    @APIFuncWrapper
    def enable(session: Session = None):
        if ElectiveActivity.status:
            return {'status': True}
        else:
            week = autoCalWeek()
            session.delete(session.query(Elective).all())
            cid = session.query(CourseInfo.course_id).filter(CourseInfo.start_week > week).all()
            for i in cid:
                session.add(Elective(course_id=i[0], rest=100))
            return {'status': True}

    @staticmethod
    def disable():
        ElectiveActivity.status = False
        return {'status': True}
