from fastapi import FastAPI
from routers import usuario, solicitud, cliente

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(usuario.router)
app.include_router(solicitud.router)
app.include_router(cliente.router)

@app.get('/')
async def hola():
    return 'hola'

origins = [
    
    'http://localhost:2999'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)