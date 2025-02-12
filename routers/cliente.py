from fastapi import APIRouter, HTTPException
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
