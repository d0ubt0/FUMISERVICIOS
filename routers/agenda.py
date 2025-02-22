from fastapi import APIRouter
from pydantic import BaseModel, Field
from GestorDB import GestorDB
from typing import Literal
from datetime import date

class Agenda(BaseModel):
    id : int = Field(gt = 0)
    id_usuario : int = Field(gt = 0)
    fecha : date
    tipo_actividad : str = Literal['Diagnostico', 'Servicio']
    
db = GestorDB()
router = APIRouter(prefix='/agenda')