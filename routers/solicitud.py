from fastapi import APIRouter
from pydantic import BaseModel, Field
from GestorDB import GestorDB
from typing import Literal, Optional
from fastapi import HTTPException
from schemas import Solicitud
import sqlite3

router = APIRouter(prefix='/solicitud')
db = GestorDB()

# ver historial de solicitudes
@router.get('/')
async def solicitud(skip:int = 0, limit:int = 10):

    try:
        db.abrir_conexion()

        # query
        db.cursor.execute("SELECT * FROM Solicitud LIMIT ? OFFSET ?",(limit, skip))
        solicitudes = db.cursor.fetchall()

        db.cerrar_conexion()
        return solicitudes

    except sqlite3.Error as error:
        raise HTTPException(400,f'sqlite error: {str(error)}')   

    except Exception as error:
        raise HTTPException(400,str(error))
    
    finally:
        db.cerrar_conexion()



# añadir solicitud
@router.post('/')
async def solicitud(solicitud:Solicitud):
    try:
        db.abrir_conexion()
        db.cursor.execute('''INSERT INTO Solicitud
                          (id_cliente, id_usuario, estado, descripcion, tipo_servicio, direccion)
                          VALUES (?,?,?,?,?,?)''',
                          (solicitud.id_cliente, solicitud.id_usuario, solicitud.estado, solicitud.descripcion, solicitud.tipo_servicio, solicitud.direccion))
        db.conexion.commit()
        return {'message': 'Solicitud creada correctamente'}

    except sqlite3.Error as error:
        raise HTTPException(400,f'sqlite error: {str(error)}')   

    except Exception as error:
        raise HTTPException(400,str(error))
    
    finally:
        db.cerrar_conexion()



# buscar solicitud
@router.get('/{id}')
async def solicitud(id:int):
    try:
        db.abrir_conexion()
        solicitud = db.conexion.execute('''SELECT * FROM solicitud WHERE id = ?''', (id,)).fetchone()
        if not solicitud:
            raise HTTPException(400,"Usuario no Encontrado")
        return solicitud
    
    except sqlite3.Error as error:
        raise HTTPException(400,f'sqlite error: {str(error)}')   

    except Exception as error:
        raise HTTPException(400,str(error))
    
    finally:
        db.cerrar_conexion()



# añadir id_usuario a solicitud
@router.put('/{id}')
async def solicitud(id:int, id_usuario:int = None):
    try:
        db.abrir_conexion()
        db.conexion.execute(''' UPDATE Solicitud
                                SET id_usuario = ?
                                WHERE id = ?''',
                                (id_usuario, id)).fetchone()
        db.conexion.commit()
        return {'message' : f'Usuario agregado correctamente a la solicitud con id = {id}'}

    except sqlite3.Error as error:
        raise HTTPException(400,f'sqlite error: {str(error)}')   

    except Exception as error:
        raise HTTPException(400,str(error))
    
    finally:
        db.cerrar_conexion()