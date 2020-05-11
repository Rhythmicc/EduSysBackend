from ORM.Tables import CourseInfo, StudentCourse, TeacherCourse, Elective, SpElective
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
    @APIFuncWrapper
    def QryCourseNamed(name: str, session: Session = None):
        ls = session.query(CourseInfo).filter(CourseInfo.name.like('%' + name + '%')).all()
        ret = [to_dict(i) for i in ls] if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper
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
    @APIFuncWrapper
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
    @APIFuncWrapper
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
    @APIFuncWrapper
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
    @APIFuncWrapper
    def QryAllCourse(session: Session = None):
        ls = session.query(CourseInfo).all()
        ret = [to_dict(i) for i in ls] if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper
    def QrySelectableCourse(session: Session = None):
        rls = session.query(Elective.course_id, Elective.rest).filter(Elective.rest > 0).all()
        ls = session.query(CourseInfo).filter(CourseInfo.course_id.in_(
            [i[0] for i in rls]
        )).all()
        rls = {i[0]: i[1] for i in rls}
        ls = [to_dict(i) for i in ls]
        [i.update({'rest': rls[i['course_id']]}) for i in ls]
        ret = ls if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper
    def QryScheduleWithStudent(user_id: str, session: Session = None):
        week = autoCalWeek()
        ls = session.query(CourseInfo.time_ls, CourseInfo.name, CourseInfo.loc_ls) \
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
    def QryScheduleWithTeacher(user_id: str, session: Session = None):
        week = autoCalWeek()
        ls = session.query(CourseInfo.time_ls, CourseInfo.name, CourseInfo.loc_ls) \
            .filter(CourseInfo.course_id.in_(
                [i[0] for i in session.query(TeacherCourse.course_id)
                    .filter(TeacherCourse.course_id.in_(
                        [i[0] for i in session.query(CourseInfo.course_id)
                            .filter(CourseInfo.start_week <= week)
                            .filter(CourseInfo.start_week + CourseInfo.weeks > week).all()
                         ]))
                    .filter(TeacherCourse.user_id.like(user_id)).all()]
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
        week = autoCalWeek()
        if session.query(CourseInfo.course_id)\
                .filter(CourseInfo.course_id == course_id)\
                .filter(CourseInfo.start_week > week)\
                .first():
            session.add(SpElective(user_id=user_id, course_id=course_id))
            return {'status': True, 'msg': 'submit success'}
        else:
            return {'status': False, 'msg': '无课程或无法选课'}

    @staticmethod
    @APIFuncWrapper
    def ApproveSpSelectCourse(user_id: str, course_id: int, approve: bool, session: Session = None):
        target = session.query(SpElective)\
            .filter(SpElective.user_id.like(user_id))\
            .filter(SpElective.course_id == course_id).first()
        if target:
            if approve:
                session.add(StudentCourse(user_id=user_id, course_id=course_id))
            session.delete(target)
            return {'status': True, 'msg': 'Approve Success'}
        else:
            return {'status': False, 'msg': 'No such application'}

    @staticmethod
    @APIFuncWrapper
    def NeedApproveElective(session: Session = None):
        dt = session.query(SpElective.course_id, SpElective.user_id).all()
        cid_user = {}
        for i in dt:
            if i[0] not in cid_user:
                cid_user[i[0]] = []
            cid_user[i[0]].append(i[1])
        cls = session.query(CourseInfo.course_id, CourseInfo.name, CourseInfo.score)\
            .filter(CourseInfo.course_id.in_(list(cid_user.keys()))).all()
        ret = []
        for i in cls:
            for user in cid_user[i[0]]:
                ret.append({'course_id': i[0], 'name': i[1], 'score': i[2], 'user_id': user})
        return ret if ret else {'status': False, 'msg': 'No application'}

    @staticmethod
    @APIFuncWrapper
    def QryGrade(user_id: str, session: Session = None):
        ls = session.query(CourseInfo.name, StudentCourse.score) \
            .filter(CourseInfo.course_id == StudentCourse.course_id) \
            .filter(StudentCourse.user_id.like(user_id)) \
            .filter(StudentCourse.score >= 0).all()
        ret = {i[0]: i[1] for i in ls} if ls else {'status': False}
        return ret

    @staticmethod
    @APIFuncWrapper
    def QryAllCourseIdName(user_id: str, session: Session = None):
        ls = session.query(CourseInfo.course_id, CourseInfo.name).filter(CourseInfo.course_id.in_(
                [i[0] for i in session.query(TeacherCourse.course_id)
                    .filter(TeacherCourse.user_id.like(user_id))
                    .filter(TeacherCourse.active).all()]
        )).all()
        return {i[0]: i[1] for i in ls} if ls else {'status': False}

    @staticmethod
    @APIFuncWrapper
    def QryStudentsByCourseId(course_id, session: Session = None):
        ls = session.query(StudentCourse.user_id)\
            .filter(StudentCourse.course_id == course_id)\
            .filter(StudentCourse.score < 0).all()
        return [i[0] for i in ls] if ls else {'status': False}

    @staticmethod
    @APIFuncWrapper
    def QryGradesByStudent(user_id: str, session: Session = None):
        ls = session.query(StudentCourse.course_id, StudentCourse.score)\
            .filter(StudentCourse.user_id.like(user_id))\
            .filter(StudentCourse.score >= 0).all()
        scs = {i[0]: i[1] for i in ls}
        cids = [i[0] for i in ls]
        ls = session.query(CourseInfo).filter(CourseInfo.course_id.in_(cids)).all()
        ls = [to_dict(i) for i in ls]
        for _ in ls:
            _['grade'] = scs[_['course_id']]
        return ls if ls else {'status': False}

    @staticmethod
    @APIFuncWrapper
    def StudentCalendar(user_id: str, session: Session = None):
        week = autoCalWeek()
        cls = session.query(StudentCourse.course_id)\
            .filter(StudentCourse.user_id.like(user_id))\
            .filter(StudentCourse.score < 0).all()
        cls = session.query(CourseInfo.start_week, CourseInfo.weeks, CourseInfo.time_ls)\
            .filter(CourseInfo.course_id.in_([i[0] for i in cls]))\
            .filter(CourseInfo.start_week > week)\
            .all()
        return [{'start_week': i[0], 'weeks': i[1], 'time_ls': i[2]} for i in cls] if cls \
            else {'status': False, 'msg': 'No limit'}

    @staticmethod
    @APIFuncWrapper
    def DropableCourses(user_id: str, session: Session = None):
        week = autoCalWeek()
        cls = session.query(StudentCourse.course_id) \
            .filter(StudentCourse.user_id.like(user_id)) \
            .filter(StudentCourse.score < 0).all()
        cls = session.query(CourseInfo)\
            .filter(CourseInfo.course_id.in_([i[0] for i in cls]))\
            .filter(CourseInfo.start_week > week)\
            .all()
        return [to_dict(i) for i in cls] if cls else {'status': False}

    @staticmethod
    @APIFuncWrapper
    def DropCourse(user_id: str, course_id: int, session: Session = None):
        info = session.query(StudentCourse)\
            .filter(StudentCourse.user_id.like(user_id))\
            .filter(StudentCourse.course_id == course_id).first()
        if info:
            session.delete(info)
            info = session.query(Elective).filter(Elective.course_id == course_id).first()
            info.rest += 1
        return {'status': True}
