from Database.Options import OptionAPI
from fastapi import APIRouter
from . import DayForm

router = APIRouter()


@router.get('/d7f6g78d678g6d78g6d')
async def QuitService():
    from Database import CloseDatabase
    CloseDatabase()
    exit(0)


@router.post('/SetStartDay')
async def Set_Start_Day(dt: DayForm):
    return {'status': OptionAPI.setStartDay(dt.year, dt.semester, dt.start_day)}


@router.post('/AddStartDay')
async def Add_Start_Day(dt: DayForm):
    return {'status': OptionAPI.AddStartDay(dt.year, dt.semester, dt.start_day)}
