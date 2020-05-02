from Database.Student import StudentAPI
from Database.Teacher import TeacherAPI
from Database.Admin import AdminAPI
from fastapi import APIRouter
from . import *

router = APIRouter()


@router.get('/info/student/{user_id}')
async def QueryStudentInfo(user_id: str):
    return StudentAPI.QueryInfo(user_id)


@router.get('/info/teacher/{user_id}')
async def QueryTeacherInfo(user_id: str):
    return TeacherAPI.QueryInfo(user_id)


@router.get('/info/manager/{user_id}')
async def QueryManagerInfo(user_id: str):
    return AdminAPI.QueryInfo(user_id)


@router.post('/info/altStudent')
async def AltStudent(dt: StudentInfo):
    return {'status': StudentAPI.AltStudent(
        dt.user_id, dt.name, dt.gender == 'male',
        dt.college, dt.profession, dt.grade)}


@router.post('/info/altTeacher')
async def AltTeacher(dt: TeacherInfo):
    return {'status': TeacherAPI.AltTeacher(
        dt.user_id, dt.name, dt.gender == 'male',
        dt.title, dt.college)}


@router.post('/info/altManager')
async def AltManager(dt: AdminInfo):
    return {'status': AdminAPI.AltAdmin(
        dt.user_id, dt.name, dt.gender == 'male')}
