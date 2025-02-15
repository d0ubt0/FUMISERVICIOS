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
    
    def ver_clientes(self,limit: int):
        self.cursor.execute("SELECT * FROM CLIENTE LIMIT ?",(limit, ))
        return self.cursor.fetchall()
    
    def ver_usuario(self, id: int):
        self.cursor.execute("SELECT * FROM USUARIO WHERE ID = ? ", (id,))
        return self.cursor.fetchone()
    
    def ver_cliente(self, id: int):
        self.cursor.execute("SELECT * FROM CLIENTE WHERE ID = ? ", (id,))
        return self.cursor.fetchone()

    def agregar_usuario(self,usuario):
        try:
            self.cursor.execute("INSERT INTO USUARIO (id,nombre,email,contrasena,tipo) VALUES (?,?,?,?,?)",(usuario.id,usuario.nombre,usuario.email,usuario.contrasena,usuario.tipo))
            self.conexion.commit()
        except sqlite3.IntegrityError:
            raise ValueError("ID o Email ya existen")
        
    def agregar_cliente(self, cliente):
        try:
            self.cursor.execute("INSERT INTO CLIENTE (id,nombre,telefono,email) VALUES (?,?,?,?)",(cliente.id,cliente.nombre,cliente.telefono,cliente.email))
            self.conexion.commit()
        except sqlite3.IntegrityError:
            raise ValueError("ID, email o telefono ya existen")
        
    def eliminar_usuario(self,id: int):
        self.cursor.execute("DELETE FROM USUARIO WHERE ID = ?",(id,))
        self.conexion.commit()
        self.cursor.execute("SELECT changes()")
        return self.cursor.fetchone()[0]
    
    def eliminar_cliente(self,id: int):
        self.cursor.execute("DELETE FROM CLIENTE WHERE ID = ?",(id,))
        self.conexion.commit()
        self.cursor.execute("SELECT changes()")
        return self.cursor.fetchone()[0]
        

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close() 

