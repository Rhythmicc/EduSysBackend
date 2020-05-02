from Server import Info
from Server import Options
from Server import Users
from fastapi import FastAPI

server = FastAPI()
server.title = 'EduSysBackendAPI'
server.include_router(Info.router, tags=['info'])
server.include_router(Options.router, tags=['options'])
server.include_router(Users.router, tags=['user'])
