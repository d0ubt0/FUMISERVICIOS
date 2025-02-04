class Usuario():
    
    def __init__(self, id, nombre, email, contrasena, tipo):
        """Clase destinada a representar todo empleado de fumiservicios con los atributos obtenidos de la base de datos.

        Args:
            id (int): id
            nombre (str): nombre
            email (str): email
            contrasena (str): contrasena
            tipo (str): tipo
        """
        self._id = id
        self._nombre = nombre
        self._email = email 
        self._contrasena = contrasena
        self._tipo = tipo

    def get_id(self) -> int:
        return self._id
    
    def get_nombre(self) -> str:
        return self._nombre

    def get_email(self) -> str:
        return self._email
    
    def get_contrasena(self) -> str:
        return self._contrasena

    def get_tipo(self) -> str:
        return self._tipo
