from ORM.Tables import TimeInfo
from . import APIFuncWrapper, Session
from datetime import datetime


class OptionAPI:
    @staticmethod
    @APIFuncWrapper
    def SetStartDay(year: int, semester: int, start_day: str, session: Session = None):
        ret = {'status': True}
        tm = session.query(TimeInfo)\
            .filter(TimeInfo.year == year)\
            .filter(TimeInfo.semester == semester).first()
        if tm:
            tm.start_day = datetime.strptime(start_day, "%Y%m%d").date()
        else:
            ret['status'] = False
        return ret

    @staticmethod
    @APIFuncWrapper
    def AddStartDay(year: int, semester: int, start_day: str, session: Session = None):
        return {'status': True} if session.add(TimeInfo(
            year=year, semester=semester, start_day=datetime.strptime(start_day, "%Y%m%d").date()
        )) else {'status': False}
