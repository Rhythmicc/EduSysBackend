from ORM.Users import UserAPI
from ORM.Student import StudentAPI
from ORM.Teacher import TeacherAPI
from ORM.Admin import AdminAPI
from . import *
from fastapi import APIRouter

router = APIRouter()


@router.get('/login/{user_id}')
async def login(user_id: str, pwd: str):
    return UserAPI.QryUser(user_id, pwd)


@router.post('/register/student')
async def register_student(dt: StudentInfo):
    res = UserAPI.AddUser(dt.user_id, dt.pwd, 0)
    if res['status']:
        ret = StudentAPI.AddStudent(dt.user_id, dt.name, dt.gender == 'male',
                                    dt.college, dt.profession, dt.grade)
        res['msg'] = 'success' if ret['status'] else 'failed'
        if not ret['status']:
            UserAPI.DelUser(dt.user_id)
    return res


@router.post('/register/teacher')
async def register_teacher(dt: TeacherInfo):
    res = UserAPI.AddUser(dt.user_id, dt.pwd, 1)
    if res['status']:
        ret = TeacherAPI.AddTeacher(dt.user_id, dt.name, dt.gender == 'male', dt.title, dt.college)
        res['msg'] = 'success' if ret['status'] else 'failed'
        if not ret['status']:
            UserAPI.DelUser(dt.user_id)
    return res


@router.post('/register/manager')
async def register_manager(dt: AdminInfo):
    res = UserAPI.AddUser(dt.user_id, dt.pwd, 2)
    if res['status']:
        ret = AdminAPI.AddAdmin(dt.user_id, dt.name, dt.gender == 'male')
        res['msg'] = 'success' if ret['status'] else 'failed'
        if not ret['status']:
            UserAPI.DelUser(dt.user_id)
    return res
