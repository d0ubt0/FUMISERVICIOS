from fastapi import APIRouter
from pydantic import BaseModel, Field, EmailStr
from GestorDB import GestorDB
from typing import Literal, Optional
from datetime import date

tipo_usuario_restriccion = Literal["CTecnico","TEspecializado" ,"ACliente" ,"EqTecnico"] 
contrasena_restriccion = Field(min_length=8,max_length=25)


class AgendaIn(BaseModel):
    id_usuario : int = Field(gt = 0)
    fecha : date
    tipo_actividad : Literal['diagnostico', 'servicio']

class AgendaOut(BaseModel):
    id : int = Field(gt = 0)
    id_usuario : int = Field(gt = 0)
    fecha : date
    tipo_actividad : Literal['diagnostico', 'servicio']

class Cliente(BaseModel):
    id: int = Field(gt = 0)
    nombre: str 
    telefono: int
    email: EmailStr

# se mantiene por compatibilidad momentanea
class Solicitud(BaseModel):
    id : Optional[int] = None
    id_cliente : int = Field(gt = 0)
    id_usuario : int = Field(gt = 0)
    fecha : Optional[str] = None
    estado : Literal['Aceptado', 'En Espera', 'Rechazado'] = 'En Espera'
    descripcion : str
    tipo_servicio : str 
    direccion : str

class SolicitudIn(BaseModel):
    id_cliente : int = Field(gt = 0)
    id_usuario : Optional[int] = None
    descripcion : str
    tipo_servicio : str 
    direccion : str

class SolicitudOut(BaseModel):
    id : int = Field(gt = 0)
    id_cliente : int = Field(gt = 0)
    nombre_cliente : str
    id_usuario : Optional[int] 
    nombre_usuario : Optional[str]
    fecha : str
    estado : Literal['Aceptado', 'En Espera', 'Rechazado']
    descripcion : str
    tipo_servicio : str 
    direccion : str

class UsuarioIn(BaseModel):
    id: int = Field(gt = 0)
    nombre: str 
    email: EmailStr
    contrasena: str = contrasena_restriccion
    tipo: tipo_usuario_restriccion  

class UsuarioOut(BaseModel):
    id: int = Field(gt = 0)
    nombre: str 
    email: EmailStr
    tipo: tipo_usuario_restriccion 

class UsuarioLogin(BaseModel):
    id: int = Field(gt = 0)
    contrasena: str = contrasena_restriccion