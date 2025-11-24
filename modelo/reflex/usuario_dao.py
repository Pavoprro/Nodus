from modelo.conexionbd import ConexionBD
from modelo.reflex.usuario import Usuario

class UsuarioDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.usuario = Usuario()
    
    def registrar_usuario(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_RegisterUser @email = ?, @password_hash = ?, @nombre = ?, @telefono = ?"
        param = (self.usuario.email, self.usuario.password_hash, self.usuario.nombre, self.usuario.telefono)
        cursor.execute(sp, param)
        self.bd.conexion.commit()
        print("✅ Usuario registrado correctamente")
        self.bd.cerrarConexionBD()
    
    def login_usuario(self, email):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_LoginUser @email = ?"
        param = [email]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def actualizar_perfil(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_UpdateUserProfile @id_usuario = ?, @nombre = ?, @descripcion = ?, @telefono = ?"
        param = (self.usuario.id_usuario, self.usuario.nombre, self.usuario.descripcion, self.usuario.telefono)
        cursor.execute(sp, param)
        self.bd.conexion.commit()
        print("✅ Perfil actualizado correctamente")
        self.bd.cerrarConexionBD()
    
    def eventos_creados_usuario(self, id_usuario):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetUserCreatedEvents @id_usuario = ?"
        param = [id_usuario]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def eventos_asistiendo_usuario(self, id_usuario):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetUserAttendingEvents @id_usuario = ?"
        param = [id_usuario]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def obtener_perfil(self, id_usuario):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetUserProfile @id_usuario = ?"
        param = [id_usuario]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas