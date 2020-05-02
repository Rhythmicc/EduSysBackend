from Database.Student import StudentAPI
from Database.Teacher import TeacherAPI
from Database.Admin import AdminAPI
from fastapi import APIRouter

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
