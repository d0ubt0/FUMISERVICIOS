from fastapi import APIRouter, HTTPException
from GestorDB import GestorDB
from schemas import AgendaIn, AgendaOut, UsuarioOut
from datetime import datetime

# QUE SE VEA REFLEJADO TECNICO ESPECIALIZADO EN AGENDA

db = GestorDB()
router = APIRouter(prefix='/agenda')

# fechas ocupadas de un usuario
@router.get('/usuario/{id}')
async def agenda(id: int) -> list[AgendaOut]:
    try:
        dias = db.ver_disponibilidad_empleado(id)
        return [AgendaOut(**dia) for dia in dias]
    except Exception as error:
        raise HTTPException(400, error)
    
# usuarios libres en una fecha
@router.get('/fecha/{fecha}')
async def agenda(fecha: str):
    try:
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    except:
        raise HTTPException(400, 'Ingrese una fecha valida en formato yyyy-mm-dd')
    try:
        print("xd")
        usuarios_disponibles = db.ver_TE_disponibles(fecha)
        if not usuarios_disponibles:
            raise HTTPException(400, "No hay usuarios disponibles")
        return [UsuarioOut(**usuario) for usuario in usuarios_disponibles]
    except Exception as error:
        raise HTTPException(400, str(error))

# asignar tecnico especializado 
@router.post('/')
async def agenda(registro: AgendaIn):
    try:
        id_usuario = registro.id_usuario
        usuario = UsuarioOut(**db.ver_usuario(id_usuario))
        if usuario.tipo != 'TEspecializado':
            raise HTTPException(400, 'El usuario agregado debe ser Tecnico Especializado')
        print(registro)
        db.insertar_agenda(registro)
        return {'message': 'Asignado correctamente'}

    except Exception as error:
            raise HTTPException(400, str(error))
