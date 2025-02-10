from fastapi import APIRouter ,HTTPException
import sqlite3
from pydantic import BaseModel

class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    contrasena: str
    tipo: str

class GestorDB:
    def __init__(self, path_db = 'fumiservicios.db'):
        self.path_db = path_db
        self.conexion = sqlite3.connect(path_db)
        self.cursor = self.conexion.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def ver_usuarios(self,limit: int):
        self.cursor.execute("SELECT * FROM USUARIO LIMIT ?",(limit, ))
        return self.cursor.fetchall()

    def agregar_usuario(self,usuario: Usuario):
        try:
            self.cursor.execute("INSERT INTO USUARIO (id,nombre,email,contrasena,tipo) VALUES (?,?,?,?,?)",(usuario.id,usuario.nombre,usuario.email,usuario.contrasena,usuario.tipo))
            self.conexion.commit()
        except sqlite3.IntegrityError:
            raise ValueError("ID o Email ya existen")

        
db = GestorDB()
router = APIRouter()

#Ver los primeros 10 o limit usuarios
@router.get('/usuarios')
async def users(limit: int = 10):
    usuarios = db.ver_usuarios(limit)
    usuarios_json = [Usuario(id = usuario[0],nombre = usuario[1],email = usuario[2], contrasena = usuario[3],tipo = usuario[4]) for usuario in usuarios]
    return usuarios_json


#Agregar usuario
@router.post('/usuario')
async def users(user:Usuario):
    try:
        db.agregar_usuario(user)
        return {'message': 'Usuario creado correctamente'}
    except ValueError as error:
        raise HTTPException(400,str(error))


#Ver un usuario en especifico
@router.get('/usuario/{id}')
async def users(id:int):
    db.cursor.execute("SELECT * FROM USUARIO WHERE ID = ? ", (id,))
    usuario = db.cursor.fetchone()
    if not usuario:
        raise HTTPException(400, 'Usuario no encontrado')

    return Usuario(id = usuario[0],nombre = usuario[1],email = usuario[2], contrasena = usuario[3],tipo = usuario[4])

    


