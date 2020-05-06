from ORM.Tables import AdminInfo
from . import APIFuncWrapper, to_dict, Session


class AdminAPI:
    @staticmethod
    @APIFuncWrapper
    def AddAdmin(user_id: str, name: str, gender: bool, session: Session = None):
        obj = AdminInfo(user_id=user_id, name=name, gender=gender)
        session.add(obj)
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def DelAdmin(user_id: str, session: Session = None):
        user = session.query(AdminInfo).filter(AdminInfo.user_id.like(user_id)).first()
        session.delete(user)
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def AltAdmin(user_id: str, name: str, gender: bool, session: Session = None):
        user = session.query(AdminInfo).filter(AdminInfo.user_id.like(user_id)).first()
        user.name = name
        user.gender = gender
        return {'status': True}

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QryAdmin(user_id: str, session: Session = None):
        user = session.query(AdminInfo).filter(AdminInfo.user_id.like(user_id)).first()
        return to_dict(user)
