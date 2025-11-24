import reflex as rx

class Categoria(rx.Model, table=False):
    id_categoria: int = 0
    nombre: str = ''
    descripcion: str = ''