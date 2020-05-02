from Database.Users import UserAPI
from Database.Student import StudentAPI
from Database.Teacher import TeacherAPI
from Database.Admin import AdminAPI
from . import *
from fastapi import APIRouter

router = APIRouter()


@router.get('/login/{user_id}', tags=['user'])
async def login(user_id: str, pwd: str):
    status, role = UserAPI.query(user_id, pwd)
    return {'status': status, 'role': role}


@router.post('/register/student', tags=['user'])
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


@router.post('/register/teacher', tags=['user'])
async def register_teacher(dt: TeacherInfo):
    msg = 'User exists'
    res = UserAPI.register(dt.user_id, dt.pwd, 1)
    if res:
        res = TeacherAPI.AddTeacher(dt.user_id, dt.name, dt.gender == 'male', dt.title, dt.college)
        msg = 'success' if res else 'failed'
        if not res:
            UserAPI.delete(dt.user_id)
    return {'status': res, 'msg': msg}


@router.post('/register/manager', tags=['user'])
async def register_manager(dt: AdminInfo):
    msg = 'User exists'
    res = UserAPI.register(dt.user_id, dt.pwd, 2)
    if res:
        res = AdminAPI.AddAdmin(dt.user_id, dt.name, dt.gender == 'male')
        msg = 'success' if res else 'failed'
        if not res:
            UserAPI.delete(dt.user_id)
    return {'status': res, 'msg': msg}
