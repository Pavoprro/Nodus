import reflex as rx
from rxconfig import config

# Importar los DAOs
from modelo.reflex.categoria_dao import CategoriaDAO
from modelo.reflex.evento_dao import EventoDAO
from modelo.reflex.usuario_dao import UsuarioDAO
from modelo.reflex.reserva_dao import ReservaDAO

class State(rx.State):
    # Estados para UI
    show_sidebar: bool = False
    is_logged_in: bool = False
    current_page: str = "home"
    show_crear_evento_modal: bool = False
    show_login_modal: bool = False
    show_registro_modal: bool = False
    
    # Estados para datos
    categorias: list[dict] = []
    eventos: list[tuple] = []
    eventos_filtrados: list[tuple] = []
    mis_eventos: list[tuple] = []
    mis_asistencias: list[tuple] = []
    categorias_seleccionadas: list[int] = []
    
    # Usuario actual
    id_usuario_logueado: int = 0  # ← ESTO FALTABA
    usuario_nombre: str = ""
    usuario_email: str = ""
    usuario_telefono: str = ""
    usuario_descripcion: str = ""
    
    # Filtros
    termino_busqueda: str = ""
    
    # Form crear evento
    nuevo_evento_titulo: str = ""
    nuevo_evento_descripcion: str = ""
    nuevo_evento_categoria: int = 0
    nuevo_evento_categoria_nombre: str = "Seleccionar..."
    nuevo_evento_fecha: str = ""
    nuevo_evento_hora_inicio: str = ""
    nuevo_evento_hora_fin: str = ""
    nuevo_evento_lugar: str = ""
    nuevo_evento_direccion: str = ""
    nuevo_evento_cupo_maximo: int = 0
    nuevo_evento_costo: str = ""
    
    # Login/Registro
    login_email: str = ""
    login_password: str = ""
    registro_nombre: str = ""
    registro_email: str = ""
    registro_password: str = ""
    registro_telefono: str = ""
    mensaje_error: str = ""

    # Notificaciones toast
    show_toast: bool = False
    toast_message: str = ""
    toast_type: str = "success"

    # Modal confirmar eliminar evento
    show_confirmar_eliminar: bool = False
    evento_a_eliminar: int = 0
    
       # Modal editar evento
    show_editar_evento_modal: bool = False
    evento_editando: int = 0
    editar_evento_titulo: str = ""
    editar_evento_descripcion: str = ""
    editar_evento_categoria: int = 0
    editar_evento_categoria_nombre: str = ""
    editar_evento_fecha: str = ""
    editar_evento_hora_inicio: str = ""
    editar_evento_hora_fin: str = ""
    editar_evento_lugar: str = ""
    editar_evento_direccion: str = ""
    editar_evento_cupo_maximo: int = 0
    editar_evento_costo: str = ""
    
    # Modal editar perfil
    show_editar_perfil_modal: bool = False
    editar_perfil_nombre: str = ""
    editar_perfil_descripcion: str = ""
    editar_perfil_telefono: str = ""

    # Modal ver detalles evento
    show_detalles_evento_modal: bool = False
    evento_detalle: tuple = ()

    categorias_seleccionadas: list[int] = []  # Lista de IDs seleccionados

    def cargar_todos_eventos(self):
        """Carga TODOS los eventos para la página de eventos"""
        try:
            dao = EventoDAO()
            result = dao.todos_los_eventos()
            
            # Convertir a lista de tuplas simples
            eventos_convertidos = []
            for evento in result:
                evento_tuple = tuple(
                    str(item) if not isinstance(item, (int, float, str, type(None))) else item 
                    for item in evento
                )
                eventos_convertidos.append(evento_tuple)
            
            self.eventos = eventos_convertidos
            self.eventos_filtrados = eventos_convertidos
        except Exception as e:
            print(f"❌ Error cargando todos los eventos: {e}")
    
    def seleccionar_categoria(self, cat_id: int):
        if cat_id in self.categorias_seleccionadas:
            self.categorias_seleccionadas.remove(cat_id)
        else:
            self.categorias_seleccionadas.append(cat_id)

    def cancelar_asistencia(self, id_reserva: int):
        """Cancela la asistencia del usuario a un evento"""
        try:
            if not self.is_logged_in:
                self.mostrar_notificacion("Debes iniciar sesión", "error")
                return
            
            dao = ReservaDAO()
            result = dao.cancelar_reserva(id_reserva)
            
            if result == 'Success':
                self.mostrar_notificacion("Asistencia cancelada correctamente", "success")
                # Recargar las asistencias para actualizar la vista
                self.cargar_mis_asistencias()
                # También recargar eventos por si afecta cupos
                self.cargar_eventos()
            else:
                self.mostrar_notificacion(f"Error: {result}", "error")
                
        except Exception as e:
            print(f"❌ Error cancelando asistencia: {e}")
            self.mostrar_notificacion("Error al cancelar asistencia", "error")

    def abrir_modal_detalles_evento(self, evento: tuple):
        """Abre el modal con los detalles completos del evento"""
        self.evento_detalle = evento
        self.show_detalles_evento_modal = True

    def cerrar_modal_detalles_evento(self):
        """Cierra el modal de detalles"""
        self.show_detalles_evento_modal = False
        self.evento_detalle = ()

    def registrar_asistencia(self, id_evento: int, cantidad_personas: int = 1):
        """Registra la asistencia del usuario al evento"""
        try:
            if not self.is_logged_in:
                self.mostrar_notificacion("Debes iniciar sesión para registrarte", "error")
                return
            
            dao = ReservaDAO()
            result = dao.crear_reserva(self.id_usuario_logueado, id_evento, cantidad_personas)
            
            if result and len(result) > 0 and result[0][1] == 'Success':
                self.mostrar_notificacion("¡Registro exitoso! 🎉", "success")
                self.cerrar_modal_detalles_evento()
                self.cargar_mis_asistencias()
                self.cargar_eventos()  # Actualizar cupos
            else:
                mensaje_error = result[0][1] if result and len(result) > 0 else "No hay cupos disponibles"
                self.mostrar_notificacion(f"{mensaje_error}", "error")
        except Exception as e:
            print(f"Error registrando asistencia: {e}")
            self.mostrar_notificacion("Error al registrar asistencia", "error")

    def cerrar_modal_editar_evento(self):
        self.show_editar_evento_modal = False

    def ir_a_perfil(self):
        if not self.is_logged_in:
            self.mostrar_notificacion("Debes iniciar sesión primero", "error")  # ← SIN yield
            return
        
        self.set_page("perfil")
        self.cargar_perfil_usuario()
        self.cargar_mis_eventos()
        self.cargar_mis_asistencias()
    

    def confirmar_eliminar_evento(self, id_evento: int):
        """Muestra el modal de confirmación para eliminar"""
        self.evento_a_eliminar = id_evento
        self.show_confirmar_eliminar = True

    def cancelar_eliminar_evento(self):
        """Cancela la eliminación"""
        self.show_confirmar_eliminar = False
        self.evento_a_eliminar = 0

    def eliminar_evento(self):
        try:
            dao = EventoDAO()
            dao.eliminar_evento(self.evento_a_eliminar)
            
            self.show_confirmar_eliminar = False
            self.evento_a_eliminar = 0
            self.cargar_mis_eventos()
            self.cargar_eventos()
            self.mostrar_notificacion("Evento eliminado correctamente", "success")  # ← SIN yield
        except Exception as e:
            print(f"Error eliminando evento: {e}")
            self.mostrar_notificacion("Error al eliminar evento", "error")

    def abrir_modal_editar_evento(self, evento: tuple):
        """Abre el modal de editar con los datos del evento"""
        self.evento_editando = evento[0]
        self.editar_evento_titulo = str(evento[1])
        self.editar_evento_descripcion = str(evento[11])
        self.editar_evento_fecha = str(evento[3])
        self.editar_evento_hora_inicio = str(evento[4])[:5]  # Solo HH:MM
        self.editar_evento_hora_fin = str(evento[5])[:5] if evento[5] else ""
        self.editar_evento_lugar = str(evento[6])
        self.editar_evento_direccion = str(evento[7])
        self.editar_evento_cupo_maximo = int(evento[8])
        self.editar_evento_costo = str(evento[10])
        self.editar_evento_categoria_nombre = str(evento[12])
        self.editar_evento_categoria = int(evento[13])
        
        self.show_editar_evento_modal = True
        if not self.categorias:
            self.cargar_categorias()

    def actualizar_evento(self):
        try:
            from datetime import datetime
            
            dao = EventoDAO()
            dao.evento.id_evento = self.evento_editando
            dao.evento.id_categoria = self.editar_evento_categoria
            dao.evento.titulo = self.editar_evento_titulo
            dao.evento.descripcion = self.editar_evento_descripcion
            
            if "/" in self.editar_evento_fecha:
                fecha_obj = datetime.strptime(self.editar_evento_fecha, "%m/%d/%Y")
                dao.evento.fecha = fecha_obj.strftime("%Y-%m-%d")
            else:
                dao.evento.fecha = self.editar_evento_fecha
            
            dao.evento.hora_inicio = self.editar_evento_hora_inicio + ":00" if len(self.editar_evento_hora_inicio) == 5 else self.editar_evento_hora_inicio
            dao.evento.hora_fin = self.editar_evento_hora_fin + ":00" if self.editar_evento_hora_fin and len(self.editar_evento_hora_fin) == 5 else self.editar_evento_hora_fin
            dao.evento.lugar = self.editar_evento_lugar
            dao.evento.direccion = self.editar_evento_direccion
            dao.evento.cupo_maximo = self.editar_evento_cupo_maximo
            dao.evento.costo = self.editar_evento_costo
            
            dao.actualizar_evento()
            
            self.show_editar_evento_modal = False
            self.cargar_mis_eventos()
            self.cargar_eventos()
            self.mostrar_notificacion("Evento actualizado correctamente", "success")  # ← SIN yield
        except Exception as e:
            print(f"Error actualizando evento: {e}")
            self.mostrar_notificacion("Error al actualizar evento", "error") 
    
    def seleccionar_categoria(self, id_categoria: int):
        """Función que recibe solo el ID sin el evento del mouse"""
        self.toggle_categoria_filter(id_categoria)

    # Setters para editar evento
    def set_editar_evento_titulo(self, value: str):
        self.editar_evento_titulo = value

    def set_editar_evento_descripcion(self, value: str):
        self.editar_evento_descripcion = value

    def set_editar_evento_categoria(self, value: int):
        self.editar_evento_categoria = value
        for cat in self.categorias:
            if cat["id"] == value:
                self.editar_evento_categoria_nombre = cat["nombre"]
                break

    def set_editar_evento_fecha(self, value: str):
        self.editar_evento_fecha = value

    def set_editar_evento_hora_inicio(self, value: str):
        self.editar_evento_hora_inicio = value

    def set_editar_evento_hora_fin(self, value: str):
        self.editar_evento_hora_fin = value

    def set_editar_evento_lugar(self, value: str):
        self.editar_evento_lugar = value

    def set_editar_evento_direccion(self, value: str):
        self.editar_evento_direccion = value

    def set_editar_evento_cupo_maximo(self, value: str):
        try:
            self.editar_evento_cupo_maximo = int(value)
        except:
            self.editar_evento_cupo_maximo = 0

    def set_editar_evento_costo(self, value: str):
        self.editar_evento_costo = value

    def mostrar_notificacion(self, mensaje: str, tipo: str = "success"):
        """Muestra una notificación toast temporal - NO retorna nada"""
        self.toast_message = mensaje
        self.toast_type = tipo
        self.show_toast = True

    def ocultar_notificacion(self):
        """Oculta la notificación manualmente"""
        self.show_toast = False

    def toggle_sidebar(self):
        self.show_sidebar = not self.show_sidebar
    
    def toggle_login(self):
        self.is_logged_in = not self.is_logged_in
    
    def set_page(self, page: str):
        self.current_page = page
        self.show_sidebar = False
    
    def set_termino_busqueda(self, value: str):
        self.termino_busqueda = value
    
    def toggle_categoria_filter(self, id_categoria: int):
        if id_categoria in self.categorias_seleccionadas:
            self.categorias_seleccionadas.remove(id_categoria)
        else:
            self.categorias_seleccionadas.append(id_categoria)
        self.aplicar_filtros()
    
    def aplicar_filtros(self):
        if not self.categorias_seleccionadas:
            self.eventos_filtrados = self.eventos
        else:
            if not self.eventos or len(self.eventos) == 0:
                self.eventos_filtrados = []
                return
            
            self.eventos_filtrados = [
                e for e in self.eventos 
                if int(e[2]) in self.categorias_seleccionadas
            ]
    
    def cargar_categorias(self):
        try:
            dao = CategoriaDAO()
            result = dao.listar_categorias()
            self.categorias = [{"id": r[0], "nombre": r[1], "descripcion": r[2]} for r in result]
        except Exception as e:
            print(f"Error cargando categorías: {e}")
    
    def cargar_eventos(self):
        try:
            dao = EventoDAO()
            result = dao.eventos_recomendados()
            
            # Convertir a lista de tuplas simples
            eventos_convertidos = []
            for evento in result:
                evento_tuple = tuple(
                    str(item) if not isinstance(item, (int, float, str, type(None))) else item 
                    for item in evento
                )
                eventos_convertidos.append(evento_tuple)
            
            self.eventos = eventos_convertidos
            self.eventos_filtrados = eventos_convertidos
        except Exception as e:
            print(f"❌ Error cargando eventos: {e}")
        
    def cargar_mis_eventos(self):
        try:
            dao = UsuarioDAO()
            result = dao.eventos_creados_usuario(self.id_usuario_logueado)
            
            # Convertir a lista de tuplas simples
            eventos_convertidos = []
            for evento in result:
                evento_tuple = tuple(
                    str(item) if not isinstance(item, (int, float, str)) else item 
                    for item in evento
                )
                eventos_convertidos.append(evento_tuple)
            
            self.mis_eventos = eventos_convertidos
        except Exception as e:
            print(f"Error cargando mis eventos: {e}")

    def cargar_mis_asistencias(self):
        try:
            dao = UsuarioDAO()
            result = dao.eventos_asistiendo_usuario(self.id_usuario_logueado)
            
            # Convertir a lista de tuplas simples
            eventos_convertidos = []
            for evento in result:
                evento_tuple = tuple(
                    str(item) if not isinstance(item, (int, float, str)) else item 
                    for item in evento
                )
                eventos_convertidos.append(evento_tuple)
            
            self.mis_asistencias = eventos_convertidos
        except Exception as e:
            print(f"Error cargando asistencias: {e}")
    
    def cargar_perfil_usuario(self):
        try:
            dao = UsuarioDAO()
            result = dao.obtener_perfil(self.id_usuario_logueado)
            if result:
                self.usuario_nombre = result[0][2]
                self.usuario_email = result[0][1]
                self.usuario_descripcion = result[0][3] if result[0][3] else ""
                self.usuario_telefono = result[0][4] if result[0][4] else ""
        except Exception as e:
            print(f"Error cargando perfil: {e}")
    
    def toggle_crear_evento_modal(self):
        if not self.is_logged_in:
            self.mostrar_notificacion("Debes iniciar sesión para crear eventos", "error")  # ← SIN return
            return
        
        self.show_crear_evento_modal = not self.show_crear_evento_modal
        if self.show_crear_evento_modal and not self.categorias:
            self.cargar_categorias()
    
    def crear_evento(self):
        try:
            # Validaciones
            if not self.nuevo_evento_titulo:
                self.mostrar_notificacion("El título es obligatorio", "error")  # ← SIN yield
                return
            
            if not self.nuevo_evento_categoria or self.nuevo_evento_categoria == 0:
                self.mostrar_notificacion("Selecciona una categoría", "error")  # ← SIN yield
                return
            
            if not self.nuevo_evento_fecha:
                self.mostrar_notificacion("La fecha es obligatoria", "error")  # ← SIN yield
                return
            
            if not self.nuevo_evento_hora_inicio:
                self.mostrar_notificacion("La hora de inicio es obligatoria", "error")  # ← SIN yield
                return
            
            dao = EventoDAO()
            dao.evento.id_usuario_creador = self.id_usuario_logueado
            dao.evento.id_categoria = self.nuevo_evento_categoria
            dao.evento.titulo = self.nuevo_evento_titulo
            dao.evento.descripcion = self.nuevo_evento_descripcion
            dao.evento.fecha = self.nuevo_evento_fecha
            
            dao.evento.hora_inicio = self.nuevo_evento_hora_inicio + ":00" if len(self.nuevo_evento_hora_inicio) == 5 else self.nuevo_evento_hora_inicio
            dao.evento.hora_fin = self.nuevo_evento_hora_fin + ":00" if self.nuevo_evento_hora_fin and len(self.nuevo_evento_hora_fin) == 5 else self.nuevo_evento_hora_fin
            
            dao.evento.lugar = self.nuevo_evento_lugar
            dao.evento.direccion = self.nuevo_evento_direccion
            dao.evento.cupo_maximo = self.nuevo_evento_cupo_maximo
            dao.evento.costo = self.nuevo_evento_costo
            
            dao.crear_evento()
            self.limpiar_form_evento()
            self.show_crear_evento_modal = False
            self.cargar_mis_eventos()
            self.cargar_eventos()
            self.mostrar_notificacion("¡Evento creado exitosamente! 🎉", "success")  # ← SIN yield
            
        except Exception as e:
            print(f"Error creando evento: {e}")
            self.mostrar_notificacion(f"Error al crear evento", "error")  
    
    def limpiar_form_evento(self):
        self.nuevo_evento_titulo = ""
        self.nuevo_evento_descripcion = ""
        self.nuevo_evento_categoria = 0
        self.nuevo_evento_categoria_nombre = "Seleccionar..."
        self.nuevo_evento_fecha = ""
        self.nuevo_evento_hora_inicio = ""
        self.nuevo_evento_hora_fin = ""
        self.nuevo_evento_lugar = ""
        self.nuevo_evento_direccion = ""
        self.nuevo_evento_cupo_maximo = 0
        self.nuevo_evento_costo = ""
        self.mensaje_error = ""
    
    def cerrar_sesion(self):
        self.is_logged_in = False
        self.id_usuario_logueado = 0
        self.usuario_nombre = ""
        self.usuario_email = ""
        self.usuario_telefono = ""
        self.usuario_descripcion = ""
        self.set_page("home")
        self.mostrar_notificacion("Sesión cerrada correctamente", "success")
    
    # Setters para form crear evento
    def set_nuevo_evento_titulo(self, value: str):
        self.nuevo_evento_titulo = value
    
    def set_nuevo_evento_descripcion(self, value: str):
        self.nuevo_evento_descripcion = value
    
    def set_nuevo_evento_categoria(self, value):
        if isinstance(value, int):
            self.nuevo_evento_categoria = value
            # Encontrar el nombre
            for cat in self.categorias:
                if cat["id"] == value:
                    self.nuevo_evento_categoria_nombre = cat["nombre"]
                    break
        else:
            # Buscar el ID de la categoría por nombre
            for cat in self.categorias:
                if cat["nombre"] == value:
                    self.nuevo_evento_categoria = cat["id"]
                    self.nuevo_evento_categoria_nombre = cat["nombre"]
                    break
    
    def set_nuevo_evento_fecha(self, value: str):
        self.nuevo_evento_fecha = value
    
    def set_nuevo_evento_hora_inicio(self, value: str):
        self.nuevo_evento_hora_inicio = value
    
    def set_nuevo_evento_hora_fin(self, value: str):
        self.nuevo_evento_hora_fin = value
    
    def set_nuevo_evento_lugar(self, value: str):
        self.nuevo_evento_lugar = value
    
    def set_nuevo_evento_direccion(self, value: str):
        self.nuevo_evento_direccion = value
    
    def set_nuevo_evento_cupo_maximo(self, value: str):
        try:
            self.nuevo_evento_cupo_maximo = int(value)
        except:
            self.nuevo_evento_cupo_maximo = 0
    
    def set_nuevo_evento_costo(self, value: str):
        self.nuevo_evento_costo = value
    
    def toggle_login_modal(self):
        self.show_login_modal = not self.show_login_modal
        self.mensaje_error = ""
    
    def toggle_registro_modal(self):
        self.show_registro_modal = not self.show_registro_modal
        self.mensaje_error = ""
    
    def set_login_email(self, value: str):
        self.login_email = value
    
    def set_login_password(self, value: str):
        self.login_password = value
    
    def set_registro_nombre(self, value: str):
        self.registro_nombre = value
    
    def set_registro_email(self, value: str):
        self.registro_email = value
    
    def set_registro_password(self, value: str):
        self.registro_password = value
    
    def set_registro_telefono(self, value: str):
        self.registro_telefono = value
    
    def iniciar_sesion(self):
        try:
            if not self.login_email:
                self.mensaje_error = "El email es obligatorio"
                return
            
            if not self.login_password:
                self.mensaje_error = "La contraseña es obligatoria"
                return
            
            import hashlib
            dao = UsuarioDAO()
            result = dao.login_usuario(self.login_email)
            
            if result and len(result) > 0:
                password_hash = hashlib.sha256(self.login_password.encode()).hexdigest()
                
                if result[0][2] == password_hash:
                    self.id_usuario_logueado = result[0][0]
                    self.usuario_nombre = result[0][3]
                    self.usuario_email = result[0][1]
                    self.usuario_descripcion = result[0][4] if result[0][4] else ""
                    self.usuario_telefono = result[0][5] if result[0][5] else ""
                    self.is_logged_in = True
                    self.show_login_modal = False
                    self.login_email = ""
                    self.login_password = ""
                    print("✅ Sesión iniciada correctamente")
                    self.mostrar_notificacion(f"¡Bienvenido {self.usuario_nombre}!", "success")  # ← SIN return ni yield
                else:
                    self.mensaje_error = "Contraseña incorrecta"
            else:
                self.mensaje_error = "Usuario no encontrado"
        except Exception as e:
            print(f"Error iniciando sesión: {e}")
            self.mensaje_error = "Error al iniciar sesión"

    def registrar_usuario(self):
        try:
            if not self.registro_nombre:
                self.mensaje_error = "El nombre es obligatorio"
                return
            
            if not self.registro_email:
                self.mensaje_error = "El email es obligatorio"
                return
            
            if not self.registro_password:
                self.mensaje_error = "La contraseña es obligatoria"
                return
            
            import hashlib
            dao = UsuarioDAO()
            
            # Verificar si el email ya existe
            result = dao.login_usuario(self.registro_email)
            if result and len(result) > 0:
                self.mensaje_error = "Este email ya está registrado"
                self.mostrar_notificacion("Este email ya está registrado", "error")  # ← SIN yield ni return
                return
            
            dao.usuario.email = self.registro_email
            dao.usuario.password_hash = hashlib.sha256(self.registro_password.encode()).hexdigest()
            dao.usuario.nombre = self.registro_nombre
            dao.usuario.telefono = self.registro_telefono
            
            dao.registrar_usuario()
            
            self.show_registro_modal = False
            self.limpiar_form_registro()
            print("✅ Usuario registrado correctamente")
            self.mostrar_notificacion(f"¡Cuenta creada exitosamente! Ahora puedes iniciar sesión", "success")  # ← SIN yield ni return
            
        except Exception as e:
            print(f"Error registrando usuario: {e}")
            self.mensaje_error = "Error al registrar usuario"
            self.mostrar_notificacion("Error al registrar usuario", "error") 

    def limpiar_form_registro(self):
        self.registro_nombre = ""
        self.registro_email = ""
        self.registro_password = ""
        self.registro_telefono = ""
        self.mensaje_error = ""

def sidebar() -> rx.Component:
    return rx.cond(
        State.show_sidebar,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading("NODUS", size="5", 
                              background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                              background_clip="text",
                              style={"-webkit-background-clip": "text", "-webkit-text-fill-color": "transparent"}),
                    rx.button(
                        "✕",
                        on_click=State.toggle_sidebar,
                        bg="transparent",
                        color="white",
                        _hover={"bg": "rgba(255,255,255,0.1)", "transform": "rotate(90deg)"},
                        font_size="1.5em",
                        border_radius="full"
                    ),
                    justify="between",
                    width="100%",
                    padding_bottom="4",
                    border_bottom="1px solid rgba(255,255,255,0.1)"
                ),
                
                rx.vstack(
                    rx.button(
                        "🏠 Home",
                        on_click=lambda: [State.set_page("home"), State.cargar_eventos()],
                        bg="transparent",
                        justify_content="start",
                        width="100%",
                        color="white",
                        _hover={"bg": "rgba(102, 126, 234, 0.2)", "transform": "translateX(10px)"},
                        font_size="1.1em",
                        padding_y="3",
                        border_radius="lg"
                    ),
                    rx.button(
                        "🎯 Eventos",
                        on_click=lambda: [State.set_page("eventos"), State.cargar_todos_eventos(), State.cargar_categorias()],
                        bg="transparent",
                        justify_content="start",
                        width="100%",
                        color="white",
                        _hover={"bg": "rgba(102, 126, 234, 0.2)", "transform": "translateX(10px)"},
                        font_size="1.1em",
                        padding_y="3",
                        border_radius="lg"
                    ),
                    rx.button(
                        "👤 Mi Perfil",
                        on_click=lambda: [State.set_page("perfil"), State.cargar_perfil_usuario(), State.cargar_mis_eventos(), State.cargar_mis_asistencias()],
                        bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        justify_content="start",
                        width="100%",
                        color="white",
                        _hover={"transform": "scale(1.05)", "box_shadow": "0 8px 25px rgba(102, 126, 234, 0.4)"},
                        font_size="1.1em",
                        padding_y="3",
                        border_radius="lg"
                    ),
                    spacing="2"
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
            bg="rgba(0,0,0,0.95)",
            backdrop_filter="blur(10px)",
            border_right="1px solid rgba(255,255,255,0.1)",
            z_index="1000",
            padding="6"
        )
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(width="40px"),
            rx.button(
                "☰",
                on_click=State.toggle_sidebar,
                bg="transparent",
                color="white",
                _hover={"bg": "rgba(102, 126, 234, 0.2)", "transform": "scale(1.1)"},
                border_radius="md",
                font_size="2em",
                padding="3"
            ),
            rx.box(width="5px"),
            rx.spacer(),
            rx.image(
                src="/logo.jpeg",
                on_click=lambda: [State.set_page("home"), State.cargar_eventos()],
                width="200px",
                height="100px",
                border_radius="12px"
            ),
            rx.spacer(),
            rx.cond(
                State.is_logged_in,
                rx.hstack(
                    rx.button(
                        "Mi Perfil",
                        on_click=lambda: State.ir_a_perfil(),
                        bg="transparent", 
                        color="white",
                        _hover={"bg": "rgba(102, 126, 234, 0.2)"},
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
                        border="2px solid rgba(102, 126, 234, 0.5)",
                        on_click=State.toggle_login_modal,
                        padding_x="5",
                        padding_y="3",
                        font_size="1.3em"
                    ),
                    rx.button(
                        "Registrarse",
                        bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        on_click=State.toggle_registro_modal,
                        color="white",
                        padding_x="5",
                        padding_y="3",
                        font_size="1.3em"
                    ),
                    spacing="4"
                )
            ),
            rx.box(width="40px"),
            align="center",
            padding_y="6",
            height="120px",
            width="100%"
        ),
        bg="rgba(0,0,0,0.95)",
        backdrop_filter="blur(10px)",
        border_bottom="1px solid rgba(102, 126, 234, 0.2)",
        position="sticky",
        top="0",
        z_index="999"
    )

def home_page() -> rx.Component:
    return rx.box(
        # Hero section
        rx.box(
            rx.container(
                rx.center(
                    rx.vstack(
                        rx.heading(
                            "Encuentra y Crea Eventos Increíbles",
                            size="7",
                            text_align="center",
                            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            background_clip="text",
                            style={"-webkit-background-clip": "text", "-webkit-text-fill-color": "transparent"},
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
        ),
        
        # Sección de eventos recomendados
        rx.container(
            rx.vstack(
                rx.heading("Eventos Recomendados", size="6", color="white", margin_bottom="6"),
                rx.grid(
                    rx.foreach(
                        State.eventos,
                        lambda evento: rx.box(
                            rx.vstack(
                                rx.badge(
                                    evento[14],  # categoria nombre
                                    bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                    color="white",
                                    font_size="1em",
                                    position="absolute",
                                    top="3",
                                    right="3"
                                ),
                                rx.heading(
                                    evento[1],  # titulo
                                    size="5",
                                    color="white",
                                    text_align="center"
                                ),
                                rx.text(
                                    evento[11],  # descripcion
                                    color="gray.400",
                                    text_align="center",
                                    no_of_lines=2
                                ),
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("📅", color="#667eea"),
                                        rx.text(evento[3], color="gray.300"),
                                        spacing="2"
                                    ),
                                    rx.hstack(
                                        rx.text("📍", color="#667eea"),
                                        rx.text(evento[6], color="gray.300"),
                                        spacing="2"
                                    ),
                                    rx.hstack(
                                        rx.text("💰", color="#667eea"),
                                        rx.text(evento[10], color="gray.300"),
                                        spacing="2"
                                    ),
                                    rx.hstack(
                                        rx.text("👥", color="#667eea"),
                                        rx.text(f"{evento[9]}/{evento[8]} cupos", color="gray.300"),
                                        spacing="2"
                                    ),
                                    spacing="2"
                                ),
                                rx.button(
                                    "Ver Detalles",
                                    on_click=lambda ev, evento=evento: State.abrir_modal_detalles_evento(evento),
                                    bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                    color="white",
                                    width="100%"
                                ),
                                spacing="4",
                                padding="6",
                                position="relative"
                            ),
                            bg="rgba(17, 17, 17, 0.8)",
                            border="1px solid rgba(102, 126, 234, 0.3)",
                            border_radius="xl",
                            _hover={"transform": "translateY(-5px)", "border_color": "#667eea"}
                        )
                    ),
                    columns="3",
                    spacing="6",
                    width="100%"
                ),
                
                # MENSAGJE QUE PEDISTE - agregado aquí
                rx.center(
                    rx.text(
                        "Nodus agradece su preferencia, esperamos lo mejor en sus eventos!!!",
                        text_align="center",
                        color="gray.400",
                        font_size="lg",
                        font_weight="medium",
                        margin_top="12",
                        padding_y="3",
                        padding_x="6",
                        bg="rgba(26, 26, 26, 0.3)",
                        border_radius="lg",
                        border="1px solid rgba(102, 126, 234, 0.2)",
                        width="100%",
                        max_width="600px"
                    ),
                    width="100%"
                ),
                
                spacing="8",
                align="center"
            ),
            padding_y="8"
        ),
        
        bg="black",
        min_height="70vh",
        on_mount=State.cargar_eventos
    )
       

def eventos_page() -> rx.Component:
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Todos los Eventos",
                    size="7",
                    color="white",
                    margin_bottom="8"
                ),
                
                # Filtros de categoría
                rx.box(
                    rx.vstack(
                        rx.text("Filtrar por categoría:", color="gray.400", font_size="lg", margin_bottom="4"),
                        rx.flex(
                            rx.foreach(
                                State.categorias,
                                lambda cat: rx.button(
                                    cat["nombre"],
                                    on_click=State.seleccionar_categoria(cat["id"]),
                                    bg=rx.cond(
                                        State.categorias_seleccionadas.contains(cat["id"]),
                                        "linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%)",  # Color más intenso cuando está seleccionado
                                        "linear-gradient(135deg, rgba(102, 126, 234, 0.4) 0%, rgba(118, 75, 162, 0.4) 100%)"   # Color más tenue cuando NO está seleccionado
                                    ),
                                    color=rx.cond(
                                        State.categorias_seleccionadas.contains(cat["id"]),
                                        "white",
                                        "rgba(255, 255, 255, 0.6)"
                                    ),
                                    border=rx.cond(
                                        State.categorias_seleccionadas.contains(cat["id"]),
                                        "2px solid rgba(102, 126, 234, 0.9)",  # Borde más visible cuando está seleccionado
                                        "1px solid rgba(102, 126, 234, 0.2)"
                                    ),
                                    opacity=rx.cond(
                                        State.categorias_seleccionadas.contains(cat["id"]),
                                        "1",      # Totalmente opaco cuando está seleccionado
                                        "0.6"     # Más transparente cuando NO está seleccionado
                                    ),
                                    padding_x="5",
                                    padding_y="3",
                                    border_radius="full",
                                    box_shadow=rx.cond(
                                        State.categorias_seleccionadas.contains(cat["id"]),
                                        "0 0 20px rgba(102, 126, 234, 0.6)",  # Glow effect cuando está seleccionado
                                        "none"
                                    ),
                                    font_weight=rx.cond(
                                        State.categorias_seleccionadas.contains(cat["id"]),
                                        "bold",
                                        "normal"
                                    ),
                                    _hover={"transform": "scale(1.05)"}
                                )
                            ),
                            spacing="3",
                            wrap="wrap"
                        ),
                        width="100%",
                        padding="6",
                        bg="rgba(26, 26, 26, 0.5)",
                        border_radius="lg",
                        border="1px solid rgba(102, 126, 234, 0.2)"
                    ),
                    margin_bottom="8"
                ),
                
                # Grid de eventos
                rx.grid(
                    rx.foreach(
                        State.eventos_filtrados,
                        lambda evento: rx.box(
                            rx.vstack(
                                rx.badge(
                                    evento[14],  # categoria nombre
                                    bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                    color="white",
                                    font_size="1em"
                                ),
                                rx.heading(
                                    evento[1],  # titulo
                                    size="5",
                                    color="white",
                                    text_align="center"
                                ),
                                rx.text(
                                    evento[11],  # descripcion
                                    color="gray.400",
                                    text_align="center",
                                    no_of_lines=2
                                ),
                                rx.vstack(
                                    rx.hstack(
                                        rx.text("📅", color="#667eea"),
                                        rx.text(evento[3], color="gray.300"),
                                        spacing="2"
                                    ),
                                    rx.hstack(
                                        rx.text("📍", color="#667eea"),
                                        rx.text(evento[6], color="gray.300"),
                                        spacing="2"
                                    ),
                                    rx.hstack(
                                        rx.text("💰", color="#667eea"),
                                        rx.text(evento[10], color="gray.300"),
                                        spacing="2"
                                    ),
                                    rx.hstack(
                                        rx.text("👥", color="#667eea"),
                                        rx.text(f"{evento[9]}/{evento[8]} cupos", color="gray.300"),
                                        spacing="2"
                                    ),
                                    spacing="2"
                                ),
                                rx.button(
                                    "Ver Detalles",
                                    on_click=lambda ev, evento=evento: State.abrir_modal_detalles_evento(evento),
                                    bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                    color="white",
                                    width="100%"
                                ),
                                spacing="4",
                                padding="6"
                            ),
                            bg="rgba(17, 17, 17, 0.8)",
                            border="1px solid rgba(102, 126, 234, 0.3)",
                            border_radius="xl",
                            _hover={"transform": "translateY(-5px)", "border_color": "#667eea"}
                        )
                    ),
                    columns="3",
                    spacing="6",
                    width="100%"
                ),
                spacing="6",
                width="100%",
                padding_y="8"
            )
        ),
        bg="black",
        min_height="100vh",
        padding_y="8",
        on_mount=State.cargar_todos_eventos
    )

def modal_crear_evento() -> rx.Component:
    return rx.cond(
        State.show_crear_evento_modal,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Crear Nuevo Evento", size="6", color="white"),
                        rx.button(
                            "✕",
                            on_click=State.toggle_crear_evento_modal,
                            bg="transparent",
                            color="white"
                        ),
                        justify="between",
                        width="100%"
                    ),
                    rx.cond(
                        State.mensaje_error != "",
                        rx.box(
                            rx.text(State.mensaje_error, color="red.400", font_size="sm"),
                            padding="3",
                            bg="rgba(255, 0, 0, 0.1)",
                            border="1px solid rgba(255, 0, 0, 0.3)",
                            border_radius="lg",
                            width="100%"
                        )
                    ),
                    rx.input(
                        placeholder="Título del evento",
                        value=State.nuevo_evento_titulo,
                        on_change=State.set_nuevo_evento_titulo,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.text_area(
                        placeholder="Descripción",
                        value=State.nuevo_evento_descripcion,
                        on_change=State.set_nuevo_evento_descripcion,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%",
                        rows="4"
                    ),
                    
                    rx.vstack(
                        rx.text("Categoría:", color="gray.400"),
                        rx.text(
                            State.nuevo_evento_categoria_nombre,
                            color="white",
                            font_weight="bold",
                            padding="3",
                            bg=rx.cond(
                                State.nuevo_evento_categoria_nombre == "Seleccionar...",
                                "rgba(102, 126, 234, 0.2)",
                                "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                            ),
                            border_radius="lg",
                            width="100%"
                        ),
                        rx.flex(
                            rx.foreach(
                                State.categorias,
                                lambda cat: rx.button(
                                    cat["nombre"],
                                    on_click=State.set_nuevo_evento_categoria(cat["id"]),  # ← Sin lambda interno
                                    bg=rx.cond(
                                        State.nuevo_evento_categoria == cat["id"],  # ← Comparar por ID
                                        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                        "rgba(26, 26, 26, 0.8)"
                                    ),
                                    color="white",
                                    border=rx.cond(
                                        State.nuevo_evento_categoria == cat["id"],  # ← Comparar por ID
                                        "2px solid #667eea",
                                        "1px solid rgba(102, 126, 234, 0.3)"
                                    ),
                                    padding_x="4",
                                    padding_y="2",
                                    border_radius="lg",
                                    _hover={"bg": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"},
                                    font_size="sm"
                                )
                            ),
                            spacing="2",
                            wrap="wrap"
                        ),
                        width="100%",
                        spacing="2"
                    ),
                    
                    rx.hstack(
                        rx.input(
                            type_="date",
                            placeholder="Fecha del evento",
                            value=State.nuevo_evento_fecha,
                            on_change=State.set_nuevo_evento_fecha,
                            bg="rgba(26, 26, 26, 0.8)",
                            color="white",
                            border="1px solid rgba(102, 126, 234, 0.3)"
                        ),
                        rx.input(
                            type_="time",
                            placeholder="Hora inicio",
                            value=State.nuevo_evento_hora_inicio,
                            on_change=State.set_nuevo_evento_hora_inicio,
                            bg="rgba(26, 26, 26, 0.8)",
                            color="white",
                            border="1px solid rgba(102, 126, 234, 0.3)"
                        ),
                        rx.input(
                            type_="time",
                            placeholder="Hora fin",
                            value=State.nuevo_evento_hora_fin,
                            on_change=State.set_nuevo_evento_hora_fin,
                            bg="rgba(26, 26, 26, 0.8)",
                            color="white",
                            border="1px solid rgba(102, 126, 234, 0.3)"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    
                    rx.input(
                        placeholder="Lugar",
                        value=State.nuevo_evento_lugar,
                        on_change=State.set_nuevo_evento_lugar,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.input(
                        placeholder="Dirección completa",
                        value=State.nuevo_evento_direccion,
                        on_change=State.set_nuevo_evento_direccion,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.hstack(
                        rx.input(
                            type_="number",
                            placeholder="Cupo máximo",
                            value=State.nuevo_evento_cupo_maximo,
                            on_change=State.set_nuevo_evento_cupo_maximo,
                            bg="rgba(26, 26, 26, 0.8)",
                            color="white",
                            border="1px solid rgba(102, 126, 234, 0.3)"
                        ),
                        rx.input(
                            placeholder="Costo (ej: Gratis, $100)",
                            value=State.nuevo_evento_costo,
                            on_change=State.set_nuevo_evento_costo,
                            bg="rgba(26, 26, 26, 0.8)",
                            color="white",
                            border="1px solid rgba(102, 126, 234, 0.3)"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    
                    rx.button(
                        "Crear Evento",
                        on_click=State.crear_evento,
                        bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        color="white",
                        width="100%",
                        padding_y="4",
                        _hover={"transform": "scale(1.02)"}
                    ),
                    
                    spacing="4",
                    width="100%",
                    max_width="600px",
                    bg="rgba(0, 0, 0, 0.95)",
                    padding="8",
                    border_radius="xl",
                    border="1px solid rgba(102, 126, 234, 0.3)"
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="2000"
            ),
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            bg="rgba(0, 0, 0, 0.8)",
            z_index="1999"
        )
    )

def modal_confirmar_eliminar() -> rx.Component:
    return rx.cond(
        State.show_confirmar_eliminar,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.heading("⚠️ Confirmar Eliminación", size="6", color="white"),
                    rx.text(
                        "¿Estás seguro de que deseas eliminar este evento? Esta acción no se puede deshacer.",
                        color="gray.300",
                        text_align="center"
                    ),
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            on_click=State.cancelar_eliminar_evento,
                            bg="gray.600",
                            color="white",
                            width="50%",
                            _hover={"bg": "gray.700"}
                        ),
                        rx.button(
                            "Eliminar",
                            on_click=State.eliminar_evento,
                            bg="red.500",
                            color="white",
                            width="50%",
                            _hover={"bg": "red.600"}
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    spacing="4",
                    width="100%",
                    max_width="400px",
                    bg="rgba(0, 0, 0, 0.95)",
                    padding="8",
                    border_radius="xl",
                    border="1px solid rgba(239, 68, 68, 0.5)"
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="2001"
            ),
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            bg="rgba(0, 0, 0, 0.8)",
            z_index="2000"
        )
    )

def modal_editar_evento() -> rx.Component:
    return rx.cond(
        State.show_editar_evento_modal,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.heading("Editar Evento", size="6", color="white"),
                    
                    rx.input(
                        placeholder="Título del evento",
                        value=State.editar_evento_titulo,
                        on_change=State.set_editar_evento_titulo,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.text_area(
                        placeholder="Descripción",
                        value=State.editar_evento_descripcion,
                        on_change=State.set_editar_evento_descripcion,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%",
                        rows="4"
                    ),
                    
                    rx.vstack(
                        rx.text("Categoría:", color="gray.400"),
                        rx.text(
                            State.editar_evento_categoria_nombre,
                            color="white",
                            font_weight="bold",
                            padding="3",
                            bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            border_radius="lg",
                            width="100%"
                        ),
                        rx.flex(
                            rx.foreach(
                                State.categorias,
                                lambda cat: rx.button(
                                    cat["nombre"],
                                    on_click=State.set_editar_evento_categoria(cat["id"]),
                                    bg=rx.cond(
                                        State.editar_evento_categoria == cat["id"],
                                        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                        "rgba(26, 26, 26, 0.8)"
                                    ),
                                    color="white",
                                    border=rx.cond(
                                        State.editar_evento_categoria == cat["id"],
                                        "2px solid #667eea",
                                        "1px solid rgba(102, 126, 234, 0.3)"
                                    ),
                                    padding_x="4",
                                    padding_y="2",
                                    border_radius="lg",
                                    _hover={"bg": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"},
                                    font_size="sm"
                                )
                            ),
                            spacing="2",
                            wrap="wrap"
                        ),
                        width="100%",
                        spacing="2"
                    ),
                    
                    rx.hstack(
                        rx.input(
                            type_="date",
                            value=State.editar_evento_fecha,
                            on_change=State.set_editar_evento_fecha,
                            bg="rgba(26, 26, 26, 0.8)",
                            color="white",
                            border="1px solid rgba(102, 126, 234, 0.3)"
                        ),
                        rx.input(
                            type_="time",
                            value=State.editar_evento_hora_inicio,
                            on_change=State.set_editar_evento_hora_inicio,
                            bg="rgba(26, 26, 26, 0.8)",
                            color="white",
                            border="1px solid rgba(102, 126, 234, 0.3)"
                        ),
                        rx.input(
                            type_="time",
                            value=State.editar_evento_hora_fin,
                            on_change=State.set_editar_evento_hora_fin,
                            bg="rgba(26, 26, 26, 0.8)",
                            color="white",
                            border="1px solid rgba(102, 126, 234, 0.3)"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    
                    rx.input(
                        placeholder="Lugar",
                        value=State.editar_evento_lugar,
                        on_change=State.set_editar_evento_lugar,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.input(
                        placeholder="Dirección completa",
                        value=State.editar_evento_direccion,
                        on_change=State.set_editar_evento_direccion,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.hstack(
                        rx.input(
                            type_="number",
                            placeholder="Cupo máximo",
                            value=State.editar_evento_cupo_maximo,
                            on_change=State.set_editar_evento_cupo_maximo,
                            bg="rgba(26, 26, 26, 0.8)",
                            color="white",
                            border="1px solid rgba(102, 126, 234, 0.3)"
                        ),
                        rx.input(
                            placeholder="Costo",
                            value=State.editar_evento_costo,
                            on_change=State.set_editar_evento_costo,
                            bg="rgba(26, 26, 26, 0.8)",
                            color="white",
                            border="1px solid rgba(102, 126, 234, 0.3)"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            on_click=State.cerrar_modal_editar_evento,
                            bg="gray.600",
                            color="white",
                            width="50%"
                        ),
                        rx.button(
                            "Actualizar Evento",
                            on_click=State.actualizar_evento,
                            bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            color="white",
                            width="50%"
                        ),
                        spacing="3",
                        width="100%"
                    ),
                    
                    spacing="4",
                    width="100%",
                    max_width="600px",
                    bg="rgba(0, 0, 0, 0.95)",
                    padding="8",
                    border_radius="xl",
                    border="1px solid rgba(102, 126, 234, 0.3)"
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="2001"
            ),
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            bg="rgba(0, 0, 0, 0.8)",
            z_index="2000"
        )
    )

def set_show_editar_evento_modal(self, value: bool):
    self.show_editar_evento_modal = value

def modal_login() -> rx.Component:
    return rx.cond(
        State.show_login_modal,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Iniciar Sesión", size="6", color="white"),
                        rx.button(
                            "✕",
                            on_click=State.toggle_login_modal,
                            bg="transparent",
                            color="white"
                        ),
                        justify="between",
                        width="100%"
                    ),
                    
                    rx.cond(
                        State.mensaje_error != "",
                        rx.box(
                            rx.text(State.mensaje_error, color="red.400"),
                            padding="3",
                            bg="rgba(255, 0, 0, 0.1)",
                            border_radius="lg",
                            width="100%"
                        )
                    ),
                    
                    rx.input(
                        placeholder="Email",
                        type_="email",
                        value=State.login_email,
                        on_change=State.set_login_email,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.input(
                        placeholder="Contraseña",
                        type_="password",
                        value=State.login_password,
                        on_change=State.set_login_password,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.button(
                        "Iniciar Sesión",
                        on_click=State.iniciar_sesion,
                        bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        color="white",
                        width="100%",
                        padding_y="4"
                    ),
                    
                    spacing="4",
                    width="100%",
                    max_width="400px",
                    bg="rgba(0, 0, 0, 0.95)",
                    padding="8",
                    border_radius="xl",
                    border="1px solid rgba(102, 126, 234, 0.3)"
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="2000"
            ),
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            bg="rgba(0, 0, 0, 0.8)",
            z_index="1999"
        )
    )

def modal_registro() -> rx.Component:
    return rx.cond(
        State.show_registro_modal,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Registrarse", size="6", color="white"),
                        rx.button(
                            "✕",
                            on_click=State.toggle_registro_modal,
                            bg="transparent",
                            color="white"
                        ),
                        justify="between",
                        width="100%"
                    ),
                    
                    rx.cond(
                        State.mensaje_error != "",
                        rx.box(
                            rx.text(State.mensaje_error, color="red.400"),
                            padding="3",
                            bg="rgba(255, 0, 0, 0.1)",
                            border_radius="lg",
                            width="100%"
                        )
                    ),
                    
                    rx.input(
                        placeholder="Nombre completo",
                        value=State.registro_nombre,
                        on_change=State.set_registro_nombre,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.input(
                        placeholder="Email",
                        type_="email",
                        value=State.registro_email,
                        on_change=State.set_registro_email,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.input(
                        placeholder="Contraseña",
                        type_="password",
                        value=State.registro_password,
                        on_change=State.set_registro_password,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.input(
                        placeholder="Teléfono (opcional)",
                        value=State.registro_telefono,
                        on_change=State.set_registro_telefono,
                        bg="rgba(26, 26, 26, 0.8)",
                        color="white",
                        border="1px solid rgba(102, 126, 234, 0.3)",
                        width="100%"
                    ),
                    
                    rx.button(
                        "Registrarse",
                        on_click=State.registrar_usuario,
                        bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        color="white",
                        width="100%",
                        padding_y="4"
                    ),
                    
                    spacing="4",
                    width="100%",
                    max_width="400px",
                    bg="rgba(0, 0, 0, 0.95)",
                    padding="8",
                    border_radius="xl",
                    border="1px solid rgba(102, 126, 234, 0.3)"
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="2000"
            ),
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            bg="rgba(0, 0, 0, 0.8)",
            z_index="1999"
        )
    )

def modal_detalles_evento() -> rx.Component:
    return rx.cond(
        State.show_detalles_evento_modal,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.heading(
                            rx.cond(
                                State.evento_detalle,
                                State.evento_detalle[1],
                                "Evento"
                            ),
                            size="7",
                            color="white"
                        ),
                        rx.button(
                            "✕",
                            on_click=State.cerrar_modal_detalles_evento,
                            bg="transparent",
                            color="white",
                            _hover={"bg": "rgba(255,255,255,0.1)"},
                            font_size="2em"
                        ),
                        justify="between",
                        width="100%",
                        margin_bottom="6"
                    ),
                    
                    # Badge categoría
                    rx.badge(
                        State.evento_detalle[14],
                        bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        color="white",
                        font_size="1.1em",
                        padding="2",
                        margin_bottom="4"
                    ),
                    
                    # Descripción
                    rx.vstack(
                        rx.heading("📋 Descripción", size="4", color="#667eea"),
                        rx.text(
                            State.evento_detalle[11],
                            color="gray.300",
                            font_size="lg"
                        ),
                        spacing="2",
                        width="100%",
                        padding="4",
                        bg="rgba(26, 26, 26, 0.5)",
                        border_radius="lg"
                    ),
                    
                    # Grid información
                    rx.grid(
                        rx.vstack(
                            rx.heading("📅 Fecha", size="3", color="#667eea"),
                            rx.text(State.evento_detalle[3], color="white", font_size="lg"),
                            spacing="1",
                            align_items="start"
                        ),
                        rx.vstack(
                            rx.heading("🕐 Horario", size="3", color="#667eea"),
                            rx.text(
                                f"{State.evento_detalle[4]} - {State.evento_detalle[5]}",
                                color="white",
                                font_size="lg"
                            ),
                            spacing="1",
                            align_items="start"
                        ),
                        rx.vstack(
                            rx.heading("📍 Lugar", size="3", color="#667eea"),
                            rx.text(State.evento_detalle[6], color="white", font_size="lg"),
                            spacing="1",
                            align_items="start"
                        ),
                        rx.vstack(
                            rx.heading("🗺️ Dirección", size="3", color="#667eea"),
                            rx.text(State.evento_detalle[7], color="white", font_size="lg"),
                            spacing="1",
                            align_items="start"
                        ),
                        rx.vstack(
                            rx.heading("👥 Cupos", size="3", color="#667eea"),
                            rx.text(
                                f"{State.evento_detalle[9]}/{State.evento_detalle[8]} ocupados",
                                color="white",
                                font_size="lg"
                            ),
                            spacing="1",
                            align_items="start"
                        ),
                        rx.vstack(
                            rx.heading("💰 Costo", size="3", color="#667eea"),
                            rx.text(State.evento_detalle[10], color="white", font_size="lg"),
                            spacing="1",
                            align_items="start"
                        ),
                        
                        columns="2",
                        spacing="6",
                        width="100%",
                        padding="6",
                        bg="rgba(26, 26, 26, 0.5)",
                        border_radius="lg"
                    ),
                    
                    # Botón registro
                    rx.button(
                        "✅ Registrarme al evento",
                        on_click=lambda: State.registrar_asistencia(State.evento_detalle[0]),
                        bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        color="white",
                        width="100%",
                        padding_y="5",
                        font_size="1.2em",
                        _hover={"transform": "scale(1.02)", "box_shadow": "0 8px 25px rgba(102, 126, 234, 0.4)"}
                    ),
                    
                    spacing="6",
                    width="100%",
                    max_width="700px",
                    bg="rgba(0, 0, 0, 0.95)",
                    padding="8",
                    border_radius="xl",
                    border="1px solid rgba(102, 126, 234, 0.3)"
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="2001",
                max_height="90vh",
                overflow_y="auto"
            ),
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            bg="rgba(0, 0, 0, 0.8)",
            z_index="2000"
        )
    )

def perfil_page() -> rx.Component:
    return rx.box(
        modal_crear_evento(),
        rx.container(
            rx.vstack(
                # Header del perfil
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Mi Perfil",
                            size="7",
                            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            background_clip="text",
                            style={"-webkit-background-clip": "text", "-webkit-text-fill-color": "transparent"},
                            margin_bottom="4"
                        ),
                        
                        rx.grid(
                            # Columna izquierda
                            rx.vstack(
                                rx.text("Nombre completo:", color="gray.400", font_size="sm"),
                                rx.text(State.usuario_nombre, color="white", font_size="xl", font_weight="bold"),
                                
                                rx.text("Email:", color="gray.400", font_size="sm", margin_top="4"),
                                rx.text(State.usuario_email, color="white", font_size="lg"),
                                
                                rx.text("Teléfono:", color="gray.400", font_size="sm", margin_top="4"),
                                rx.text(
                                    rx.cond(
                                        State.usuario_telefono != "",
                                        State.usuario_telefono,
                                        "No especificado"
                                    ),
                                    color="white",
                                    font_size="lg"
                                ),
                                
                                align_items="start",
                                width="100%"
                            ),
                            
                            # Columna derecha
                            rx.vstack(
                                rx.text("Descripción:", color="gray.400", font_size="sm"),
                                rx.text(
                                    rx.cond(
                                        State.usuario_descripcion != "",
                                        State.usuario_descripcion,
                                        "Sin descripción"
                                    ),
                                    color="white",
                                    font_size="md"
                                ),
                                
                                rx.button(
                                    "🚪 Cerrar Sesión",
                                    on_click=State.cerrar_sesion,
                                    bg="red.500",
                                    color="white",
                                    margin_top="2",
                                    _hover={"bg": "red.600"}
                                ),
                                
                                align_items="start",
                                width="100%"
                            ),
                            
                            columns="2",
                            spacing="8",
                            width="100%"
                        ),
                        
                        spacing="4",
                        width="100%"
                    ),
                    padding="8",
                    bg="rgba(26, 26, 26, 0.5)",
                    border_radius="xl",
                    border="1px solid rgba(102, 126, 234, 0.3)",
                    margin_bottom="8"
                ),
                
                # Tabs: Mis Eventos y Asistencias
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Mis Eventos Creados", value="eventos"),
                        rx.tabs.trigger("Mis Asistencias", value="asistencias"),
                    ),
                    
                    # Panel Mis Eventos
                    rx.tabs.content(
                        rx.vstack(
                            rx.button(
                                "+ Crear Nuevo Evento",
                                on_click=State.toggle_crear_evento_modal,
                                bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                color="white",
                                size="3",
                                margin_bottom="6"
                            ),
                            rx.grid(
                                rx.foreach(
                                    State.mis_eventos,
                                    lambda evento: rx.box(
                                        rx.vstack(
                                            rx.badge(
                                                evento[12],  # categoria_nombre
                                                bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                                color="white",
                                                font_size="0.9em",
                                                margin_bottom="2"
                                            ),
                                            rx.heading(evento[1], size="4", color="white", margin_bottom="2"),
                                            rx.text(evento[11], color="gray.400", no_of_lines=2, margin_bottom="3"),
                                            rx.vstack(
                                                rx.hstack(
                                                    rx.text("📅", color="#667eea"),
                                                    rx.text(f"{evento[3]} • {str(evento[4])[:5]}", color="gray.300"),
                                                    spacing="2"
                                                ),
                                                rx.hstack(
                                                    rx.text("📍", color="#667eea"),
                                                    rx.text(evento[6], color="gray.300"),
                                                    spacing="2"
                                                ),
                                                rx.hstack(
                                                    rx.text("💰", color="#667eea"),
                                                    rx.text(evento[10], color="gray.300"),
                                                    spacing="2"
                                                ),
                                                rx.hstack(
                                                    rx.text("👥", color="#667eea"),
                                                    rx.text(f"{evento[9]}/{evento[8]} cupos", color="gray.300"),
                                                    spacing="2"
                                                ),
                                                spacing="2",
                                                width="100%"
                                            ),
                                            rx.hstack(
                                                rx.button(
                                                    "✏️ Editar",
                                                    on_click=State.abrir_modal_editar_evento(evento),
                                                    bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                                    color="white",
                                                    size="2",
                                                    flex="1"
                                                ),
                                                rx.button(
                                                    "❌ Eliminar",
                                                    on_click=State.confirmar_eliminar_evento(evento[0]),
                                                    bg="red.500",
                                                    color="white",
                                                    size="2",
                                                    flex="1"
                                                ),
                                                spacing="2",
                                                width="100%",
                                                margin_top="3"
                                            ),
                                            spacing="2",
                                            padding="5"
                                        ),
                                        bg="rgba(17, 17, 17, 0.8)",
                                        border="1px solid rgba(102, 126, 234, 0.3)",
                                        border_radius="lg",
                                        _hover={"border_color": "#667eea", "transform": "translateY(-3px)"}
                                    )
                                ),
                                columns="3",
                                spacing="5"
                            ),
                            width="100%"
                        ),
                        value="eventos"
                    ),
                    
                    # Panel Asistencias
                    rx.tabs.content(
                        rx.cond(
                            State.mis_asistencias,
                            rx.grid(
                                rx.foreach(
                                    State.mis_asistencias,
                                    lambda evento: rx.box(
                                        rx.vstack(
                                            rx.badge(
                                                evento[14],  # categoria_nombre
                                                bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                                color="white",
                                                font_size="0.9em",
                                                margin_bottom="2"
                                            ),
                                            rx.heading(evento[1], size="4", color="white", margin_bottom="2"),
                                            rx.text(evento[11], color="gray.400", no_of_lines=2, margin_bottom="3"),
                                            rx.vstack(
                                                rx.hstack(
                                                    rx.text("📅", color="#667eea"),
                                                    rx.text(f"{evento[3]} • {str(evento[4])[:5]}", color="gray.300"),
                                                    spacing="2"
                                                ),
                                                rx.hstack(
                                                    rx.text("📍", color="#667eea"),
                                                    rx.text(evento[6], color="gray.300"),
                                                    spacing="2"
                                                ),
                                                rx.hstack(
                                                    rx.text("💰", color="#667eea"),
                                                    rx.text(evento[10], color="gray.300"),
                                                    spacing="2"
                                                ),
                                                rx.hstack(
                                                    rx.text("👥", color="#667eea"),
                                                    rx.text(f"{evento[9]}/{evento[8]} cupos", color="gray.300"),
                                                    spacing="2"
                                                ),
                                                spacing="2",
                                                width="100%"
                                            ),
                                            rx.button(
                                                "❌ Cancelar Asistencia",
                                                on_click=lambda ev, id_reserva=evento[16]: State.cancelar_asistencia(id_reserva),
                                                bg="red.500",
                                                color="white",
                                                width="100%",
                                                size="2",
                                                margin_top="3",
                                                _hover={"bg": "red.600", "transform": "scale(1.02)"}
                                            ),
                                            spacing="2",
                                            padding="5"
                                        ),
                                        bg="rgba(17, 17, 17, 0.8)",
                                        border="1px solid rgba(102, 126, 234, 0.3)",
                                        border_radius="lg",
                                        _hover={"border_color": "#667eea", "transform": "translateY(-3px)"}
                                    )
                                ),
                                columns="3",
                                spacing="5"
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.text("📭", font_size="4em"),
                                    rx.text(
                                        "No tienes asistencias registradas",
                                        color="gray.400",
                                        font_size="lg"
                                    ),
                                    rx.button(
                                        "Ver Eventos Disponibles",
                                        on_click=lambda: [State.set_page("eventos"), State.cargar_eventos(), State.cargar_categorias()],
                                        bg="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                        color="white",
                                        margin_top="4"
                                    ),
                                    spacing="3",
                                    align="center",
                                    padding="8"
                                ),
                                text_align="center"
                            )
                        ),
                        value="asistencias"
                    ),
                    
                    default_value="eventos",
                    color_scheme="purple",
                    width="100%"
                ),
                
                spacing="6",
                width="100%",
                padding_y="8"
            )
        ),
        bg="black",
        min_height="100vh"
    )


def toast_notification() -> rx.Component:
    return rx.cond(
        State.show_toast,
        rx.box(
            rx.hstack(
                rx.cond(
                    State.toast_type == "success",
                    rx.text("✓", color="green.400", font_size="xl", font_weight="bold"),
                    rx.cond(
                        State.toast_type == "error",
                        rx.text("✕", color="red.400", font_size="xl", font_weight="bold"),
                        rx.text("ℹ", color="blue.400", font_size="xl", font_weight="bold")
                    )
                ),
                rx.text(
                    State.toast_message,
                    color="white",
                    font_weight="500"
                ),
                rx.button(
                    "×",
                    on_click=State.ocultar_notificacion,  # ← NUEVO: botón para cerrar
                    bg="transparent",
                    color="white",
                    _hover={"bg": "rgba(255,255,255,0.1)"},
                    font_size="xl",
                    padding="0",
                    min_width="30px",
                    height="30px"
                ),
                spacing="3",
                align="center"
            ),
            position="fixed",
            top="20px",
            right="20px",
            bg=rx.cond(
                State.toast_type == "success",
                "rgba(34, 197, 94, 0.9)",
                rx.cond(
                    State.toast_type == "error",
                    "rgba(239, 68, 68, 0.9)",
                    "rgba(59, 130, 246, 0.9)"
                )
            ),
            padding="4",
            border_radius="lg",
            box_shadow="0 10px 40px rgba(0, 0, 0, 0.3)",
            z_index="9999",
            min_width="250px",
            animation="slideInRight 0.3s ease-out"
        )
    )

def index() -> rx.Component:
    return rx.box(
        toast_notification(),
        modal_login(),  # ← Agregar
        modal_registro(),  # ← Agregar
        modal_editar_evento(),  # ← Agregar
        modal_confirmar_eliminar(),
        modal_detalles_evento(),
        sidebar(),
        navbar(),
        rx.cond(
            State.current_page == "home",
            home_page(),
            rx.cond(
                State.current_page == "eventos",
                eventos_page(),
                rx.cond(
                    State.current_page == "perfil",
                    perfil_page(),
                    home_page()
                )
            )
        ),
        bg="black",
        min_height="100vh",
        color="white"
    )

app = rx.App()
app.add_page(index)