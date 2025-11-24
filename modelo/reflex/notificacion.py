import reflex as rx

class Notificacion(rx.Model, table=False):
    id_notificacion: int = 0
    id_usuario: int = 0
    tipo: str = ''
    titulo: str = ''
    mensaje: str = ''
    fecha_envio: str = ''
    id_evento_relacionado: int = 0