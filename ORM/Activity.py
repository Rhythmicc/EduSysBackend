from ORM.Tables import ActivityStatus
from . import APIFuncWrapper, to_dict, Session
from ORM.RegisteredActivities import ElectiveActivity


ActivityName = {
    'elective': ElectiveActivity
}


class ActivityAPI:
    @staticmethod
    @APIFuncWrapper
    def AddActivity(activity: str, session: Session = None):
        event = ActivityStatus()
        event.activity = activity
        event.status = True
        session.add(event)
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def DelActivity(activity: str, session: Session = None):
        session.delete(session.query(ActivityStatus).filter(ActivityStatus.status == activity).first())
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def EnableActivity(activity: str, session: Session = None):
        act = session.query(ActivityStatus).filter(ActivityStatus.activity == activity).first()
        act.status = True
        ActivityName[activity].enable()
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def DisableActivity(activity: str, session: Session = None):
        act = session.query(ActivityStatus).filter(ActivityStatus.activity == activity).first()
        act.status = False
        ActivityName[activity].disable()
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def QryActivity(activity: str, session: Session = None):
        act = session.query(ActivityStatus).filter(ActivityStatus.activity == activity).first()
        return to_dict(act) if act else {'status': False}
