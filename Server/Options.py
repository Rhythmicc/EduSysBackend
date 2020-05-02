from fastapi import APIRouter

router = APIRouter()


@router.get('/d7f6g78d678g6d78g6d', tags=['options'])
async def QuitService():
    from Database import CloseDatabase
    CloseDatabase()
    exit(0)
