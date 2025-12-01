import reflex as rx

from rxconfig import config

import reflex as rx

class State(rx.State):
    # Estados para UI
    show_sidebar: bool = False
    is_logged_in: bool = False
    
    # Estados para datos
    categorias: list = []
    eventos_destacados: list = []
    usuario_actual: dict = {}
    
    # Búsqueda
    termino_busqueda: str = ""
    
    def toggle_sidebar(self):
        self.show_sidebar = not self.show_sidebar
    
    def toggle_login(self):
        self.is_logged_in = not self.is_logged_in
    
    def set_termino_busqueda(self, value: str):
        self.termino_busqueda = value
    
    def buscar_eventos(self):
        if self.termino_busqueda:
            pass

def sidebar() -> rx.Component:
    return rx.cond(
        State.show_sidebar,
        rx.box(
            rx.vstack(
                # Header del sidebar
                rx.hstack(
                    rx.heading("NODUS", size="5", color="#0E0D75"),
                    rx.button(
                        "X",
                        on_click=State.toggle_sidebar,
                        bg="transparent",
                        color="white",
                        _hover={"bg": "#333"},
                        font_size="1.5em"
                    ),
                    justify="between",
                    width="100%",
                    padding_bottom="4",
                    border_bottom="1px solid #333"
                ),
                
                # Navegación principal
                rx.box(
                    rx.vstack(
                        rx.button(
                            "Home",
                            bg="transparent",
                            justify_content="start",
                            width="100%",
                            color="white",
                            _hover={"bg": "#1A1A1A"},
                            font_size="1.1em",
                            padding_y="3"
                        ),
                        rx.button(
                            "Populares",
                            bg="transparent",
                            justify_content="start",
                            width="100%",
                            color="white",
                            _hover={"bg": "#1A1A1A"},
                            font_size="1.1em",
                            padding_y="3"
                        ),
                        rx.button(
                            "Mis Eventos",
                            bg="transparent",
                            justify_content="start",
                            width="100%",
                            color="white",
                            _hover={"bg": "#1A1A1A"},
                            font_size="1.1em",
                            padding_y="3"
                        ),
                        rx.button(
                            "Asistencias",
                            bg="transparent",
                            justify_content="start",
                            width="100%",
                            color="white",
                            _hover={"bg": "#1A1A1A"},
                            font_size="1.1em",
                            padding_y="3"
                        ),
                        spacing="1"
                    ),
                    width="100%"
                ),
                
                rx.divider(border_color="#333", margin_y="4"),
                
                # Perfil
                rx.box(
                    rx.button(
                        "Mi Perfil",
                        bg="transparent",
                        justify_content="start",
                        width="100%",
                        color="white",
                        _hover={"bg": "#1A1A1A"},
                        font_size="1.1em",
                        padding_y="3"
                    ),
                    width="100%"
                ),
                spacing="4",
                align_items="start",
                height="100vh"
            ),
            position="fixed",
            top="0",
            left="0",
            width="350px",
            height="100vh",
            bg="black",
            border_right="1px solid #333",
            z_index="1000",
            padding="6"
        )
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Espaciado izquierdo (igual al del botón hamburguesa)
            rx.box(width="40px"),
            
            # Menú hamburguesa
            rx.button(
                "☰",
                on_click=State.toggle_sidebar,
                bg="transparent",
                color="white",
                _hover={"bg": "#1A1A1A"},
                border_radius="md",
                font_size="2em",
                padding="3"
            ),
            rx.box(width="5px"),
            # Buscador
            rx.hstack(
                rx.input(
                    placeholder="Buscar eventos...",
                    bg="#1A1A1A",
                    color="white",
                    border="none",
                    _placeholder={"color": "gray.400"},
                    width="300px",
                    value=State.termino_busqueda,
                    on_change=State.set_termino_busqueda,
                    padding_y="3"
                ),
                rx.button(
                    "🔍",
                    on_click=State.buscar_eventos,
                    bg="transparent",
                    color="gray.400",
                    _hover={"color": "white"},
                    padding_x="3"
                ),
                spacing="1",
                padding_x="4",
                border="1px solid #333",
                border_radius="full",
                bg="#1A1A1A",
                height="34px"
            ),
            
            # Espaciado para centrar el logo
            rx.spacer(),
            
            # Logo
            rx.image(
                src="/logo.jpeg",
                width="200px",
                height="100px",
                border_radius="12px"
            ),
            
            # Espaciado para centrar los botones
            rx.spacer(),
            rx.box(width="45px"),
            
            # Botones de usuario
            rx.cond(
                State.is_logged_in,
                rx.hstack(
                    rx.button(
                        "Mis Eventos",
                        bg="transparent",
                        color="white",
                        _hover={"bg": "#1A1A1A"},
                        padding_x="5",
                        padding_y="3",
                        font_size="1.3em"
                    ),
                    rx.box(width="20px"),
                    rx.button(
                        "Mi Perfil",
                        bg="transparent", 
                        color="white",
                        _hover={"bg": "#1A1A1A"},
                        padding_x="5",
                        padding_y="3",
                        font_size="1.3em"
                    ),
                    spacing="4"
                ),
                rx.hstack(
                    rx.button(
                        "Iniciar Sesión",
                        bg="transparent",
                        color="white", 
                        _hover={"bg": "#1A1A1A"},
                        on_click=State.toggle_login,
                        padding_x="5",
                        padding_y="3",
                        font_size="1.3em"
                    ),
                    rx.box(width="20px"),
                    rx.button(
                        "Registrarse",
                        bg="#680596",
                        color="white",
                        _hover={"bg": "#7A0DA6"},
                        padding_x="5",
                        padding_y="3",
                        font_size="1.3em"
                    ),
                    spacing="4"
                )
            ),
            
            # Espaciado derecho (igual al izquierdo)
            rx.box(width="40px"),
            
            align="center",
            padding_y="6",
            height="120px",
            width="100%"
        ),
        bg="black",
        border_bottom="1px solid #333",
        position="sticky",
        top="0",
        z_index="999"
    )

def hero_section() -> rx.Component:
    return rx.box(
        rx.container(
            rx.center(
                rx.vstack(
                    rx.heading(
                        "Encuentra y Crea Eventos Increíbles",
                        size="7",
                        text_align="center",
                        color="white",
                        font_weight="bold",
                        margin_bottom="3"
                    ),
                    rx.text(
                        "Conecta con personas que comparten tus intereses y pasiones", 
                        size="5",
                        text_align="center",
                        color="gray.300",
                        margin_bottom="8"
                    ),
                    spacing="4",
                    align="center",
                    padding_y="20"
                )
            )
        ),
        bg="black"
    )

def categorias_ribbon() -> rx.Component:
    categorias = ["Social", "Aprendizaje", "Natural", "Deportes", "Cultural", "Gaming"]
    
    return rx.box(
        rx.container(
            rx.vstack(
                rx.text(
                    "Explorar por categorías",
                    color="gray.400",
                    font_size="md",
                    font_weight="medium",
                    margin_bottom="6"
                ),
                rx.box(
                    rx.hstack(
                        *[
                            rx.box(
                                rx.text(
                                    categoria,
                                    color="white",
                                    font_weight="medium"
                                ),
                                bg="gray.700",
                                border="2px solid gray",
                                border_radius="20px",
                                padding_x="6",
                                padding_y="4",
                                min_width="120px",
                                text_align="center"
                            )
                            for categoria in categorias
                        ],
                        spacing="4",
                        padding_y="4",
                        padding_x="6",
                        overflow_x="auto",
                        justify="center",
                        width="100%"
                    ),
                    bg="#270135",
                    border_radius="25px",
                    padding="6",
                    border="2px solid white",
                    width="100%"
                ),
                spacing="1",
                width="100%",
                align="center"
            )
        ),
        bg="black",
        border_bottom="1px solid #333",
        padding_y="8"
    )

def eventos_section() -> rx.Component:
    eventos = [
        {
            "id": 1,
            "titulo": "Noche de Jazz en Vivo",
            "fecha": "15 Dic 2024",
            "lugar": "Centro Cultural",
            "costo": "Gratis", 
            "categoria": "Cultural",
            "cupos_disponibles": 45
        },
        {
            "id": 2,
            "titulo": "Taller de Python Básico",
            "fecha": "20 Dic 2024",
            "lugar": "Tech Hub", 
            "costo": "$100",
            "categoria": "Aprendizaje",
            "cupos_disponibles": 20
        },
        {
            "id": 3, 
            "titulo": "Hiking en la Montaña",
            "fecha": "18 Dic 2024",
            "lugar": "Parque Natural",
            "costo": "Gratis",
            "categoria": "Natural",
            "cupos_disponibles": 30
        }
    ]
    
    return rx.container(
        rx.vstack(
            rx.heading(
                "Eventos Destacados",
                size="7",
                color="white",
                text_align="center",
                margin_bottom="12"
            ),
            rx.hstack(
                *[
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.badge(
                                    evento["categoria"],
                                    bg="#680596",
                                    color="white",
                                    font_size="1em"
                                ),
                                rx.spacer(),
                                rx.text(
                                    f"{evento['cupos_disponibles']} cupos",
                                    color="gray.400",
                                    font_size="sm"
                                ),
                                width="100%",
                                align="center",
                                margin_bottom="2"
                            ),
                            rx.heading(
                                evento["titulo"],
                                size="5",
                                color="white",
                                text_align="center",
                                margin_bottom="4"
                            ),
                            
                            rx.vstack(
                                rx.hstack(
                                    rx.text("📅", color="gray.400"),
                                    rx.text(evento["fecha"], color="gray.300", font_size="md"),
                                    spacing="3",
                                    justify="center"
                                ),
                                rx.hstack(
                                    rx.text("📍", color="gray.400"),
                                    rx.text(evento["lugar"], color="gray.300", font_size="md"),
                                    spacing="3",
                                    justify="center"
                                ),
                                rx.hstack(
                                    rx.text("💰", color="gray.400"),
                                    rx.text(evento["costo"], color="gray.300", font_size="md"),
                                    spacing="3",
                                    justify="center"
                                ),
                                spacing="4",
                                align_items="center",
                                width="100%",
                                margin_y="6"
                            ),
                            
                            rx.button(
                                "Ver Detalles",
                                bg="#0E0D75",
                                color="white",
                                width="100%",
                                _hover={"bg": "#1A1990"},
                                padding_y="3",
                                font_size="1.1em"
                            ),
                            spacing="4",
                            align="center",
                            height="100%",
                            padding="6"
                        ),
                        bg="#111",
                        border="1px solid #333",
                        border_radius="lg",
                        height="100%",
                        min_width="350px",
                        flex="1"
                    )
                    for evento in eventos
                ],
                spacing="8",
                justify="center",
                width="100%"
            ),
            spacing="8",
            align="center",
            width="100%"
        ),
        padding_y="16",
        bg="black",
        width="100%"
    )

def footer() -> rx.Component:
    return rx.box(
        rx.container(
            rx.hstack(
                rx.vstack(
                    rx.heading("NODUS", size="4", color="#0E0D75"),
                    rx.text("Conectando personas a través de eventos", color="gray.400"),
                    align_items="start",
                    spacing="2"
                ),
                rx.spacer(),
                rx.hstack(
                    rx.vstack(
                        rx.text("Enlaces", color="white", font_weight="bold"),
                        rx.link("Inicio", color="gray.400", _hover={"color": "white"}),
                        rx.link("Eventos", color="gray.400", _hover={"color": "white"}),
                        rx.link("Categorías", color="gray.400", _hover={"color": "white"}),
                        spacing="1",
                        align_items="start"
                    ),
                    rx.vstack(
                        rx.text("Legal", color="white", font_weight="bold"),
                        rx.link("Términos", color="gray.400", _hover={"color": "white"}),
                        rx.link("Privacidad", color="gray.400", _hover={"color": "white"}),
                        spacing="1",
                        align_items="start"
                    ),
                    spacing="6"
                ),
                align_items="start"
            ),
            padding_y="6"
        ),
        bg="black",
        border_top="1px solid #333"
    )

def index() -> rx.Component:
    return rx.box(
        sidebar(),
        navbar(),
        hero_section(),
        categorias_ribbon(),
        eventos_section(),
        footer(),
        bg="black",
        min_height="100vh",
        color="white"
    )

app = rx.App()
app.add_page(index)