import reflex as rx

class Usuario(rx.Model, table=False):
    id_usuario: int = 0
    email: str = ''
    password_hash: str = ''
    nombre: str = ''
    descripcion: str = ''
    telefono: str = ''
    fecha_registro: str = ''