import sqlite3
#from schemas import UsuarioIn, Cliente
#Da error desconocido al importar :(


class GestorDB:
    def __init__(self, path_db = 'fumiservicios.db'):
        self.path_db = path_db
        self.conexion = sqlite3.connect(path_db,check_same_thread= False)
        self.conexion.row_factory = sqlite3.Row
        self.cursor = self.conexion.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        

    def abrir_conexion(self, path_db = 'fumiservicios.db', as_dict = True):
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

    #CLIENTE

    def ver_clientes(self,limit: int):
        self.cursor.execute("SELECT * FROM CLIENTE LIMIT ?",(limit, ))
        return self.cursor.fetchall()
    
    def ver_cliente(self, id: int):
        self.cursor.execute("SELECT * FROM CLIENTE WHERE ID = ? ", (id,))
        return self.cursor.fetchone()
        
    def agregar_cliente(self, cliente):
        try:
            self.cursor.execute("INSERT INTO CLIENTE (id,nombre,telefono,email) VALUES (?,?,?,?)",(cliente.id,cliente.nombre,cliente.telefono,cliente.email))
            self.conexion.commit()
        except sqlite3.IntegrityError:
            raise ValueError("ID, email o telefono ya existen")
    
    def eliminar_cliente(self,id: int):
        self.cursor.execute("DELETE FROM CLIENTE WHERE ID = ?",(id,))
        self.conexion.commit()
        self.cursor.execute("SELECT changes()")
        return self.cursor.fetchone()[0]

    def actualizar_cliente(self, cliente):
        self.cursor.execute("UPDATE cliente SET nombre = ? , telefono = ?, email = ? WHERE id = ?", (cliente.nombre,cliente.telefono,cliente.email, cliente.id))
        self.conexion.commit()
        self.cursor.execute("SELECT changes()")
        return self.cursor.fetchone()[0]
        
    #USUARIO

    def ver_usuarios(self,limit: int):
        self.cursor.execute("SELECT * FROM USUARIO LIMIT ?",(limit, ))
        return self.cursor.fetchall()
    
    def ver_usuario(self, id: int):
        self.cursor.execute("SELECT * FROM USUARIO WHERE ID = ? ", (id,))
        return self.cursor.fetchone()

    def agregar_usuario(self,usuario):
        try:
            self.cursor.execute("INSERT INTO USUARIO (id,nombre,email,contrasena,tipo) VALUES (?,?,?,?,?)",(usuario.id,usuario.nombre,usuario.email,usuario.contrasena,usuario.tipo))
            self.conexion.commit()
        except sqlite3.IntegrityError:
            raise ValueError("ID o Email ya existen")
    
    def eliminar_usuario(self,id: int):
        self.cursor.execute("DELETE FROM USUARIO WHERE ID = ?",(id,))
        self.conexion.commit()
        self.cursor.execute("SELECT changes()")
        return self.cursor.fetchone()[0]

    def comprobar_usuario(self, id: int, contrasena: str):
        self.cursor.execute('SELECT * FROM USUARIO WHERE ID = ? AND CONTRASENA = ?' , (id, contrasena))
        return self.cursor.fetchone()
    
    def actualizar_usuario(self, usuario):
        self.cursor.execute("UPDATE usuario SET nombre = ? , email = ?, contrasena = ?, tipo = ? WHERE id = ?", (usuario.nombre,usuario.email,usuario.contrasena, usuario.tipo, usuario.id))
        self.conexion.commit()
        self.cursor.execute("SELECT changes()")
        return self.cursor.fetchone()[0]
    
    def actualizar_tipo_usuario(self, id, tipo):
        self.cursor.execute("UPDATE usuario SET tipo = ? WHERE id = ?", (tipo, id))
        self.conexion.commit()
        self.cursor.execute("SELECT changes()")
        return self.cursor.fetchone()[0]
        
    # SOLICITUD

    def ver_solicitudes(self, skip:int, limit:int):
        try:
            self.cursor.execute('''SELECT Solicitud.id, Solicitud.id_cliente, Cliente.nombre as nombre_cliente,
                                    Solicitud.id_usuario, Usuario.nombre as nombre_usuario, Solicitud.fecha, Solicitud.estado,
                                    Solicitud.descripcion, Solicitud.tipo_servicio, Solicitud.direccion FROM Solicitud
                                    LEFT JOIN Usuario ON Solicitud.id_usuario = Usuario.id
                                    LEFT JOIN Cliente ON Solicitud.id_cliente = Cliente.id
                                    LIMIT ? OFFSET ?''',(limit, skip))
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            raise error

    def ver_solicitud(self, id:int):
        try:
            self.cursor.execute('''SELECT Solicitud.id, Solicitud.id_cliente, Cliente.nombre as nombre_cliente,
                                    Solicitud.id_usuario, Usuario.nombre as nombre_usuario, Solicitud.fecha, Solicitud.estado,
                                    Solicitud.descripcion, Solicitud.tipo_servicio, Solicitud.direccion FROM Solicitud
                                    LEFT JOIN Usuario ON Solicitud.id_usuario = Usuario.id
                                    LEFT JOIN Cliente ON Solicitud.id_cliente = Cliente.id
                                    WHERE Solicitud.id = ? ''', (id,))
            return self.cursor.fetchone()
        except sqlite3.Error as error:
            raise error

    def agregar_solicitud(self,solicitud):
        try:
            self.cursor.execute('''INSERT INTO Solicitud
                                (id_cliente, id_usuario, descripcion, tipo_servicio, direccion)
                                VALUES (?,?,?,?,?)''',
                                (solicitud.id_cliente, solicitud.id_usuario, solicitud.descripcion, solicitud.tipo_servicio, solicitud.direccion))
            self.conexion.commit()
        except sqlite3.Error as error:
            raise error
        
    def agregar_usuario_solicitud(self, id, id_usuario):
        try:
            self.cursor.execute(''' UPDATE Solicitud
                                    SET id_usuario = ?
                                    WHERE id = ?''',
                                    (id_usuario, id))
            self.conexion.commit()
        except sqlite3.Error as error:
            raise error
        
    def actualizar_solicitud(self, data):
        try: 
            self.cursor.execute("""UPDATE Solicitud
                SET id_cliente = ?, id_usuario = ?, estado = ?, descripcion = ?, tipo_servicio = ?, direccion = ?
                WHERE id = ?""", (data['id_cliente'],data['id_usuario'],data['estado'],data['descripcion'],data['tipo_servicio'],data['direccion'],data['id'])
            )

            self.conexion.commit()
            
            self.cursor.execute("SELECT changes()")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as error:
            raise error

# AGENDA

    def ver_disponibilidad_empleado(self, id_usuario):
        try:
            self.cursor.execute('''SELECT * FROM Agenda
                                WHERE id_usuario = ?''', (id_usuario,))
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            raise error
        
    def ver_empleados_disponibles(self, fecha):
        try:
            self.cursor.execute('''SELECT DISTINCT Usuario.id, Usuario.nombre, Usuario.email, Usuario.tipo FROM Usuario
                                LEFT JOIN Agenda ON Usuario.id = Agenda.id_usuario
                                WHERE
                                Usuario.id NOT IN (
                                    SELECT DISTINCT Usuario.id FROM Usuario
                                    LEFT JOIN Agenda ON Usuario.id = Agenda.id_usuario
                                    WHERE
                                    Agenda.fecha = ?);''', (fecha,))
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            raise error

    def ver_TE_disponibles(self, fecha):
        try:
            self.cursor.execute('''SELECT DISTINCT Usuario.id, Usuario.nombre, Usuario.email, Usuario.tipo FROM Usuario
                                LEFT JOIN Agenda ON Usuario.id = Agenda.id_usuario
                                WHERE
                                Usuario.tipo = 'TEspecializado' AND
                                Usuario.id NOT IN (
                                    SELECT DISTINCT Usuario.id FROM Usuario
                                    LEFT JOIN Agenda ON Usuario.id = Agenda.id_usuario
                                    WHERE
                                    Agenda.fecha = ?
                                );''', (fecha,))
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            raise error
        
    def insertar_agenda(self, agenda):
        try:
            self.cursor.execute('''INSERT INTO Agenda (id_usuario, fecha, tipo_actividad) VALUES
                                (?,?,?)''', (agenda.id_usuario, agenda.fecha, agenda.tipo_actividad))
            self.conexion.commit()
            self.cursor.execute("SELECT changes()")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as error:
            raise error

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close() 