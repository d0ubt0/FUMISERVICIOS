from fastapi import APIRouter
from GestorDB import GestorDB
from fastapi import HTTPException
from schemas import Solicitud, SolicitudIn, SolicitudOut, UsuarioOut
import sqlite3

router = APIRouter(prefix='/solicitud')
db = GestorDB()

# ver historial de solicitudes
@router.get('/')
async def solicitud(skip:int = 0, limit:int = 10) -> list[SolicitudOut]:
    try:
        solicitudes = db.ver_solicitudes(skip, limit)
        return [SolicitudOut(**dict(solicitud)) for solicitud in solicitudes]
    except Exception as error:
        raise HTTPException(400,str(error))

# añadir solicitud
@router.post('/')
async def solicitud(solicitud:SolicitudIn):
    try:
        db.agregar_solicitud(solicitud)
        return {'message': 'Solicitud creada correctamente'}
    except Exception as error:
        raise HTTPException(400,str(error))

# buscar solicitud
@router.get('/{id}')
async def solicitud(id:int) -> SolicitudOut:
    try:
        solicitud = db.ver_solicitud(id)
        if not solicitud:
            raise HTTPException(400,"Usuario no Encontrado")
        return SolicitudOut(**solicitud)
    except Exception as error:
        raise HTTPException(400,str(error))

# añadir id_usuario a solicitud
@router.put('/usuario/')
async def solicitud(id:int, id_usuario:int = None):
    try:
        usuario = db.ver_usuario(id_usuario)

        if not usuario:
            raise HTTPException(404,'Usuario no encontrado')
        
        usuario = UsuarioOut(**usuario)

        if usuario.tipo != 'TEspecializado':
            raise HTTPException(401, 'Usuario debe ser tecnico especializado')

        db.agregar_usuario_solicitud(id, id_usuario)
        return {'message' : f'Usuario {id_usuario} agregado correctamente a la solicitud con id = {id}'}
    except Exception as error:
        raise HTTPException(400,str(error))
    
# Cambiar solicitud completa
@router.put('/')
async def solicitud(data: dict):
    cantidad_actualizado = db.actualizar_solicitud(data)

    if cantidad_actualizado == 0:
        raise HTTPException(404, 'Solicitud no encontrada')
    
    return {'message' : 'Solicitud actualizada correctamente'}

    