from fastapi import APIRouter ,HTTPException
from pydantic import BaseModel
from GestorDB import GestorDB


class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    contrasena: str
    tipo: str

db = GestorDB()
router = APIRouter()

#Ver los primeros 10 o limit usuarios
@router.get('/usuarios')
async def obtener_usuarios(limit: int = 10):
    usuarios = db.ver_usuarios(limit)
    if not usuarios:
        return {'message': 'No hay usuarios'}
    return usuarios


#Agregar usuario
@router.post('/usuario')
async def agregar_usuario(usuario:Usuario):
    try:
        db.agregar_usuario(usuario)
        return {'message': 'Usuario creado correctamente'}
    except ValueError as error:
        raise HTTPException(400,str(error))


#Ver un usuario en especifico
@router.get('/usuario/{id}')
async def obtener_usuario(id:int):
    usuario = db.ver_usuario(id)
    if not usuario:
        raise HTTPException(400, 'Usuario no encontrado')
    return usuario
    


