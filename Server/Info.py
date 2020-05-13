from ORM.Student import StudentAPI
from ORM.Teacher import TeacherAPI
from ORM.Admin import AdminAPI
from ORM.Course import CourseAPI
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


@router.get('/StudentCalendar/{user_id}')
async def Student_Calendar(user_id: str):
    return CourseAPI.StudentCalendar(user_id)


@router.get('/AllStudentByCourse/{course_id}')
async def All_Student_By_Course(course_id: int):
    return StudentAPI.SelectAllStudentByCourse(course_id)
