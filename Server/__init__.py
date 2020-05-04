from pydantic import BaseModel
name = 'EduSysBackend'


class StudentInfo(BaseModel):
    user_id: str
    pwd: str
    name: str
    gender: str
    college: str
    profession: str
    grade: int


class TeacherInfo(BaseModel):
    user_id: str
    pwd: str
    name: str
    gender: str
    title: str
    college: str


class AdminInfo(BaseModel):
    user_id: str
    pwd: str
    name: str
    gender: str


class CourseInfo(BaseModel):
    course_id: int = -1
    name: str
    score: int
    weeks: int
    time_ls: list
    loc_ls: list


class DayForm(BaseModel):
    year: int
    semester: int
    start_day: str
