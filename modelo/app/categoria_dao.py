import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conexionbd import ConexionBD

class CategoriaDAO:
    def __init__(self):
        self.conexion = ConexionBD()
    
    def listar_categorias(self):
        """Lista todas las categorías disponibles"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            cursor.execute("SELECT id_categoria, nombre, descripcion FROM Categorias")
            result = cursor.fetchall()
            
            cursor.close()
            return result
        except Exception as e:
            print(f"❌ Error listando categorías: {e}")
            return []
        finally:
            self.conexion.cerrarConexionBD()