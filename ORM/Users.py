from ORM.Tables import User
from ORM import APIFuncWrapper, Session


class UserAPI:
    @staticmethod
    @APIFuncWrapper
    def AddUser(user_id: str, password: str, role: int, session: Session = None):
        ck = session.query(User).filter(User.user_id.like(user_id)).first()
        ret = {'status': False, 'msg': 'User Exists'} if ck else {'status': True}
        if not ck:
            obj = User(user_id=user_id, password=password, role=role)
            session.add(obj)
        return ret

    @staticmethod
    @APIFuncWrapper
    def DelUser(user_id: str, session: Session = None):
        ret = False
        user = session.query(User).filter(User.user_id.like(user_id)).first()
        if user:
            session.delete(user)
            ret = True
        return {'status': ret}

    @staticmethod
    @APIFuncWrapper
    def AltUser(user_id: str, password: str, role: int, session: Session = None):
        ret = False
        user = session.query(User).filter(User.user_id.like(user_id)).first()
        if user:
            user.password = password
            user.role = role
            ret = True
        return {'status': ret}

    @staticmethod
    @APIFuncWrapper
    def QryUser(user_id: str, password: str, session: Session = None):
        user = session.query(User).filter(User.user_id.like(user_id)).first()
        ret = {'status': user.password == password, 'role': user.role} \
            if user else {'status': False, 'msg': 'User not exists!'}
        return ret
