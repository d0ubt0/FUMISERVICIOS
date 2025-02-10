from fastapi import APIRouter
from pydantic import BaseModel
from GestorDB import GestorDB

router = APIRouter()
db = GestorDB()

# añadir solicitudes
# modificar solicitudes
# buscar solicitudes

class Solicitud(BaseModel):
    id : int
    id_cliente : int
    id_usuario : int
    fecha : str
    estado : str
    descripcion : str
    tipo_servicio : str
    direccion : str

# ver historial de solicitudes
# FALTA AÑADIR EXCEPTIONS
@router.get('/solicitudes/')
async def solicitudes(limit:int = 10):

    db.abrir_conexion(as_dict=True)

    # query
    db.cursor.execute("SELECT * FROM Solicitud LIMIT ?",(limit,))
    query_result = db.cursor.fetchall()

    # formateo para json
    solicitudes = list(map( lambda solicitud : Solicitud(**dict(solicitud)), query_result))
    
    db.cerrar_conexion()

    return solicitudes