from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field 
from GestorDB import GestorDB
from typing import Literal


class Usuario(BaseModel):
    id: int = Field(gt = 0)
    nombre: str 
    email: EmailStr
    contrasena: str = Field(min_length=8,max_length=25)
    tipo: Literal["CTecnico","TEspecializado" ,"ACliente" ,"EqTecnico"]    

db = GestorDB()
router = APIRouter(prefix='/usuario')

#Ver los primeros 10 o limit usuarios
@router.get('/')
async def obtener_usuarios(limit: int = 10) -> list[Usuario]:
    usuarios = db.ver_usuarios(limit)
    if not usuarios:
        return []
    return [Usuario(**usuario) for usuario in usuarios]

#Agregar usuario
@router.post('/')
async def agregar_usuario(usuario:Usuario):
    try:
        db.agregar_usuario(usuario)
        return {'message': 'Usuario creado correctamente'}
    except ValueError as error:
        raise HTTPException(400,str(error))

#Ver un usuario en especifico
@router.get('/{id}')
async def obtener_usuario(id:int) -> Usuario:
    usuario = db.ver_usuario(id)
    if not usuario:
        raise HTTPException(400, 'Usuario no encontrado')
    return Usuario(**usuario)

#Eliminar un usuario en especifico
@router.delete('/{id}')
async def eliminar_usuario(id:int):
    cantidad_eliminado = db.eliminar_usuario(id)
    if cantidad_eliminado == 0:
        raise HTTPException(400, 'Usuario no encontrado')
    return {'message' : 'Usuario eliminado correctamente'}
    
    


