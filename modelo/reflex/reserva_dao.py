from modelo.conexionbd import ConexionBD
from modelo.reflex.reserva import Reserva

class ReservaDAO:
    def __init__(self):
        self.bd = ConexionBD()
        self.reserva = Reserva()
    
    def crear_reserva(self, id_usuario, id_evento, cantidad_personas=1):
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            
            # 1. Verificar cupos disponibles
            cursor.execute("""
                SELECT cupo_maximo, ISNULL(cupos_ocupados, 0) 
                FROM Eventos 
                WHERE id_evento = ?
            """, [id_evento])
            
            evento = cursor.fetchone()
            if not evento:
                return (-1, 'Evento no encontrado')
                
            cupo_maximo, cupos_ocupados = evento
            cupos_disponibles = cupo_maximo - cupos_ocupados
            
            if cupos_disponibles < cantidad_personas:
                return (-1, 'No hay cupos disponibles')
            
            # 2. Crear reserva
            cursor.execute("""
                INSERT INTO Reservas (id_usuario, id_evento, cantidad_personas, estado)
                OUTPUT INSERTED.id_reserva
                VALUES (?, ?, ?, 'Activa')
            """, (id_usuario, id_evento, cantidad_personas))
            
            id_reserva = cursor.fetchone()[0]
            
            # 3. Actualizar cupos
            cursor.execute("""
                UPDATE Eventos 
                SET cupos_ocupados = ISNULL(cupos_ocupados, 0) + ?
                WHERE id_evento = ?
            """, (cantidad_personas, id_evento))
            
            # 4. Crear notificación
            cursor.execute("""
                INSERT INTO Notificaciones (id_usuario, tipo, titulo, mensaje, id_evento_relacionado)
                VALUES (?, 'registrado', 'Reserva confirmada', 'Tu reserva para el evento ha sido confirmada', ?)
            """, (id_usuario, id_evento))
            
            self.bd.conexion.commit()
            self.bd.cerrarConexionBD()
            
            return (id_reserva, 'Success')
            
        except Exception as e:
            print(f"❌ Error creando reserva: {e}")
            if self.bd.conexion:
                self.bd.conexion.rollback()
                self.bd.cerrarConexionBD()
            return (-1, f'Error: {str(e)}')
    
    def cancelar_reserva(self, id_reserva):
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            
            # 1. Obtener datos de la reserva
            cursor.execute("""
                SELECT id_evento, cantidad_personas, id_usuario 
                FROM Reservas 
                WHERE id_reserva = ? AND estado = 'Activa'
            """, [id_reserva])
            
            reserva = cursor.fetchone()
            if not reserva:
                return 'Reserva no encontrada o ya cancelada'
                
            id_evento, cantidad_personas, id_usuario = reserva
            
            # 2. Cancelar reserva
            cursor.execute("""
                UPDATE Reservas 
                SET estado = 'Cancelada'
                WHERE id_reserva = ?
            """, [id_reserva])
            
            # 3. Liberar cupos
            cursor.execute("""
                UPDATE Eventos 
                SET cupos_ocupados = cupos_ocupados - ?
                WHERE id_evento = ?
            """, (cantidad_personas, id_evento))
            
            # 4. Crear notificación
            cursor.execute("""
                INSERT INTO Notificaciones (id_usuario, tipo, titulo, mensaje, id_evento_relacionado)
                VALUES (?, 'cancelado', 'Reserva cancelada', 'Tu reserva ha sido cancelada', ?)
            """, (id_usuario, id_evento))
            
            self.bd.conexion.commit()
            self.bd.cerrarConexionBD()
            
            return 'Success'
            
        except Exception as e:
            print(f"❌ Error cancelando reserva: {e}")
            if self.bd.conexion:
                self.bd.conexion.rollback()
                self.bd.cerrarConexionBD()
            return f'Error: {str(e)}'
    
    def reservas_usuario(self, id_usuario):
        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()
        sp = "EXEC sp_GetUserReservations @id_usuario = ?"
        param = [id_usuario]
        cursor.execute(sp, param)
        filas = cursor.fetchall()
        self.bd.cerrarConexionBD()
        return filas