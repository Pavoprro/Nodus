import reflex as rx

class Reserva(rx.Model, table=False):
    id_reserva: int = 0
    id_usuario: int = 0
    id_evento: int = 0
    cantidad_personas: int = 1
    estado: str = 'Activa'
    fecha_reserva: str = ''