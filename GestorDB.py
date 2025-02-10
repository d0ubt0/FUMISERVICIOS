import sqlite3

class GestorDB:
    def __init__(self):
        self.conexion = None
        self.cursor = None

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

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close() 