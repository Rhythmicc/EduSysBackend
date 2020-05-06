from ORM.Student import StudentAPI
from ORM.Teacher import TeacherAPI
from ORM.Admin import AdminAPI
from fastapi import APIRouter
from . import *

router = APIRouter()


@router.get('/student/{user_id}')
async def Query_Student_Info(user_id: str):
    return StudentAPI.QryStudent(user_id)


@router.get('/teacher/{user_id}')
async def Query_Teacher_Info(user_id: str):
    return TeacherAPI.QryTeacher(user_id)


@router.get('/manager/{user_id}')
async def Query_Manager_Info(user_id: str):
    return AdminAPI.QryAdmin(user_id)


@router.post('/altStudent')
async def Alter_Student(dt: StudentInfo):
    return StudentAPI.AltStudent(
        dt.user_id, dt.name, dt.gender == 'male',
        dt.college, dt.profession, dt.grade)


@router.post('/altTeacher')
async def Alter_Teacher(dt: TeacherInfo):
    return TeacherAPI.AltTeacher(
        dt.user_id, dt.name, dt.gender == 'male',
        dt.title, dt.college)


@router.post('/info/altManager')
async def AltManager(dt: AdminInfo):
    return AdminAPI.AltAdmin(dt.user_id, dt.name, dt.gender == 'male')
