from ORM.Activity import ActivityAPI
from fastapi import APIRouter

router = APIRouter()


@router.get('/AddActivity/{activity}')
async def Add_Activity(activity: str):
    return ActivityAPI.AddActivity(activity)


@router.get('/DelActivity/{activity}')
async def Del_Activity(activity: str):
    return ActivityAPI.DelActivity(activity)


@router.get('/EnableActivity/{activity}')
async def Enable_Activity(activity: str):
    return ActivityAPI.EnableActivity(activity)


@router.get('/DisableActivity/{activity}')
async def Disable_Activity(activity: str):
    return ActivityAPI.DisableActivity(activity)


@router.get('/QryActivity/{activity}')
async def Query_Activity(activity: str):
    return ActivityAPI.QryActivity(activity)
