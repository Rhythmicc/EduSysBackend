from ORM.Course import CourseAPI
from . import SelectCourseInfo
from fastapi import APIRouter

router = APIRouter()


@router.get('/Student/Schedule/{user_id}')
async def Student_Schedule(user_id: str):
    return CourseAPI.QryScheduleWithStudent(user_id)


@router.get('/Student/HistoryCourse/{user_id}')
async def Student_History_Course(user_id: str):
    return CourseAPI.QryHistoryCourseWithStudent(user_id)


@router.get('/Teacher/Schedule/{user_id}')
async def Teacher_Schedule(user_id: str):
    return CourseAPI.QryScheduleWithTeacher(user_id)


@router.get('/Teacher/HistoryCourse/{user_id}')
async def Teacher_History_Course(user_id):
    return CourseAPI.QryHistoryCourseWithTeacher(user_id)


@router.get('/Student/Courses/{user_id}')
async def Student_Active_Courses(user_id: str):
    return CourseAPI.QryActiveCourseWithStudent(user_id)


@router.get('/Teacher/Courses/{user_id}')
async def Student_Active_Courses(user_id: str):
    return CourseAPI.QryActiveCourseWithTeacher(user_id)


@router.post('/UploadGrade')
async def Upload_Grade(dt: list):
    ret = {'status': True}
    for info in dt:
        ret = CourseAPI.AddCourseScore(info['user_id'], info['course_id'], info['score'])
    return ret


@router.get('/Teacher/AllCourseIdName/{user_id}')
async def Teacher_All_CourseId_Name(user_id: str):
    return CourseAPI.QryAllCourseIdName(user_id)


@router.get('/GetStudentsByCourseId/{course_id}')
async def Get_Students_By_CourseId(course_id: int):
    return CourseAPI.QryStudentsByCourseId(course_id)


@router.get('/GetGradesByStudent/{user_id}')
async def Get_Grades_By_Student(user_id: str):
    return CourseAPI.QryGradesByStudent(user_id)


@router.get('/SelectableCourse')
async def Selectable_Course():
    return CourseAPI.QrySelectableCourse()


@router.post('/SelectCourse')
async def Select_Course(dt: SelectCourseInfo):
    res = {}
    for i in dt.course_ls:
        ret = CourseAPI.SelectCourse(dt.user_id, i)
        res[i] = ret['status']
    return res
