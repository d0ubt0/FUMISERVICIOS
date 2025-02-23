from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field 
from GestorDB import GestorDB
from typing import Literal
from time import sleep
from schemas import UsuarioLogin, UsuarioOut


db = GestorDB()
router = APIRouter(prefix='/login')

@router.post('/')
def iniciar_sesion(usuario: UsuarioLogin) -> UsuarioOut:
    usuario = db.comprobar_usuario(usuario.id, usuario.contrasena)
    if not usuario:
        raise HTTPException(404, 'Usuario no encontrado')
    else:
        return UsuarioOut(**usuario)