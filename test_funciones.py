# test_borrar_reserva.py
from modelo.reflex.reserva_dao import ReservaDAO

def test_borrar_reserva_12():
    print("🧪 BORRANDO RESERVA ID 12...")
    
    reserva_dao = ReservaDAO()
    
    # Cancelar la reserva ID 12 que creamos
    print("🗑️ Cancelando reserva ID 12...")
    try:
        resultado = reserva_dao.cancelar_reserva(12)
        print(f"✅ Resultado: {resultado}")
        
        # Verificar que se canceló
        print("\n🔍 Verificando estado de la reserva...")
        reservas = reserva_dao.reservas_usuario(1)
        for reserva in reservas:
            if reserva[0] == 12:  # ID de la reserva
                print(f"📊 Reserva ID {reserva[0]} - Estado: {reserva[2]}")
                break
        else:
            print("❌ No se encontró la reserva ID 12")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_borrar_reserva_12()