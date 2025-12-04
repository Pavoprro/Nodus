from modelo.conexionbd import ConexionBD
from modelo.reflex.evento import Evento

class EventoDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.evento = Evento()
    
    def crear_evento(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_CreateEvent @id_usuario_creador = ?, @id_categoria = ?, @titulo = ?, @descripcion = ?, @fecha = ?, @hora_inicio = ?, @hora_fin = ?, @lugar = ?, @direccion = ?, @cupo_maximo = ?, @costo = ?"
        param = (self.evento.id_usuario_creador, self.evento.id_categoria, self.evento.titulo, self.evento.descripcion, 
                self.evento.fecha, self.evento.hora_inicio, self.evento.hora_fin, self.evento.lugar, 
                self.evento.direccion, self.evento.cupo_maximo, self.evento.costo)
        cursor.execute(sp, param)
        self.bd.conexion.commit()
        print("✅ Evento creado correctamente")
        self.bd.cerrarConexionBD()
    
    def cancelar_evento(self, id_evento):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_CancelEvent @id_evento = ?"
        param = [id_evento]
        cursor.execute(sp, param)
        self.bd.conexion.commit()
        print("✅ Evento cancelado correctamente")
        self.bd.cerrarConexionBD()
    
    def obtener_detalles_evento(self, id_evento):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetEventDetails @id_evento = ?"
        param = [id_evento]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def obtener_asistentes_evento(self, id_evento):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetEventAttendees @id_evento = ?"
        param = [id_evento]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def verificar_registro_usuario(self, id_usuario, id_evento):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_CheckUserEventRegistration @id_usuario = ?, @id_evento = ?"
        param = (id_usuario, id_evento)
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def eventos_recomendados(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetRecommendedEvents"
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas
    
    def eliminar_evento(self, id_evento):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_DeleteEvent @id_evento = ?"
        param = [id_evento]
        cursor.execute(sp, param)
        self.bd.conexion.commit()
        print("✅ Evento eliminado correctamente")
        self.bd.cerrarConexionBD()

    def actualizar_evento(self):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_UpdateEvent @id_evento = ?, @id_categoria = ?, @titulo = ?, @descripcion = ?, @fecha = ?, @hora_inicio = ?, @hora_fin = ?, @lugar = ?, @direccion = ?, @cupo_maximo = ?, @costo = ?"
        param = (self.evento.id_evento, self.evento.id_categoria, self.evento.titulo, self.evento.descripcion,
                self.evento.fecha, self.evento.hora_inicio, self.evento.hora_fin, self.evento.lugar,
                self.evento.direccion, self.evento.cupo_maximo, self.evento.costo)
        cursor.execute(sp, param)
        self.bd.conexion.commit()
        print("✅ Evento actualizado correctamente")
        self.bd.cerrarConexionBD()

    def todos_los_eventos(self):
        """Obtiene TODOS los eventos activos sin límite"""
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetAllEvents"
        cursor.execute(sp)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas