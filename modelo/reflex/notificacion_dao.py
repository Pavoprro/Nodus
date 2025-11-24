from modelo.conexionbd import ConexionBD
from modelo.reflex.notificacion import Notificacion

class NotificacionDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.notificacion = Notificacion()
    
    def crear_notificacion(self, id_usuario, tipo, titulo, mensaje, id_evento_relacionado=None):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_CreateNotification @id_usuario = ?, @tipo = ?, @titulo = ?, @mensaje = ?, @id_evento_relacionado = ?"
        param = (id_usuario, tipo, titulo, mensaje, id_evento_relacionado)
        cursor.execute(sp, param)
        self.bd.conexion.commit()
        print("✅ Notificación creada correctamente")
        self.bd.cerrarConexionBD()
    
    def notificaciones_usuario(self, id_usuario):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetUserNotifications @id_usuario = ?"
        param = [id_usuario]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def eliminar_notificacion(self, id_notificacion):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_DeleteNotification @id_notificacion = ?"
        param = [id_notificacion]
        cursor.execute(sp, param)
        self.bd.conexion.commit()
        print("✅ Notificación eliminada correctamente")
        self.bd.cerrarConexionBD()