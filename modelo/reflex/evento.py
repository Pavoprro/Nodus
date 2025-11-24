import reflex as rx

class Evento(rx.Model, table=False):
    id_evento: int = 0
    id_usuario_creador: int = 0
    id_categoria: int = 0
    titulo: str = ''
    descripcion: str = ''
    fecha: str = ''
    hora_inicio: str = ''
    hora_fin: str = ''
    lugar: str = ''
    direccion: str = ''
    cupo_maximo: int = 0
    cupos_ocupados: int = 0
    costo: str = ''
    estado: str = 'Activo'
    fecha_creacion: str = ''