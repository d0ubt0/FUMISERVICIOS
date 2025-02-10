import sqlite3
import time

class GestorDB:
    def __init__(self, path_db = 'fumiservicios.db'):
        self.path_db = path_db
        self.conexion = sqlite3.connect(path_db)
        self.conexion.row_factory = sqlite3.Row
        self.cursor = self.conexion.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        

    def abrir_conexion(self, path_db = 'fumiservicios.db', as_dict = False):
        """Abre conexion con la base de datos usando sqlite3

        Args:
            path_db (str, optional): Ruta de la base de datos. Defaults to 'fumiservicios.db'.
            as_dict (bool, optional): Si es True retorna las filas en formato de un diccionario. Defaults to False.
        """
        self.conexion = sqlite3.connect(path_db)

        # Si es True retorna cada fila como un diccionario
        if as_dict == True:
            self.conexion.row_factory = sqlite3.Row

        self.cursor = self.conexion.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
    
    def ver_usuarios(self,limit: int):
        self.cursor.execute("SELECT * FROM USUARIO LIMIT ?",(limit, ))
        return self.cursor.fetchall()
    
    def ver_usuario(self, id: int):
        self.cursor.execute("SELECT * FROM USUARIO WHERE ID = ? ", (id,))
        return self.cursor.fetchone()

    def agregar_usuario(self,usuario):
        try:
            with sqlite3.connect(self.path_db) as conexion:
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO USUARIO (id,nombre,email,contrasena,tipo) VALUES (?,?,?,?,?)",(usuario.id,usuario.nombre,usuario.email,usuario.contrasena,usuario.tipo))
                time.sleep(20)
                conexion.commit()
        except sqlite3.IntegrityError:
            raise ValueError("ID o Email ya existen")

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close() 