from modelo.conexionbd import ConexionBD
from modelo.reflex.categoria import Categoria

class CategoriaDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.categoria = Categoria()
    
    def listar_categorias(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetAllCategories"
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def eventos_por_categoria(self, id_categoria):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetEventsByCategory @id_categoria = ?"
        param = [id_categoria]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def categorias_populares(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetMostPopularCategories"
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas