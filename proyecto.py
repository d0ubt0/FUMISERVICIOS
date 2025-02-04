import sqlite3
from Usuario import Usuario

class GestorDB:
    def __init__(self, path_db = 'fumiServicios.db'):
        self.path_db = path_db
        self.conexion = sqlite3.connect(path_db)
        self.cursor = self.conexion.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def crear_tabla(self, nombre_tabla: str, parametros: str):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({parametros})")
        self.conexion.commit()

    def verificar_contrasena(self, id, contrasena):
        self.cursor.execute('SELECT * FROM usuario WHERE id = ? AND contrasena = ?', (id, contrasena))
        return self.cursor.fetchone()

    def agregar_solicitud(self, id_cliente, id_usuario, descripcion, tipo_servicio, direccion):

        self.cursor.execute("INSERT INTO Solicitud (id_cliente, id_usuario, descripcion, tipo_servicio, direccion) VALUES (?, ?, ?, ?,?)",
                            (id_cliente, id_usuario, descripcion, tipo_servicio, direccion))
        self.conexion.commit()

    def leer_usuario(self, id):

        self.cursor.execute(f"SELECT * FROM Usuario WHERE id={id}")
        return(self.cursor.fetchone())

    def agenda_empleado(self, id) -> list[any]:
        """Funcion dedicada a cumplir la HU4, permitiendo ver la disponibilidad de un empleado.

        Args:
            id (int): id del empleado a buscar

        Returns:
            list[any]: Retorna una lista con el usuario y los dias en los que está ocupado
        """        
        self.cursor.execute(f"""SELECT Usuario.id, Usuario.nombre, Agenda.fecha as fecha_ocupada FROM Usuario
                            LEFT JOIN Agenda
                            ON Usuario.id = Agenda.id_usuario
                            WHERE Usuario.id = {id} AND
                            fecha_ocupada > date('now');""")

        return(self.cursor.fetchall())
    
    def empleado_disponible(self, id, fecha) -> bool:
        raise(NotImplementedError)  

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()        

def iniciar_sesion():
    # Bucle infinito hasta que dé un nombre y contraseña válidos
    while True:
        print("Inserte los datos para iniciar sesión: ")
        nombre = input("Nombre de Usuario: ").strip()
        contrasena = input("Contraseña del Usuario: ").strip()

        consulta_usuario = db.verificar_contrasena(nombre, contrasena)

        if consulta_usuario:
            print('Inicio de sesión correcto')
            return {'id': consulta_usuario[0], 'nombre': consulta_usuario[1], 'correo': consulta_usuario[2], 'tipo': consulta_usuario[4]}
        else:
            print('Nombre de Usuario o contraseña incorrecta')


def menu():

    rol = usuario_sesion[0]
    while True:
        if rol == 'CTecnico':
            pass
        elif rol == 'TEspecializado':
            pass
        elif rol == 'ACliente':
            pass
        elif rol == 'EqTecnico':
            pass

# Crear una instancia de la base de datos
db = GestorDB()

db.agregar_solicitud(1,1,12123,21312,2131)

# Agregar usuarios
# db.agregar_usuario('Jhofred', 'jhofred@gmail.com', 'jhofred123', 'EqTecnico')
# db.agregar_usuario('papisam', 'papisam@gmail.com', 'papisam123', 'CTecnico')

# Iniciar sesión con un usuario
usuario_sesion = iniciar_sesion()

print(db.agenda_empleado(1))

# Cerrar la conexión a la base de datos
db.cerrar_conexion()
