from fastapi import FastAPI
from routers import usuario, solicitud, cliente, agenda

app = FastAPI()

app.include_router(usuario.router)
app.include_router(solicitud.router)
app.include_router(cliente.router)
app.include_router(agenda.router)

@app.get('/')
async def hola():
    return 'hola'
