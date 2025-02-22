from fastapi import APIRouter, HTTPException 
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field 
from GestorDB import GestorDB
from typing import Literal

class Cliente(BaseModel):
    id: int = Field(gt = 0)
    nombre: str 
    telefono: int
    email: EmailStr    

db = GestorDB()
router = APIRouter(prefix='/cliente')

#Ver los primeros 10 o limit clientes
@router.get('/')
async def obtener_clientes(limit: int = 10) -> list[Cliente]:
    clientes = db.ver_clientes(limit)
    if not clientes:
        return []
    return [Cliente(**cliente) for cliente in clientes]

#Agregar cliente
@router.post('/')
async def agregar_cliente(cliente:Cliente):
    try:
        db.agregar_cliente(cliente)
        return {'message': 'Cliente creado correctamente'}
    except ValueError as error:
        raise HTTPException(400,str(error))

#Ver un cliente en especifico
@router.get('/{id}')
async def obtener_cliente(id:int) -> Cliente:
    cliente = db.ver_cliente(id)
    if not cliente:
        raise HTTPException(400, 'Cliente no encontrado')
    return cliente(**cliente)

#Eliminar un cliente en especifico
@router.delete('/{id}')
async def eliminar_cliente(id:int):
    cantidad_eliminado = db.eliminar_cliente(id)
    if cantidad_eliminado == 0:
        raise HTTPException(400, 'Cliente no encontrado')
    return {'message' : 'Cliente eliminado correctamente'}
