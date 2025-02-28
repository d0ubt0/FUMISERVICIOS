from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field 
from GestorDB import GestorDB
from typing import Literal
from time import sleep
from schemas import UsuarioIn, UsuarioOut

db = GestorDB()
router = APIRouter(prefix='/usuario')

#Ver los primeros 10 o limit usuarios
@router.get('/')
async def obtener_usuarios(limit: int = 10) -> list[UsuarioOut]:
    usuarios = db.ver_usuarios(limit)
    if not usuarios:
        return []
    return [UsuarioOut(**usuario) for usuario in usuarios]

#Agregar usuario
@router.post('/')
async def agregar_usuario(usuario:UsuarioIn):
    try:
        db.agregar_usuario(usuario)
        return {'message': 'Usuario creado correctamente'}
    except ValueError as error:
        raise HTTPException(400,str(error))

#Ver un usuario en especifico
@router.get('/{id}')
async def obtener_usuario(id:int) -> UsuarioOut:
    usuario = db.ver_usuario(id)
    if not usuario:
        raise HTTPException(404, 'Usuario no encontrado')
    return UsuarioOut(**usuario)

#Eliminar un usuario en especifico
@router.delete('/{id}')
async def eliminar_usuario(id:int):
    cantidad_eliminado = db.eliminar_usuario(id)
    if cantidad_eliminado == 0:
        raise HTTPException(404, 'Usuario no encontrado')
    return {'message' : 'Usuario eliminado correctamente'}

#Actualizar un usuario en especifico
@router.put('/')
async def actualizar_usuario(usuario: UsuarioIn):
    cantidad_actualizado = db.actualizar_usuario(usuario)
    if cantidad_actualizado == 0:
        raise HTTPException(404, 'Usuario no encontrado')
    return {'message' : 'Usuario actualizado correctamente'}
    
    


