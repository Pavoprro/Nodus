import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conexionbd import ConexionBD

class Evento:
    def __init__(self):
        self.id_evento = 0
        self.id_usuario_creador = 0
        self.id_categoria = 0
        self.titulo = ""
        self.descripcion = ""
        self.fecha = ""
        self.hora_inicio = ""
        self.hora_fin = ""
        self.lugar = ""
        self.direccion = ""
        self.cupo_maximo = 0
        self.costo = ""

class EventoDAO:
    def __init__(self):
        self.evento = Evento()
        self.conexion = ConexionBD()
    
    def crear_evento(self):
        """Crea un nuevo evento"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            cursor.execute(
                """EXEC sp_CreateEvent 
                @id_usuario_creador = ?, @id_categoria = ?, @titulo = ?, @descripcion = ?,
                @fecha = ?, @hora_inicio = ?, @hora_fin = ?, @lugar = ?, @direccion = ?,
                @cupo_maximo = ?, @costo = ?""",
                (self.evento.id_usuario_creador, self.evento.id_categoria, self.evento.titulo,
                 self.evento.descripcion, self.evento.fecha, self.evento.hora_inicio,
                 self.evento.hora_fin, self.evento.lugar, self.evento.direccion,
                 self.evento.cupo_maximo, self.evento.costo)
            )
            
            self.conexion.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"❌ Error creando evento: {e}")
            return False
        finally:
            self.conexion.cerrarConexionBD()
    
    def eliminar_evento(self, id_evento):
        """Elimina un evento y todas sus reservas asociadas"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            # Primero eliminar las reservas asociadas
            cursor.execute("DELETE FROM Reservas WHERE id_evento = ?", (id_evento,))
            
            # Luego eliminar el evento
            cursor.execute("DELETE FROM Eventos WHERE id_evento = ?", (id_evento,))
            
            self.conexion.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"❌ Error eliminando evento: {e}")
            return False
        finally:
            self.conexion.cerrarConexionBD()
    
    def eventos_recomendados(self):
        """Obtiene los eventos recomendados (TOP 6)"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            cursor.execute("EXEC sp_GetRecommendedEvents")
            result = cursor.fetchall()
            
            cursor.close()
            return result
        except Exception as e:
            print(f"❌ Error obteniendo eventos recomendados: {e}")
            return []
        finally:
            self.conexion.cerrarConexionBD()
    
    def todos_los_eventos(self):
        """Obtiene TODOS los eventos activos sin límite"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            cursor.execute("EXEC sp_GetAllEvents")
            result = cursor.fetchall()
            
            cursor.close()
            return result
        except Exception as e:
            print(f"❌ Error obteniendo todos los eventos: {e}")
            return []
        finally:
            self.conexion.cerrarConexionBD()