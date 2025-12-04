import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conexionbd import ConexionBD

class ReservaDAO:
    def __init__(self):
        self.conexion = ConexionBD()
    
    def crear_reserva(self, id_usuario, id_evento, cantidad_personas=1):
        """Crea una reserva para un evento"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            # Primero verificar cupos disponibles
            cursor.execute("""
                SELECT cupo_maximo - cupos_ocupados AS disponibles
                FROM Eventos
                WHERE id_evento = ?
            """, (id_evento,))
            
            disponibles = cursor.fetchone()
            if not disponibles or disponibles[0] < cantidad_personas:
                cursor.close()
                return [('Error', 'No hay cupos disponibles')]
            
            # Crear la reserva con estado 'Activa' para que coincida con el SP
            cursor.execute("""
                INSERT INTO Reservas (id_usuario, id_evento, cantidad_personas, estado, fecha_reserva)
                VALUES (?, ?, ?, 'Activa', GETDATE())
            """, (id_usuario, id_evento, cantidad_personas))
            
            # Actualizar cupos ocupados
            cursor.execute("""
                UPDATE Eventos
                SET cupos_ocupados = cupos_ocupados + ?
                WHERE id_evento = ?
            """, (cantidad_personas, id_evento))
            
            self.conexion.conexion.commit()
            cursor.close()
            return [('Success', 'Success')]
        except Exception as e:
            print(f"❌ Error creando reserva: {e}")
            return [('Error', str(e))]
        finally:
            self.conexion.cerrarConexionBD()
    
    # En reserva_dao.py
    def cancelar_reserva(self, id_reserva):
        """Cancela una reserva existente"""
        try:
            self.conexion.establecerConexionBD()
            cursor = self.conexion.conexion.cursor()
            
            # LLAMADA CORRECTA al stored procedure
            cursor.execute("EXEC sp_CancelReservation @id_reserva = ?", (id_reserva,))
            
            result = cursor.fetchone()
            
            self.conexion.conexion.commit()
            cursor.close()
            
            # El stored procedure devuelve dos columnas: resultado y mensaje
            # Solo necesitamos el resultado ('Success' o 'Error')
            return result[0] if result else 'Error'
            
        except Exception as e:
            print(f"❌ Error cancelando reserva: {e}")
            return 'Error'
        finally:
            self.conexion.cerrarConexionBD()