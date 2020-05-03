from Database.Course import CourseAPI
from fastapi import APIRouter

router = APIRouter()


@router.get('/Student/Schedule/{user_id}')
async def Student_Schedule(user_id: str):
    return CourseAPI.QryActiveCourseWithStudent(user_id)


@router.get('/Student/HistoryCourse/{user_id}')
async def Student_History_Course(user_id: str):
    return CourseAPI.QryHistoryCourseWithStudent(user_id)


@router.get('/Teacher/Schedule/{user_id}')
async def Teacher_Schedule(user_id: str):
    return CourseAPI.QryActiveCourseWithTeacher(user_id)


@router.get('/Teacher/HistoryCourse/{user_id}')
async def Teacher_History_Course(user_id):
    return CourseAPI.QryHistoryCourseWithTeacher(user_id)
