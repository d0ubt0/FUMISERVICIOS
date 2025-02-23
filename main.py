from fastapi import FastAPI
from routers import usuario, solicitud, cliente, agenda, login


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(usuario.router)
app.include_router(solicitud.router)
app.include_router(cliente.router)
app.include_router(agenda.router)
app.include_router(login.router)

@app.get('/')
async def hola():
    return 'hola'

origins = [
    
    'http://localhost:2999',
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002'
    'http://localhost:3003',
    'http://localhost:3004'

]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)