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
