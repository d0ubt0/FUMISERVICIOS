from fastapi import FastAPI
from routers import users
from routers import solicitud

app = FastAPI()

app.include_router(users.router)
app.include_router(solicitud.router)

@app.get('/')
async def hola():
    return 'hola'
