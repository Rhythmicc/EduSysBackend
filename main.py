from Server import Info
from Server import Options
from Server import Users
from Server import Course
from Server import Activity
from fastapi import FastAPI

server = FastAPI()
server.title = 'EduSysBackendAPI'
server.include_router(Info.router, prefix='/info', tags=['info'])
server.include_router(Options.router, tags=['options'])
server.include_router(Users.router, tags=['user'])
server.include_router(Course.router, prefix='/course', tags=['course'])
server.include_router(Activity.router, prefix='/activity', tags=['activity'])
