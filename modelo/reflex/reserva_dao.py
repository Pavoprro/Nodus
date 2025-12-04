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
                return [(-1, 'Evento no encontrado')]  # ← CAMBIO
                
            cupo_maximo, cupos_ocupados = evento
            cupos_disponibles = cupo_maximo - cupos_ocupados
            
            if cupos_disponibles < cantidad_personas:
                return [(-1, 'No hay cupos disponibles')]  # ← CAMBIO
            
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
            
            return [(id_reserva, 'Success')]  # ← CAMBIO
            
        except Exception as e:
            print(f"❌ Error creando reserva: {e}")
            if self.bd.conexion:
                self.bd.conexion.rollback()
                self.bd.cerrarConexionBD()
            return [(-1, f'Error: {str(e)}')]  # ← CAMBIO
    
    def cancelar_reserva(self, id_reserva):
        """Cancela una reserva usando el SP"""
        try:
            self.bd.establecerConexionBD()
            cursor = self.bd.conexion.cursor()
            
            # Ejecutar el SP
            cursor.execute("EXEC sp_CancelReservation @id_reserva = ?", [id_reserva])
            
            # Obtener el resultado
            result = cursor.fetchone()
            
            self.bd.conexion.commit()
            self.bd.cerrarConexionBD()
            
            if result and result[0] == 'Success':
                print(f"✅ Reserva {id_reserva} cancelada correctamente")
                return 'Success'
            else:
                mensaje = result[1] if result else 'Error desconocido'
                print(f"❌ Error cancelando reserva: {mensaje}")
                return mensaje
                
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