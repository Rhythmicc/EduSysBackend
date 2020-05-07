from ORM.Tables import TeacherInfo
from . import APIFuncWrapper, to_dict, Session


class TeacherAPI:
    @staticmethod
    @APIFuncWrapper
    def AddTeacher(user_id: str, name: str, gender: bool,
                   college: str, title: str, session: Session = None):
        tc = TeacherInfo(user_id=user_id, name=name, gender=gender,
                         college=college, title=title)
        session.add(tc)
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def DelTeacher(user_id: str, session: Session = None):
        tc = session.query(TeacherInfo).filter(TeacherInfo.user_id.like(user_id)).first()
        session.delete(tc)
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def AltTeacher(user_id: str, name: str, gender: bool,
                   college: str, title: str, session: Session = None):
        tc = session.query(TeacherInfo).filter(TeacherInfo.user_id.like(user_id)).first()
        if tc:
            tc.name = name
            tc.gender = gender
            tc.college = college
            tc.title = title
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def QryTeacher(user_id: str, session: Session = None):
        tc = session.query(TeacherInfo).filter(TeacherInfo.user_id.like(user_id)).first()
        return to_dict(tc)
