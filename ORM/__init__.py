import datetime
import math

from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('mysql+pymysql://edu_sys_client:P7pXAFKXbMLB3D5vTdmhnT4OX96XFQBd@rm-2ze17saovz0800382ao.mysql'
                       '.rds.aliyuncs.com/softwaredesign', encoding='utf-8')
Session = sessionmaker(bind=engine)


def APIFuncWrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = scoped_session(Session)
        try:
            ret = func(*args, **kwargs, session=session)
            session.commit()
        except Exception as e:
            print(repr(e))
            ret = {'status': False}
            session.rollback()
        finally:
            session.close()
        return ret
    return wrapper


def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


@APIFuncWrapper
def autoCalWeek(session: Session = None):
    from ORM.Tables import TimeInfo
    today = datetime.date.today()
    year = today.year
    semester = 1 if today.month <= 7 else 2
    start_day = session.query(TimeInfo.start_day).filter(
        TimeInfo.year == year and TimeInfo.semester == semester).first()
    if start_day:
        return math.ceil(((today - start_day[0]).days + 1) / 7)
    else:
        return False
