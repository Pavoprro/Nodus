import sys
import os

# Agregar el path para importar los DAOs
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
import hashlib

# Importar los DAOs
from modelo.app.usuario_dao import UsuarioDAO
from modelo.app.evento_dao import EventoDAO
from modelo.app.categoria_dao import CategoriaDAO
from modelo.app.reserva_dao import ReservaDAO

# ===================== ESTILO (PALETA NODUS) =====================

APP_STYLE = """
QWidget {
    background-color: #05050B;
    color: #FFFFFF;
    font-family: "Segoe UI", "Arial";
}

QLabel {
    color: #FFFFFF;
}

QLineEdit,
QTextEdit,
QPlainTextEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox,
QDateEdit,
QTimeEdit,
QDateTimeEdit {
    background-color: #11111B;
    border: 1px solid #2B2B3C;
    border-radius: 6px;
    padding: 6px 10px;
    color: #FFFFFF;
}

QComboBox QAbstractItemView {
    background-color: #11111B;
    color: #FFFFFF;
}

QListWidget {
    background-color: #11111B;
    border: 1px solid #2B2B3C;
    border-radius: 8px;
    padding: 4px;
}

QPushButton {
    background-color: #1A001F;
    border: 1px solid #A020F0;
    border-radius: 18px;
    padding: 8px 16px;
    color: #FFFFFF;
}
QPushButton:hover {
    background-color: #A020F0;
}
QPushButton:pressed {
    background-color: #C65BFF;
}

QPushButton#ghostButton {
    background-color: transparent;
    border: 1px solid #A020F0;
    border-radius: 18px;
    padding: 8px 16px;
    color: #A020F0;
}
QPushButton#ghostButton:hover {
    background-color: #11111B;
}

QPushButton#deleteButton {
    background-color: transparent;
    border: 1px solid #FF6B6B;
    border-radius: 18px;
    padding: 8px 16px;
    color: #FF6B6B;
}
QPushButton#deleteButton:hover {
    background-color: #FF6B6B;
    color: #FFFFFF;
}

QGroupBox {
    border: 1px solid #2B2B3C;
    border-radius: 10px;
    margin-top: 18px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 4px;
    color: #C65BFF;
}

QStatusBar {
    background-color: #05050B;
    color: #B0B0B0;
}
"""


# ===================== LOGIN CON BD =====================

class LoginWindow(QtWidgets.QWidget):
    login_success = pyqtSignal(int, str, str, str, str)  # id, nombre, email, desc, tel
    register_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nodus - Iniciar Sesión")
        self.setFixedSize(500, 560)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        lbl_logo = QtWidgets.QLabel("Nodus")
        font_logo = QtGui.QFont("Segoe UI", 26, QtGui.QFont.Bold)
        lbl_logo.setFont(font_logo)
        lbl_logo.setAlignment(QtCore.Qt.AlignCenter)

        lbl_sub = QtWidgets.QLabel("Encuentra y crea eventos increíbles")
        lbl_sub.setAlignment(QtCore.Qt.AlignCenter)
        lbl_sub.setStyleSheet("color: #B0B0B0;")

        layout.addWidget(lbl_logo)
        layout.addWidget(lbl_sub)

        form = QtWidgets.QVBoxLayout()
        form.setSpacing(12)

        lbl_mail = QtWidgets.QLabel("Correo electrónico")
        lbl_mail.setStyleSheet("margin-bottom: 6px;") 
        self.txt_mail = QtWidgets.QLineEdit()
        self.txt_mail.setPlaceholderText("usuario@ejemplo.com")
        self.txt_mail.setMinimumHeight(42)
        self.txt_mail.setStyleSheet("""
            background-color: #11111B;
            border: 1px solid #2B2B3C;
            border-radius: 8px;
            padding: 10px 15px;
            color: #FFFFFF;
            font-size: 14px;
            margin-bottom: 12px;
        """)

        lbl_pass = QtWidgets.QLabel("Contraseña")
        lbl_pass.setStyleSheet("margin-bottom: 6px;") 
        self.txt_pass = QtWidgets.QLineEdit()
        self.txt_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_pass.setPlaceholderText("••••••••••")
        self.txt_pass.setMinimumHeight(42)
        self.txt_pass.setStyleSheet("""
            background-color: #11111B;
            border: 1px solid #2B2B3C;
            border-radius: 8px;
            padding: 10px 15px;
            color: #FFFFFF;
            font-size: 14px;
            margin-bottom: 12px;
        """)

        form.addWidget(lbl_mail)
        form.addWidget(self.txt_mail)
        form.addWidget(lbl_pass)
        form.addWidget(self.txt_pass)

        layout.addLayout(form)

        self.lbl_error = QtWidgets.QLabel("")
        self.lbl_error.setStyleSheet("color: #FF6B6B;")
        layout.addWidget(self.lbl_error)

        btn_login = QtWidgets.QPushButton("Iniciar Sesión")
        btn_register = QtWidgets.QPushButton("Crear cuenta")
        btn_register.setObjectName("ghostButton")

        btn_login.clicked.connect(self.handle_login)
        btn_register.clicked.connect(self.register_requested.emit)

        layout.addWidget(btn_login)
        layout.addWidget(btn_register)

        layout.addStretch()

        lbl_footer = QtWidgets.QLabel("Nodus · 2024")
        lbl_footer.setAlignment(QtCore.Qt.AlignCenter)
        lbl_footer.setStyleSheet("color: #55556B; font-size: 10pt;")
        layout.addWidget(lbl_footer)

    def handle_login(self):
        email = self.txt_mail.text().strip()
        password = self.txt_pass.text()

        if not email or not password:
            self.lbl_error.setText("Completa todos los campos")
            return

        try:
            dao = UsuarioDAO()
            result = dao.login_usuario(email)

            if result and len(result) > 0:
                password_hash = hashlib.sha256(password.encode()).hexdigest()

                if result[0][2] == password_hash:
                    # Login exitoso
                    id_usuario = result[0][0]
                    nombre = result[0][3]
                    email_bd = result[0][1]
                    descripcion = result[0][4] if result[0][4] else ""
                    telefono = result[0][5] if result[0][5] else ""

                    self.login_success.emit(id_usuario, nombre, email_bd, descripcion, telefono)
                    self.lbl_error.setText("")
                    self.txt_mail.clear()
                    self.txt_pass.clear()
                else:
                    self.lbl_error.setText("Contraseña incorrecta")
            else:
                self.lbl_error.setText("Usuario no encontrado")
        except Exception as e:
            self.lbl_error.setText(f"Error: {str(e)}")
            print(f"❌ Error en login: {e}")


# ===================== REGISTRO CON BD =====================

class RegisterWindow(QtWidgets.QWidget):
    register_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nodus - Registro")
        self.setFixedSize(460, 620)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)

        lbl_logo = QtWidgets.QLabel("Crear cuenta Nodus")
        font_logo = QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold)
        lbl_logo.setFont(font_logo)
        lbl_logo.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(lbl_logo)

        form = QtWidgets.QFormLayout()
        form.setSpacing(12)

        self.txt_name = QtWidgets.QLineEdit()
        self.txt_name.setPlaceholderText("Tu nombre")

        self.txt_mail = QtWidgets.QLineEdit()
        self.txt_mail.setPlaceholderText("usuario@ejemplo.com")

        self.txt_phone = QtWidgets.QLineEdit()
        self.txt_phone.setPlaceholderText("Teléfono (ej: 4771234567)")

        self.txt_pass = QtWidgets.QLineEdit()
        self.txt_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_pass.setPlaceholderText("Contraseña")

        self.txt_pass2 = QtWidgets.QLineEdit()
        self.txt_pass2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_pass2.setPlaceholderText("Confirmar contraseña")

        form.addRow("Nombre:", self.txt_name)
        form.addRow("Correo:", self.txt_mail)
        form.addRow("Teléfono:", self.txt_phone)
        form.addRow("Contraseña:", self.txt_pass)
        form.addRow("Confirmar:", self.txt_pass2)

        layout.addLayout(form)

        self.lbl_error = QtWidgets.QLabel("")
        self.lbl_error.setStyleSheet("color: #FF6B6B;")
        layout.addWidget(self.lbl_error)

        btn_register = QtWidgets.QPushButton("Registrarse")
        btn_register.clicked.connect(self.handle_register)
        layout.addWidget(btn_register)

        layout.addStretch()

    def handle_register(self):
        nombre = self.txt_name.text().strip()
        correo = self.txt_mail.text().strip()
        telefono = self.txt_phone.text().strip()
        password = self.txt_pass.text()
        password2 = self.txt_pass2.text()

        if not nombre or not correo or not telefono:
            self.lbl_error.setText("Completa todos los campos")
            return

        if password != password2:
            self.lbl_error.setText("Las contraseñas no coinciden")
            return

        try:
            dao = UsuarioDAO()

            # Verificar si el email ya existe
            result = dao.login_usuario(correo)
            if result and len(result) > 0:
                self.lbl_error.setText("Este email ya está registrado")
                return

            # Registrar usuario
            dao.usuario.email = correo
            dao.usuario.password_hash = hashlib.sha256(password.encode()).hexdigest()
            dao.usuario.nombre = nombre
            dao.usuario.telefono = telefono

            if dao.registrar_usuario():
                QtWidgets.QMessageBox.information(
                    self, "Registro Exitoso",
                    "¡Cuenta creada! Ahora puedes iniciar sesión."
                )
                self.register_success.emit()
                self.txt_name.clear()
                self.txt_mail.clear()
                self.txt_phone.clear()
                self.txt_pass.clear()
                self.txt_pass2.clear()
                self.lbl_error.setText("")
            else:
                self.lbl_error.setText("Error al registrar usuario")
        except Exception as e:
            self.lbl_error.setText(f"Error: {str(e)}")
            print(f"❌ Error en registro: {e}")


# ===================== DIALOGO "CREAR NUEVO EVENTO" CON BD =====================

class NewEventDialog(QtWidgets.QDialog):
    event_created = pyqtSignal()

    def __init__(self, id_usuario_logueado, parent=None):
        super().__init__(parent)
        self.id_usuario_logueado = id_usuario_logueado
        self.setWindowTitle("Crear Nuevo Evento")
        self.resize(900, 650)
        self.setMinimumSize(800, 550)
        self.categorias = []
        self.setup_ui()
        self.cargar_categorias()

    def cargar_categorias(self):
        try:
            dao = CategoriaDAO()
            result = dao.listar_categorias()
            self.categorias = {r[1]: r[0] for r in result}  # {nombre: id}

            # Actualizar botones
            for btn in self.cat_buttons:
                btn.setVisible(btn.text() in self.categorias)
        except Exception as e:
            print(f"❌ Error cargando categorías: {e}")

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QtWidgets.QLabel("Crear Nuevo Evento")
        f = QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold)
        title.setFont(f)
        layout.addWidget(title)

        form = QtWidgets.QFormLayout()
        form.setSpacing(8)

        self.txt_title = QtWidgets.QLineEdit()
        self.txt_desc = QtWidgets.QPlainTextEdit()
        self.txt_desc.setFixedHeight(90)

        form.addRow("Título del evento:", self.txt_title)
        form.addRow("Descripción:", self.txt_desc)

        layout.addLayout(form)

        lbl_cat = QtWidgets.QLabel("Categoría:")
        layout.addWidget(lbl_cat)

        cat_row = QtWidgets.QHBoxLayout()
        cat_row.setSpacing(10)
        self.cat_buttons = []

        for name in ["Aprendizaje", "Cultural", "Deportes",
                     "Gaming", "Natural", "Social"]:
            btn = QtWidgets.QPushButton(name)
            btn.setObjectName("ghostButton")
            btn.setCheckable(True)
            btn.setMinimumWidth(110)
            btn.setMinimumHeight(32)
            btn.clicked.connect(
                lambda checked, b=btn: self.on_category_button_clicked(b)
            )
            self.cat_buttons.append(btn)
            cat_row.addWidget(btn)

        cat_row.addStretch()
        layout.addLayout(cat_row)

        date_time_layout = QtWidgets.QHBoxLayout()

        self.date_event = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date_event.setCalendarPopup(True)
        self.date_event.setMinimumHeight(32)
        self.date_event.setDisplayFormat("yyyy-MM-dd")

        self.time_start = QtWidgets.QTimeEdit(QtCore.QTime.currentTime())
        self.time_start.setMinimumHeight(32)
        self.time_start.setDisplayFormat("HH:mm")

        self.time_end = QtWidgets.QTimeEdit(QtCore.QTime.currentTime().addSecs(3600))
        self.time_end.setMinimumHeight(32)
        self.time_end.setDisplayFormat("HH:mm")

        date_form = QtWidgets.QFormLayout()
        date_form.setSpacing(8)
        date_form.addRow("Fecha del evento:", self.date_event)
        date_form.addRow("Hora inicio:", self.time_start)
        date_form.addRow("Hora fin:", self.time_end)

        date_time_layout.addLayout(date_form)
        layout.addLayout(date_time_layout)

        self.txt_place = QtWidgets.QLineEdit()
        self.txt_address = QtWidgets.QLineEdit()

        layout.addWidget(QtWidgets.QLabel("Lugar:"))
        layout.addWidget(self.txt_place)
        layout.addWidget(QtWidgets.QLabel("Dirección completa:"))
        layout.addWidget(self.txt_address)

        bottom_form = QtWidgets.QHBoxLayout()
        self.spin_quota = QtWidgets.QSpinBox()
        self.spin_quota.setMinimum(1)
        self.spin_quota.setMaximum(100000)
        self.spin_quota.setValue(10)
        self.spin_quota.setMinimumHeight(32)

        self.txt_cost = QtWidgets.QLineEdit()
        self.txt_cost.setPlaceholderText("Costo (ej: Gratis, $100)")
        self.txt_cost.setMinimumHeight(32)

        quota_form = QtWidgets.QFormLayout()
        quota_form.addRow("Cupos:", self.spin_quota)

        cost_form = QtWidgets.QFormLayout()
        cost_form.addRow("Costo:", self.txt_cost)

        bottom_form.addLayout(quota_form)
        bottom_form.addLayout(cost_form)
        layout.addLayout(bottom_form)

        self.lbl_error = QtWidgets.QLabel("")
        self.lbl_error.setStyleSheet("color: #FF6B6B;")
        layout.addWidget(self.lbl_error)

        btn_create = QtWidgets.QPushButton("Crear Evento")
        btn_create.setMinimumHeight(34)
        btn_create.clicked.connect(self.handle_create)
        layout.addWidget(btn_create)

        layout.addStretch()

    def on_category_button_clicked(self, btn):
        for b in self.cat_buttons:
            b.setChecked(b is btn)

    def handle_create(self):
        selected_cat = None
        for b in self.cat_buttons:
            if b.isChecked():
                selected_cat = b.text()
                break

        if not selected_cat:
            self.lbl_error.setText("Selecciona una categoría")
            return

        titulo = self.txt_title.text().strip()
        if not titulo:
            self.lbl_error.setText("El título es obligatorio")
            return

        try:
            dao = EventoDAO()
            dao.evento.id_usuario_creador = self.id_usuario_logueado
            dao.evento.id_categoria = self.categorias[selected_cat]
            dao.evento.titulo = titulo
            dao.evento.descripcion = self.txt_desc.toPlainText()
            dao.evento.fecha = self.date_event.date().toString("yyyy-MM-dd")
            dao.evento.hora_inicio = self.time_start.time().toString("HH:mm:ss")
            dao.evento.hora_fin = self.time_end.time().toString("HH:mm:ss")
            dao.evento.lugar = self.txt_place.text()
            dao.evento.direccion = self.txt_address.text()
            dao.evento.cupo_maximo = self.spin_quota.value()
            dao.evento.costo = self.txt_cost.text() or "Gratis"

            if dao.crear_evento():
                QtWidgets.QMessageBox.information(
                    self, "Evento Creado",
                    "¡Evento creado exitosamente! 🎉"
                )
                self.event_created.emit()
                self.accept()
            else:
                self.lbl_error.setText("Error al crear evento")
        except Exception as e:
            self.lbl_error.setText(f"Error: {str(e)}")
            print(f"❌ Error creando evento: {e}")


# ===================== ITEM DE LISTA CON "VER DETALLES" =====================

class EventItemWidget(QtWidgets.QWidget):
    view_details = pyqtSignal(dict)

    def __init__(self, event_data, parent=None):
        super().__init__(parent)
        self.event_data = event_data

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        summary = f"{event_data['categoria']} · {event_data['titulo']} · {event_data['fecha']} · {event_data['cupos_disponibles']} cupos · {event_data['costo']}"

        lbl = QtWidgets.QLabel(summary)
        lbl.setWordWrap(True)

        btn = QtWidgets.QPushButton("Ver detalles")
        btn.setObjectName("ghostButton")
        btn.setMinimumHeight(26)
        btn.clicked.connect(self.on_view_clicked)

        layout.addWidget(lbl, 1)
        layout.addWidget(btn)

    def on_view_clicked(self):
        self.view_details.emit(self.event_data)


# ===================== DIALOGO DE DETALLES DE EVENTO (MODO DINAMICO) =====================

class EventDetailsDialog(QtWidgets.QDialog):
    register_requested = pyqtSignal(int)  # id_evento
    event_deleted = pyqtSignal()
    attendance_cancelled = pyqtSignal()

    def __init__(self, event_data, id_usuario_logueado, mode="view", parent=None):
        """
        mode puede ser:
        - "view": Ver evento normal con opción de registrarse
        - "delete": Ver mi evento creado con opción de eliminar
        - "cancel": Ver evento al que asisto con opción de cancelar asistencia
        """
        super().__init__(parent)
        self.setWindowTitle("Detalles del Evento")
        self.resize(600, 500)
        self.event_data = event_data
        self.id_usuario_logueado = id_usuario_logueado
        self.mode = mode
        self.setup_ui()

    def setup_ui(self):
        d = self.event_data

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QtWidgets.QLabel(d["titulo"])
        f = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold)
        title.setFont(f)
        layout.addWidget(title)

        cat_date = QtWidgets.QLabel(
            f"{d['categoria']} · {d['fecha']} · {d['hora_inicio']} - {d['hora_fin']}"
        )
        cat_date.setStyleSheet("color: #C65BFF;")
        layout.addWidget(cat_date)

        layout.addWidget(QtWidgets.QLabel(f"Lugar: {d['lugar']}"))
        layout.addWidget(QtWidgets.QLabel(f"Dirección: {d['direccion']}"))
        layout.addWidget(QtWidgets.QLabel(f"Cupos disponibles: {d['cupos_disponibles']}/{d['cupo_maximo']}"))
        layout.addWidget(QtWidgets.QLabel(f"Costo: {d['costo']}"))

        layout.addWidget(QtWidgets.QLabel("Descripción:"))
        txt_desc = QtWidgets.QTextEdit()
        txt_desc.setReadOnly(True)
        txt_desc.setPlainText(d["descripcion"] or "Sin descripción.")
        txt_desc.setMaximumHeight(120)
        layout.addWidget(txt_desc)

        btns = QtWidgets.QHBoxLayout()

        # Botón según el modo
        if self.mode == "view":
            btn_action = QtWidgets.QPushButton("✅ Registrarme al evento")
            btn_action.clicked.connect(self.on_register_clicked)
        elif self.mode == "delete":
            btn_action = QtWidgets.QPushButton("🗑️ Eliminar Evento")
            btn_action.setObjectName("deleteButton")
            btn_action.clicked.connect(self.on_delete_clicked)
        elif self.mode == "cancel":
            btn_action = QtWidgets.QPushButton("❌ Cancelar Asistencia")
            btn_action.setObjectName("deleteButton")
            btn_action.clicked.connect(self.on_cancel_attendance_clicked)

        btn_close = QtWidgets.QPushButton("Cerrar")
        btn_close.setObjectName("ghostButton")
        btn_close.clicked.connect(self.close)

        btns.addWidget(btn_action)
        btns.addWidget(btn_close)

        layout.addLayout(btns)

    def on_register_clicked(self):
        """Registrarse a un evento"""
        try:
            dao = ReservaDAO()
            result = dao.crear_reserva(self.id_usuario_logueado, self.event_data["id_evento"])

            if result[0][1] == 'Success':
                QtWidgets.QMessageBox.information(
                    self, "Registro Exitoso",
                    "¡Te has registrado al evento! 🎉"
                )
                self.register_requested.emit(self.event_data["id_evento"])
                self.close()
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Error",
                    result[0][1]
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Error",
                f"Error al registrar asistencia: {str(e)}"
            )

    def on_delete_clicked(self):
        """Eliminar evento creado por mí"""
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar el evento '{self.event_data['titulo']}'?\n\n"
            "⚠️ Esta acción es irreversible y eliminará todas las reservas asociadas.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                dao = EventoDAO()
                if dao.eliminar_evento(self.event_data["id_evento"]):
                    QtWidgets.QMessageBox.information(
                        self, "Evento Eliminado",
                        "El evento ha sido eliminado exitosamente."
                    )
                    self.event_deleted.emit()
                    self.close()
                else:
                    QtWidgets.QMessageBox.critical(
                        self, "Error",
                        "No se pudo eliminar el evento."
                    )
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Error",
                    f"Error al eliminar evento: {str(e)}"
                )

    def on_cancel_attendance_clicked(self):
        """Cancelar mi asistencia a un evento"""
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirmar Cancelación",
            f"¿Estás seguro de cancelar tu asistencia al evento '{self.event_data['titulo']}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                dao = ReservaDAO()
                result = dao.cancelar_reserva(
                    self.event_data["id_reserva"],
                )

                if result == 'Success':
                    QtWidgets.QMessageBox.information(
                        self, "Asistencia Cancelada",
                        "Tu asistencia ha sido cancelada exitosamente."
                    )
                    self.attendance_cancelled.emit()
                    self.close()
                else:
                    QtWidgets.QMessageBox.critical(
                        self, "Error",
                        "No se pudo cancelar la asistencia."
                    )
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Error",
                    f"Error al cancelar asistencia: {str(e)}"
                )


# ===================== VENTANA PRINCIPAL CON BD =====================

class MainWindow(QtWidgets.QMainWindow):
    logout_requested = pyqtSignal()

    def __init__(self, id_usuario, nombre, email, descripcion, telefono):
        super().__init__()
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.descripcion = descripcion
        self.telefono = telefono

        self.setWindowTitle(f"Nodus - Eventos ({nombre})")
        self.resize(1100, 650)
        self.setup_ui()
        self.cargar_eventos_recomendados()
        self.cargar_mis_eventos()
        self.cargar_mis_asistencias()

    def setup_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 8)
        main_layout.setSpacing(12)

        # Top bar
        top_bar = QtWidgets.QHBoxLayout()

        lbl_logo = QtWidgets.QLabel("Nodus")
        font_logo = QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold)
        lbl_logo.setFont(font_logo)

        btn_create = QtWidgets.QPushButton("Crear Evento")
        btn_create.clicked.connect(self.open_new_event_dialog)

        btn_logout = QtWidgets.QPushButton("Cerrar Sesión")
        btn_logout.setObjectName("ghostButton")
        btn_logout.clicked.connect(self.logout_requested.emit)

        top_bar.addWidget(lbl_logo)
        top_bar.addStretch()
        top_bar.addWidget(btn_create)
        top_bar.addWidget(btn_logout)

        main_layout.addLayout(top_bar)

        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setSpacing(12)
        main_layout.addLayout(content_layout, 1)

        # Profile panel
        profile_panel = QtWidgets.QFrame()
        profile_panel.setStyleSheet("background-color: #11111B; border-radius: 12px;")
        profile_panel.setMinimumWidth(280)
        profile_panel.setMaximumWidth(320)

        profile_layout = QtWidgets.QVBoxLayout(profile_panel)
        profile_layout.setContentsMargins(12, 12, 12, 12)
        profile_layout.setSpacing(10)

        lbl_profile_title = QtWidgets.QLabel("Mi Perfil")
        font_profile_title = QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold)
        lbl_profile_title.setFont(font_profile_title)

        self.lbl_profile_name = QtWidgets.QLabel(self.nombre)
        self.lbl_profile_name.setStyleSheet("color: #C65BFF;")

        self.lbl_profile_email = QtWidgets.QLabel(self.email)
        self.lbl_profile_email.setStyleSheet("color: #B0B0B0; font-size: 9pt;")

        btn_logout_card = QtWidgets.QPushButton("Cerrar Sesión")
        btn_logout_card.setObjectName("ghostButton")
        btn_logout_card.setMinimumHeight(32)
        btn_logout_card.clicked.connect(self.logout_requested.emit)

        # Botón de refrescar
        btn_refresh = QtWidgets.QPushButton("🔄 Actualizar")
        btn_refresh.setObjectName("ghostButton")
        btn_refresh.setMinimumHeight(32)
        btn_refresh.setToolTip("Actualizar eventos y asistencias")
        btn_refresh.clicked.connect(self.refrescar_todo)

        profile_layout.addWidget(lbl_profile_title)
        profile_layout.addWidget(self.lbl_profile_name)
        profile_layout.addWidget(self.lbl_profile_email)
        profile_layout.addWidget(btn_logout_card)
        profile_layout.addWidget(btn_refresh)

        self.tabs_profile = QtWidgets.QTabWidget()
        self.tabs_profile.setDocumentMode(True)
        self.tabs_profile.setStyleSheet("""
            QTabWidget::pane { border: 0px; }
            QTabBar::tab {
                background: transparent;
                padding: 6px 10px;
                margin-right: 4px;
                color: #B0B0B0;
            }
            QTabBar::tab:selected {
                color: #FFFFFF;
                border-bottom: 2px solid #A020F0;
            }
        """)

        tab_created = QtWidgets.QWidget()
        tab_attend = QtWidgets.QWidget()

        layout_created = QtWidgets.QVBoxLayout(tab_created)
        layout_created.setContentsMargins(0, 6, 0, 0)
        layout_attend = QtWidgets.QVBoxLayout(tab_attend)
        layout_attend.setContentsMargins(0, 6, 0, 0)

        self.profile_events_list = QtWidgets.QListWidget()
        self.profile_events_list.itemDoubleClicked.connect(self.on_my_event_double_click)

        self.profile_attendance_list = QtWidgets.QListWidget()
        self.profile_attendance_list.itemDoubleClicked.connect(self.on_my_attendance_double_click)

        layout_created.addWidget(self.profile_events_list)
        layout_attend.addWidget(self.profile_attendance_list)

        self.tabs_profile.addTab(tab_created, "Mis Eventos")
        self.tabs_profile.addTab(tab_attend, "Mis Asistencias")

        profile_layout.addWidget(self.tabs_profile)

        content_layout.addWidget(profile_panel)

        # Right panel (eventos destacados)
        right_panel = QtWidgets.QFrame()
        right_panel.setStyleSheet("background-color: transparent;")
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)

        lbl_events = QtWidgets.QLabel("Todos los Eventos")
        lbl_events.setStyleSheet("font-size: 14pt; font-weight: 600;")
        right_layout.addWidget(lbl_events)

        self.events_list = QtWidgets.QListWidget()
        self.events_list.setSpacing(4)
        right_layout.addWidget(self.events_list, 1)

        content_layout.addWidget(right_panel, 1)

        status = QtWidgets.QStatusBar()
        status.showMessage(f"Sesión iniciada · {self.nombre}")
        self.setStatusBar(status)

    def cargar_eventos_recomendados(self):
        try:
            dao = EventoDAO()
            eventos = dao.todos_los_eventos()

            self.events_list.clear()

            for e in eventos:
                data = {
                    "id_evento": e[0],
                    "titulo": e[1],
                    "categoria": e[14],
                    "fecha": str(e[3]),
                    "hora_inicio": str(e[4])[:5],
                    "hora_fin": str(e[5])[:5] if e[5] else "",
                    "lugar": e[6],
                    "direccion": e[7],
                    "cupo_maximo": e[8],
                    "cupos_ocupados": e[9],
                    "cupos_disponibles": e[8] - e[9],
                    "costo": e[10],
                    "descripcion": e[11]
                }

                item = QtWidgets.QListWidgetItem()
                widget = EventItemWidget(data)
                item.setSizeHint(widget.sizeHint())
                self.events_list.addItem(item)
                self.events_list.setItemWidget(item, widget)
                widget.view_details.connect(self.show_event_details)

        except Exception as e:
            print(f"❌ Error cargando eventos: {e}")

    def cargar_mis_eventos(self):
        try:
            dao = UsuarioDAO()
            eventos = dao.eventos_creados_usuario(self.id_usuario)

            self.profile_events_list.clear()
            self.mis_eventos_data = []

            for e in eventos:
                data = {
                    "id_evento": e[0],
                    "titulo": e[1],
                    "categoria": e[12],
                    "fecha": str(e[3]),
                    "hora_inicio": str(e[4])[:5],
                    "hora_fin": str(e[5])[:5] if e[5] else "",
                    "lugar": e[6],
                    "direccion": e[7],
                    "cupo_maximo": e[8],
                    "cupos_ocupados": e[9],
                    "cupos_disponibles": e[8] - e[9],
                    "costo": e[10],
                    "descripcion": e[11]
                }

                self.mis_eventos_data.append(data)
                text = f"{data['categoria']} · {data['titulo']} · {data['fecha']}"
                self.profile_events_list.addItem(text)

        except Exception as e:
            print(f"❌ Error cargando mis eventos: {e}")

    def cargar_mis_asistencias(self):
        try:
            dao = UsuarioDAO()
            eventos = dao.eventos_asistiendo_usuario(self.id_usuario)

            self.profile_attendance_list.clear()
            self.mis_asistencias_data = []

            print(f"🔍 Debug: Eventos de asistencia para usuario {self.id_usuario}: {len(eventos)}")

            for e in eventos:
                data = {
                    "id_evento": e[0],
                    "titulo": e[1],
                    "categoria": e[14],
                    "fecha": str(e[3]),
                    "hora_inicio": str(e[4])[:5],
                    "hora_fin": str(e[5])[:5] if e[5] else "",
                    "lugar": e[6],
                    "direccion": e[7],
                    "cupo_maximo": e[8],
                    "cupos_ocupados": e[9],
                    "cupos_disponibles": e[8] - e[9],
                    "costo": e[10],
                    "descripcion": e[11],
                    "id_reserva": e[16]
                }

                self.mis_asistencias_data.append(data)
                text = f"{data['categoria']} · {data['titulo']} · {data['fecha']}"
                self.profile_attendance_list.addItem(text)

        except Exception as e:
            print(f"❌ Error cargando asistencias: {e}")

    def open_new_event_dialog(self):
        dlg = NewEventDialog(self.id_usuario, self)
        dlg.event_created.connect(self.on_event_created)
        dlg.exec_()

    def on_event_created(self):
        self.cargar_eventos_recomendados()
        self.cargar_mis_eventos()

    def show_event_details(self, data):
        """Mostrar evento normal para registrarse"""
        dlg = EventDetailsDialog(data, self.id_usuario, mode="view", parent=self)
        dlg.register_requested.connect(self.on_registered_to_event)
        dlg.exec_()

    def on_registered_to_event(self, id_evento):
        """Callback cuando se registra a un evento"""
        self.cargar_mis_asistencias()
        self.cargar_eventos_recomendados()
        self.statusBar().showMessage("✅ Registrado al evento exitosamente", 3000)

    def on_my_event_double_click(self, item):
        """Doble clic en MIS EVENTOS CREADOS -> Mostrar con opción de ELIMINAR"""
        idx = self.profile_events_list.row(item)
        if idx < len(self.mis_eventos_data):
            dlg = EventDetailsDialog(
                self.mis_eventos_data[idx], 
                self.id_usuario, 
                mode="delete",  # ← Modo eliminar
                parent=self
            )
            dlg.event_deleted.connect(self.on_event_deleted)
            dlg.exec_()

    def on_my_attendance_double_click(self, item):
        """Doble clic en MIS ASISTENCIAS -> Mostrar con opción de CANCELAR"""
        idx = self.profile_attendance_list.row(item)
        if idx < len(self.mis_asistencias_data):
            dlg = EventDetailsDialog(
                self.mis_asistencias_data[idx], 
                self.id_usuario, 
                mode="cancel",  # ← Modo cancelar
                parent=self
            )
            dlg.attendance_cancelled.connect(self.on_attendance_cancelled)
            dlg.exec_()

    def on_event_deleted(self):
        """Callback cuando se elimina un evento"""
        self.cargar_eventos_recomendados()
        self.cargar_mis_eventos()
        self.cargar_mis_asistencias()
        self.statusBar().showMessage("✅ Evento eliminado exitosamente", 3000)

    def on_attendance_cancelled(self):
        """Callback cuando se cancela una asistencia"""
        self.cargar_mis_asistencias()
        self.cargar_eventos_recomendados()
        self.statusBar().showMessage("✅ Asistencia cancelada exitosamente", 3000)

    def refrescar_todo(self):
        """Refresca todos los datos de la interfaz"""
        self.cargar_eventos_recomendados()
        self.cargar_mis_eventos()
        self.cargar_mis_asistencias()
        self.statusBar().showMessage("✅ Datos actualizados correctamente", 3000)


# ===================== CONTROLADOR DE LA APP =====================

class AppController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyleSheet(APP_STYLE)

        self.login = LoginWindow()
        self.register = RegisterWindow()
        self.main = None

        self.login.login_success.connect(self.show_main_from_login)
        self.login.register_requested.connect(self.show_register)

        self.register.register_success.connect(self.show_login_from_register)

    def show_login(self):
        if self.main:
            self.main.close()
        self.register.close()
        self.login.show()

    def show_register(self):
        self.login.close()
        if self.main:
            self.main.close()
        self.register.show()

    def show_login_from_register(self):
        self.register.close()
        self.login.show()

    def show_main_from_login(self, id_usuario, nombre, email, descripcion, telefono):
        self.login.close()
        self.main = MainWindow(id_usuario, nombre, email, descripcion, telefono)
        self.main.logout_requested.connect(self.show_login)
        self.main.show()

    def run(self):
        self.show_login()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = AppController()
    controller.run()