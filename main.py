from Database.Users import UserAPI
from Database.Student import StudentAPI
from Database.Teacher import TeacherAPI
from Database.Admin import AdminAPI
from __init__ import *
import fastapi
server = fastapi.FastAPI()


@server.get('/login/{user_id}')
async def login(user_id: str, pwd: str):
    status, role = UserAPI.query(user_id, pwd)
    return {'status': status, 'role': role}


@server.post('/register/student')
async def register_student(dt: StudentInfo):
    msg = 'User exists'
    res = UserAPI().register(dt.user_id, dt.pwd, 0)
    if res:
        res = StudentAPI.AddStudent(dt.user_id, dt.name, dt.gender == 'male',
                                    dt.college, dt.profession, dt.grade)
        msg = 'success' if res else 'failed'
        if not res:
            UserAPI.delete(dt.user_id)
    return {'status': res, 'msg': msg}


@server.post('/register/teacher')
async def register_teacher(dt: TeacherInfo):
    msg = 'User exists'
    res = UserAPI.register(dt.user_id, dt.pwd, 1)
    if res:
        res = TeacherAPI.AddTeacher(dt.user_id, dt.name, dt.gender == 'male', dt.title, dt.college)
        msg = 'success' if res else 'failed'
        if not res:
            UserAPI.delete(dt.user_id)
    return {'status': res, 'msg': msg}


@server.post('/register/manager')
async def register_manager(dt: AdminInfo):
    msg = 'User exists'
    res = UserAPI.register(dt.user_id, dt.pwd, 2)
    if res:
        res = AdminAPI.AddAdmin(dt.user_id, dt.name, dt.gender == 'male')
        msg = 'success' if res else 'failed'
        if not res:
            UserAPI.delete(dt.user_id)
    return {'status': res, 'msg': msg}


@server.get('/info/student/{user_id}')
async def QueryStudentInfo(user_id: str):
    return StudentAPI.QueryInfo(user_id)


@server.get('/info/teacher/{user_id}')
async def QueryTeacherInfo(user_id: str):
    return TeacherAPI.QueryInfo(user_id)


@server.get('/info/manager/{user_id}')
async def QueryManagerInfo(user_id: str):
    return AdminAPI.QueryInfo(user_id)


@server.get('/d7f6g78d678g6d78g6d')
async def QuitService():
    from Database import CloseDatabase
    CloseDatabase()
    exit(0)
