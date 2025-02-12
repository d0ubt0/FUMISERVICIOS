from fastapi import APIRouter
from pydantic import BaseModel, Field
from GestorDB import GestorDB
from typing import Literal


router = APIRouter()
db = GestorDB()

# modificar solicitudes
# buscar solicitudes

class Solicitud(BaseModel):
    id : int = 0
    id_cliente : int = Field(gt = 0)
    id_usuario : int = Field(gt = 0)
    fecha : str = ""
    estado : str = Literal['Aceptado', 'En Espera', 'Rechazado']
    descripcion : str
    tipo_servicio : str 
    direccion : str

# ver historial de solicitudes
@router.get('/solicitudes/')
async def solicitudes(skip:int = 0, limit:int = 10):

    db.abrir_conexion(as_dict=True)

    # query
    db.cursor.execute("SELECT * FROM Solicitud LIMIT ? OFFSET ?",(limit, skip))
    solicitudes = db.cursor.fetchall()

    db.cerrar_conexion()

    return solicitudes

# añadir solicitudes
@router.post('/solicitud/')
async def solicitud(solicitud:Solicitud):

    print(solicitud)
    db.abrir_conexion()
    db.cursor.execute('''INSERT INTO Solicitud (id_cliente, id_usuario, estado, descripcion, tipo_servicio, direccion) VALUES
                      (?,?,?,?,?,?)''', ())
    db.conexion.commit()
    db.cerrar_conexion()

    return solicitud
