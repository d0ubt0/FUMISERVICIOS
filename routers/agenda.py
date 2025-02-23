from fastapi import APIRouter
from pydantic import BaseModel, Field
from GestorDB import GestorDB
from typing import Literal
from datetime import date
from schemas import Agenda
    
db = GestorDB()
router = APIRouter(prefix='/agenda')