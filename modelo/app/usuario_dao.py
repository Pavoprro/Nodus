import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conexionbd import ConexionBD
import hashlib

class Usuario:
    def __init__(self):
        self.id_usuario = 0
        self.email = ""
        self.password_hash = ""
        self.nombre = ""
        self.descripcion = ""
        self.telefono = ""

class UsuarioDAO:
    def __init__(self):
        self.usuario = Usuario()
        self.conexion = ConexionBD()
    
    def registrar_usuario(self):
        """Registra un nuevo usuario"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            cursor.execute(
                "EXEC sp_RegisterUser @email = ?, @password_hash = ?, @nombre = ?, @telefono = ?",  # ← CAMBIO: minúsculas
                (self.usuario.email, self.usuario.password_hash, self.usuario.nombre, self.usuario.telefono)
            )
            
            self.conexion.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"❌ Error registrando usuario: {e}")
            return False
        finally:
            self.conexion.cerrarConexionBD()
    
    def login_usuario(self, email):
        """Obtiene datos del usuario por email para login"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            cursor.execute("EXEC sp_LoginUser @email = ?", (email,))  # ← CAMBIO: minúsculas
            result = cursor.fetchall()
            
            cursor.close()
            return result
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return None
        finally:
            self.conexion.cerrarConexionBD()
    
    def obtener_perfil(self, id_usuario):
        """Obtiene el perfil completo del usuario"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            cursor.execute("EXEC sp_GetUserProfile @id_usuario = ?", (id_usuario,))  # ← CAMBIO: minúsculas
            result = cursor.fetchall()
            
            cursor.close()
            return result
        except Exception as e:
            print(f"❌ Error obteniendo perfil: {e}")
            return None
        finally:
            self.conexion.cerrarConexionBD()
    
    def eventos_creados_usuario(self, id_usuario):
        """Obtiene eventos creados por el usuario"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            cursor.execute("EXEC sp_GetUserCreatedEvents @id_usuario = ?", (id_usuario,))  # ← CAMBIO: minúsculas
            result = cursor.fetchall()
            
            cursor.close()
            return result
        except Exception as e:
            print(f"❌ Error obteniendo eventos creados: {e}")
            return []
        finally:
            self.conexion.cerrarConexionBD()
    
    def eventos_asistiendo_usuario(self, id_usuario):
        """Obtiene eventos a los que asiste el usuario"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            cursor.execute("EXEC sp_GetUserAttendingEvents @id_usuario = ?", (id_usuario,))  # ← CAMBIO: minúsculas
            result = cursor.fetchall()
            
            cursor.close()
            return result
        except Exception as e:
            print(f"❌ Error obteniendo asistencias: {e}")
            return []
        finally:
            self.conexion.cerrarConexionBD()