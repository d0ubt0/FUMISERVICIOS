import os
import sqlite3
import re
from Usuario import Usuario

class Solicitud:
    def __init__(self,  id_cliente=None, id_usuario=None, descripcion=None,  tipo_servicio=None, direccion=None,):
        self._id_cliente = id_cliente
        self._descripcion = descripcion
        self._id_usuario = id_usuario
        self._tipo_servicio = tipo_servicio
        self._direccion = direccion
        
    @property
    def id_cliente(self):
        return self._id_cliente
        
    @property
    def id_usuario(self):
        return self._id_usuario
    
    @property
    def descripcion(self):
        return self._descripcion
         
    @property
    def tipo_servicio(self):
        return self._tipo_servicio
    
    @property
    def direccion(self):
        return self._direccion
      
    def agregar_solicitud(self):
        db.agregar_solicitud(self.id_cliente, self.id_usuario, self.descripcion,self.tipo_servicio,self.direccion)


class GestorDB:
    def __init__(self, path_db = 'fumiServicios.db'):
        self.path_db = path_db
        self.conexion = sqlite3.connect(path_db)
        self.cursor = self.conexion.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
    

    def verificar_contrasena(self, id:int, contrasena:str):
        """Busca el usuario por id y contraseña.

        Args:
            id (int): id del empleado a buscar
            contrasena (str): contrasena del id

        Returns:
            list[any]: Retorna los datos del usuario
            o
            null: Retorna null si no encuentra nada en la base de datos
        """ 

        self.cursor.execute('SELECT * FROM Usuario WHERE id = ? AND contrasena = ?', (id, contrasena))
        return self.cursor.fetchone()

    def agregar_solicitud(self, id_cliente:int, id_usuario:int, descripcion:str, tipo_servicio:str, direccion:str):
        try: 
            self.cursor.execute("INSERT INTO Solicitud (id_cliente, id_usuario, descripcion, tipo_servicio, direccion) VALUES (?, ?, ?, ?,?)",
                                (id_cliente, id_usuario, descripcion, tipo_servicio, direccion))
            self.conexion.commit()
        except sqlite3.IntegrityError:
            print("\nEl cliente o Usuario no existen! \n")
        else:
            print("\nSolicitud agregada\n")

    def ver_solicitudes(self):
        self.cursor.execute('SELECT * FROM Solicitud')
        return self.cursor.fetchall()

      
    def leer_usuario(self, id:int):
        self.cursor.execute("SELECT * FROM Usuario WHERE id= ? " , (id,))
        return(self.cursor.fetchone())

    def agenda_empleado(self, id:int) -> list[any]:
        """Funcion dedicada a cumplir la HU4, permitiendo ver la disponibilidad de un empleado.

        Args:
            id (int): id del empleado a buscar

        Returns:
            list[any]: Retorna una lista con el usuario y los dias en los que está ocupado
        """        
        self.cursor.execute("""SELECT Usuario.id, Usuario.nombre, Agenda.fecha as fecha_ocupada, Usuario.tipo FROM Usuario
                            LEFT JOIN Agenda
                            ON Usuario.id = Agenda.id_usuario
                            WHERE Usuario.id = ? AND
                            fecha_ocupada > date('now');""",(id,))

        return(self.cursor.fetchall())
    
    def agenda_fecha(self, fecha:str) -> list[any]:
        """Funcion dedicada a cumplir la HU4, permitiendo ver los empleados disponibles en un horario.

        Args:
            fecha (str): fecha por filtrar

        Returns:
            list[any]: Retorna una lista con los usuarios disponibles en una fecha
        """
        self.cursor.execute(f"""SELECT Usuario.id, Usuario.nombre, Agenda.fecha AS fecha_ocupada, Usuario.tipo 
                                    FROM Usuario
                                    LEFT JOIN Agenda
                                    ON Usuario.id = Agenda.id_usuario
                                    WHERE (fecha_ocupada <> ? OR fecha_ocupada IS NULL) 
                                    AND Usuario.tipo IN ('TEspecializado', 'EqTecnico');""", 
                                    (fecha,))

        return(self.cursor.fetchall())
    
    def ingresar_usuario(self,id,nombre,email,contrasena,tipo): 
        try:
            sql="INSERT INTO Usuario VALUES (?,?,?,?,?)"
            valores=(id,nombre,email,contrasena,tipo)
            self.cursor.execute(sql,valores)
            self.conexion.commit()
        except sqlite3.Error as error:
            print(f"Error!!!{error}")

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()     

##
##
##
##

#Historia de Usuario 1
def iniciar_sesion():
    # Bucle infinito hasta que dé un nombre y contraseña válidos
    while True:
        print("Inserte los datos para iniciar sesión: ")
        id = input("ID del Usuario: ").strip()
        contrasena = input("Contraseña del Usuario: ").strip()

        if len(id) == 0 or len(contrasena) == 0:
            os.system("cls")
            print("Inserta id o contraseñas validos")
            continue

        consulta_usuario = db.verificar_contrasena(id, contrasena)
        os.system("cls")
        if consulta_usuario:
            print('Inicio de sesión correcto')
            return {'id': consulta_usuario[0], 'nombre': consulta_usuario[1], 'correo': consulta_usuario[2], 'tipo': consulta_usuario[4]}
        else:
            print('Nombre de Usuario o contraseña incorrecta')

#Historia de Usuario 2
def registro_usuario(db:GestorDB):
    def idFun():
        while True:
            id =input("Ingresa la cedula: ").strip()
            if len(id)==0:
                print("No puedes dejar esto vacio")
                continue
            elif not(id.isdigit()):
                print("Debe ser un numero")
                continue
            return id
    
    def nombreFun():
        while True:
            nombre=input("Ingresa tu nombre: ").strip()
            if len(nombre)==0:
                print("No puedes dejar esto vacio")
                continue
            return nombre
  
    def emailFun():
        while True:
            email=input("Ingresa tu email: ").strip()
            if len(email)==0:
                print("No puedes dejar esto vacio")
                continue
            return email

    def contraFun():
        while True:
            contra=input("Ingresa tu contraseña: ").strip()
            if len(contra)<8:
                print("La contraseña debe tener por lo menos 8 caracteres")
                continue
            return contra
    
    def TipoFun():
        while True:
            tipo=input("Ingresa tu tipo de empleado (CTecnico, TEspecializado, ACliente, EqTecnico): ").strip()
            if tipo in ('CTecnico', 'TEspecializado', 'ACliente', 'EqTecnico'):
                return tipo
            else:
                print("Rol no valido")
        

    id = idFun()
    nombre = nombreFun() 
    contrasena = contraFun()     
    tipo = TipoFun()
    email= emailFun()

    db.ingresar_usuario(id,nombre,email,contrasena,tipo)

#Historia de Usuario 3     
def crear_solicitud():
        os.system('cls')
        preguntas = {
        "id_cliente": "Ingrese el id del cliente: ",
        "id_usuario":"Ingrese su id: ",
        "descripcion":"Ingrese la descripciÃ³n del problema: ",
        "servicio":"Ingrese el tipo de servicio: ",
        "direccion":"Ingrese la direccion del cliente: ",
            }
        datos = []
        for clave, mensaje in preguntas.items():
            while True:
                try:
                    entrada = input(mensaje)
                    if clave == "id_cliente" or clave == "id_usuario":
                        datos.append(int(entrada))
                        break
                    else:
                        if not entrada.strip():
                            print("No puedes dejar datos sin rellenar!")
                        else:
                            datos.append(entrada)
                            break
                except:
                    print("Por favor agregue los datos de forma correcta!")
        solicitud = Solicitud(datos[0], datos[1], datos[2], datos[3], datos[4])
        solicitud.agregar_solicitud()

#Historia de Usuario 4
def ver_agenda_empleado():
    id = int(input("Ingrese el id del Empleado: "))
    try:
        print("Fechas no disponibles:")
        dias_ocupados = db.agenda_empleado(id)
        for dia in dias_ocupados:
            print(dia[2])
    except ValueError:
        print("Por favor ingrese un id válido")

def ver_agenda_fecha():
    while True:
        fecha = input("Ingrese una fecha para ver los empleados disponibles (yyyy-mm-dd): ")
        regex_fecha = r'\b(20[0-9]{2}|19[0-9]{2})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\b'
        if re.match(regex_fecha,fecha):
            break
        else:
            print("Formato de fecha invalida")
    try:
        print(f"Empleados disponibles:\n")
        empleados = db.agenda_fecha(fecha)
        for empleado in empleados:
            print(f"id: {empleado[0]}, Nombre: {empleado[1]}, Rol: {empleado[3]}")
    except ValueError:
        print("Por favor ingrese una fecha válida")

#5 Historia de Usuario

def menu():
    os.system('cls')
    usuario_sesion = iniciar_sesion()

    print(f"\nBienvenido {usuario_sesion['nombre']}\n")
    tipo = usuario_sesion["tipo"]

    
    if tipo == 'CTecnico':
        CTecnico()         
    elif tipo == 'TEspecializado':
        pass
    elif tipo == 'ACliente':
        pass
    elif tipo == 'EqTecnico':
        pass

def AtencionCliente():
    while True:
        opcion = int(input("""¿Vas a crear una solicitud?
        Seleciona una opcion del menu
        1.Generar solicitud 
        2.Salir
        Opcion: """))
        if opcion == 1:
            crear_solicitud()

        elif opcion == 2:
            print("¡Hasta luego!")
            break

def CTecnico():
    while True:
        print("¿Con que vas a trabajar hoy?")
        opcion = int(input("""Seleciona una opcion del menu
        1.Registrar empleados
        2.Ver disponibilidad de Tecnico Especializados
        3.Asignar tecnico especializado
        4.Salir 
        Opcion: """))
        if opcion == 1:
            registro_usuario(db)

        elif opcion == 2:
            ver_agenda_fecha()

        elif opcion == 3:
            pass
            
        else:
            print("¡Hasta luego!")
            break

# Crear una instancia de la base de datos
db = GestorDB()

menu()
#ver_agenda_empleado()
# Iniciar sesión con un usuario

#menu()

#print(db.agenda_empleado(1))

# Cerrar la conexión a la base de datos
#db.cerrar_conexion()

# Agregar usuarios
# db.agregar_usuario('Jhofred', 'jhofred@gmail.com', 'jhofred123', 'EqTecnico')
# db.agregar_usuario('papisam', 'papisam@gmail.com', 'papisam123', 'CTecnico')\

        
        
#screar_solicitud()