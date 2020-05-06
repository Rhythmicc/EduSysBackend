from ORM.Tables import CourseInfo, StudentCourse, TeacherCourse, Elective
from . import APIFuncWrapper, to_dict, autoCalWeek, Session


class CourseAPI:
    @staticmethod
    @APIFuncWrapper
    def AddCourse(name: str, score: int, start_week: int,
                  weeks: int, time_ls: str, loc_ls: str, session: Session = None):
        session.add(CourseInfo(
            name=name, score=score, start_week=start_week,
            weeks=weeks, time_ls=time_ls, loc_ls=loc_ls
        ))
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def DelCourse(course_id: int, session: Session = None):
        course = session.query(CourseInfo).filter_by(course_id=course_id).first()
        session.delete(course)
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def AltCourse(course_id: int, name: str, score: int,
                  start_week: int, weeks: int, time_ls: str, loc_ls: str, session: Session = None):
        course = session.query(CourseInfo).filter_by(course_id=course_id).first()
        course.name = name
        course.score = score
        course.start_week = start_week
        course.weeks = weeks
        course.time_ls = time_ls
        course.loc_ls = loc_ls
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def QryCourse(course_id: int, session: Session = None):
        course = session.query(CourseInfo).filter_by(course_id=course_id).first()
        return to_dict(course)

    @staticmethod
    @APIFuncWrapper
    def AddCourseScore(user_id: str, course_id: int, score: float, session: Session = None):
        sc = session.query(StudentCourse).filter_by(user_id=user_id, course_id=course_id).first()
        sc.score = score
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def DelCourseScore(user_id: str, course_id: int, session: Session = None):
        sc = session.query(StudentCourse).filter_by(user_id=user_id, course_id=course_id).first()
        sc.score = -1
        return {'status': True}

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QryCourseNamed(name: str, session: Session = None):
        ls = session.query(CourseInfo).filter(CourseInfo.name.like('%' + name + '%')).all()
        ret = [to_dict(i) for i in ls] if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QryActiveCourseWithStudent(user_id: str, session: Session = None):
        ls = session.query(CourseInfo) \
            .filter(CourseInfo.course_id.in_(
                [i[0] for i in session.query(StudentCourse.course_id)
                    .filter(StudentCourse.user_id.like(user_id))
                    .filter(StudentCourse.score < 0).all()]
            )
        ).all()
        ret = [to_dict(i) for i in ls] if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QryActiveCourseWithTeacher(user_id: str, session: Session = None):
        ls = session.query(CourseInfo) \
            .filter(CourseInfo.course_id.in_(
                [i[0] for i in session.query(TeacherCourse.course_id)
                    .filter(TeacherCourse.user_id.like(user_id))
                    .filter(TeacherCourse.active).all()]
            )
        ).all()
        ret = [to_dict(i) for i in ls] if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QryHistoryCourseWithStudent(user_id: str, session: Session = None):
        ls = session.query(CourseInfo) \
            .filter(CourseInfo.course_id.in_(
                [i[0] for i in session.query(StudentCourse.course_id)
                    .filter(StudentCourse.user_id.like(user_id))
                    .filter(StudentCourse.score >= 0).all()]
            )
        ).all()
        ret = [to_dict(i) for i in ls] if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QryHistoryCourseWithTeacher(user_id: str, session: Session = None):
        ls = session.query(CourseInfo) \
            .filter(CourseInfo.course_id.in_(
                [i[0] for i in session.query(TeacherCourse.course_id)
                    .filter(TeacherCourse.user_id.like(user_id))
                    .filter(not TeacherCourse.active).all()]
            )
        ).all()
        ret = [to_dict(i) for i in ls] if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QryAllCourse(session: Session = None):
        ls = session.query(CourseInfo).all()
        ret = [to_dict(i) for i in ls] if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QrySelectableCourse(session: Session = None):
        ls = session.query(CourseInfo).filter(CourseInfo.course_id.in_(
            [i[0] for i in session.query(Elective.course_id).filter(Elective.rest > 0).all()]
        )).all()
        ret = [to_dict(i) for i in ls] if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QryScheduleWithStudent(user_id: str, session: Session = None):
        week = autoCalWeek()
        ls = session.query(CourseInfo.time_ls, CourseInfo.name) \
            .filter(CourseInfo.course_id.in_(
                [i[0] for i in session.query(StudentCourse.course_id)
                    .filter(StudentCourse.course_id.in_(
                        [i[0] for i in session.query(CourseInfo.course_id)
                            .filter(CourseInfo.start_week <= week)
                            .filter(CourseInfo.start_week + CourseInfo.weeks > week).all()
                         ]))
                    .filter(StudentCourse.user_id.like(user_id)).all()]
            )).all()
        ret = ls if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QryScheduleWithTeacher(user_id: str, session: Session = None):
        week = autoCalWeek()
        ls = session.query(CourseInfo.time_ls, CourseInfo.name) \
            .filter(CourseInfo.course_id.in_(
                [i[0] for i in session.query(StudentCourse.course_id)
                    .filter(StudentCourse.course_id.in_(
                        [i[0] for i in session.query(CourseInfo.course_id)
                            .filter(CourseInfo.start_week <= week)
                            .filter(CourseInfo.start_week + CourseInfo.weeks > week).all()
                        ]))
                    .filter(StudentCourse.user_id.like(user_id)).all()]
        )).all()
        ret = ls if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper
    def SelectCourse(user_id: str, course_id: int, session: Session = None):
        rest = session.query(Elective).filter(Elective.course_id == course_id and Elective.rest > 0).first()
        rest.rest -= 1
        session.commit()
        session.add(StudentCourse(user_id=user_id, course_id=course_id))
        return {'status': True}

    @staticmethod
    @APIFuncWrapper
    def SpecialSelectCourse(user_id: str, course_id: int, session: Session = None):
        session.add(StudentCourse(user_id=user_id, course_id=course_id))
        return {'status': True}

    @staticmethod
    @APIFuncWrapper(need_commit=False)
    def QryGrade(user_id: str, session: Session = None):
        ls = session.query(CourseInfo.name, StudentCourse.score) \
            .filter(CourseInfo.course_id == StudentCourse.course_id) \
            .filter(StudentCourse.user_id.like(user_id)) \
            .filter(StudentCourse.score >= 0).all()
        ret = {i[0]: i[1] for i in ls} if ls else {'status': False}
        return ret
