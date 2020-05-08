from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean, Float, \
    UniqueConstraint, Date, Index, PrimaryKeyConstraint, ForeignKey
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(String(30), primary_key=True, nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    role = Column(Integer, nullable=False)


class StudentInfo(Base):
    __tablename__ = 'studentinfo'
    user_id = Column(String(30), primary_key=True, nullable=False, unique=True)
    name = Column(String(10), nullable=False)
    gender = Column(Boolean, nullable=False)
    college = Column(String(15), nullable=False)
    profession = Column(String(15), nullable=False)
    grade = Column(Integer, nullable=False)
    courses = relationship("StudentCourse", back_populates="student")


class TeacherInfo(Base):
    __tablename__ = 'teacherinfo'
    user_id = Column(String(30), primary_key=True, nullable=False, unique=True)
    name = Column(String(10), nullable=False)
    gender = Column(Boolean, nullable=False)
    college = Column(String(15), nullable=False)
    title = Column(String(10), nullable=False)
    courses = relationship("TeacherCourse", back_populates="teacher")


class AdminInfo(Base):
    __tablename__ = 'admininfo'
    user_id = Column(String(30), primary_key=True, nullable=False, unique=True)
    name = Column(String(10), nullable=False)
    gender = Column(Boolean, nullable=False)


class CourseInfo(Base):
    __tablename__ = 'courseinfo'
    course_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(30), nullable=False)
    score = Column(Integer, nullable=False)
    start_week = Column(Integer, nullable=False)
    weeks = Column(Integer, nullable=False)
    time_ls = Column(String(50), nullable=False)
    loc_ls = Column(String(50), nullable=False)


class StudentCourse(Base):
    __tablename__ = "studentcourse"
    user_id = Column(String(30), ForeignKey("studentinfo.user_id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courseinfo.course_id"), nullable=False, index=True)
    score = Column(Float, default=-1)
    student = relationship('StudentInfo', back_populates="courses")
    __table_args__ = (
        UniqueConstraint(user_id, course_id, name='studentcourse_user_id_course_id_uindex'),
        PrimaryKeyConstraint(user_id, course_id),
        Index(user_id, course_id, unique=True)
    )


class TeacherCourse(Base):
    __tablename__ = "teachercourse"
    user_id = Column(String(30), ForeignKey("teacherinfo.user_id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courseinfo.course_id"), nullable=False, index=True)
    active = Column(Boolean, default=True)
    teacher = relationship("TeacherInfo", back_populates="courses")
    __table_args__ = (
        UniqueConstraint(user_id, course_id, name='teachercourse_user_id_course_id_uindex'),
        PrimaryKeyConstraint(user_id, course_id),
        Index(user_id, course_id, unique=True)
    )


class Elective(Base):
    __tablename__ = 'elective'
    course_id = Column(Integer, nullable=False, index=True, primary_key=True)
    rest = Column(Integer, nullable=False)


class TimeInfo(Base):
    __tablename__ = 'timeinfo'
    year = Column(Integer, nullable=False, index=True)
    semester = Column(Integer, nullable=False, index=True)
    start_day = Column(Date, nullable=False)
    __table_args__ = (
        UniqueConstraint(year, semester, name='timeinfo_year_semester_uindex'),
        PrimaryKeyConstraint(year, semester),
        Index(year, semester, unique=True)
    )


class ActivityStatus(Base):
    __tablename__ = 'activitystatus'
    activity = Column(String(30), nullable=False, index=True, primary_key=True)
    status = Column(Boolean, nullable=False)
