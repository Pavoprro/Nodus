import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal

# ===================== ESTILO (PALETA NODUS) =====================

APP_STYLE = """
QWidget {
    background-color: #05050B;
    color: #FFFFFF;
    font-family: "Segoe UI", "Arial";
}

/* Labels */
QLabel {
    color: #FFFFFF;
}

/* Entradas de texto y similares */
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

/* Listas */
QListWidget {
    background-color: #11111B;
    border: 1px solid #2B2B3C;
    border-radius: 8px;
    padding: 4px;
}

/* Botones normales */
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

/* Botón "fantasma" morado */
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

/* GroupBox */
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

/* Status bar */
QStatusBar {
    background-color: #05050B;
    color: #B0B0B0;
}
"""


# ===================== LOGIN =====================

class LoginWindow(QtWidgets.QWidget):
    login_success = pyqtSignal()
    register_requested = pyqtSignal()

    def __init__(self):  # ← CORREGIDO
        super().__init__()
        self.setWindowTitle("Nodus - Iniciar Sesión")
        self.setFixedSize(420, 520)
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
        self.txt_mail = QtWidgets.QLineEdit()
        self.txt_mail.setPlaceholderText("usuario@ejemplo.com")

        lbl_pass = QtWidgets.QLabel("Contraseña")
        self.txt_pass = QtWidgets.QLineEdit()
        self.txt_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_pass.setPlaceholderText("••••••••••")

        form.addWidget(lbl_mail)
        form.addWidget(self.txt_mail)
        form.addWidget(lbl_pass)
        form.addWidget(self.txt_pass)

        layout.addLayout(form)

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
        self.login_success.emit()


# ===================== REGISTRO =====================

class RegisterWindow(QtWidgets.QWidget):
    register_success = pyqtSignal()

    def __init__(self):  # ← CORREGIDO
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
            self.lbl_error.setText("Completa todos los campos.")
            return

        if password != password2:
            self.lbl_error.setText("Las contraseñas no coinciden.")
            return

        self.register_success.emit()


# ===================== DIALOGO "CREAR NUEVO EVENTO" =====================

class NewEventDialog(QtWidgets.QDialog):
    event_created = pyqtSignal(dict)

    def __init__(self, parent=None):  # ← CORREGIDO
        super().__init__(parent)
        self.setWindowTitle("Crear Nuevo Evento")
        self.resize(900, 650)
        self.setMinimumSize(800, 550)
        self.setup_ui()

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

        self.time_start = QtWidgets.QTimeEdit(QtCore.QTime.currentTime())
        self.time_start.setMinimumHeight(32)

        self.time_end = QtWidgets.QTimeEdit(QtCore.QTime.currentTime())
        self.time_end.setMinimumHeight(32)

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
        self.spin_quota.setMinimum(0)
        self.spin_quota.setMaximum(100000)
        self.spin_quota.setValue(0)
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
            QtWidgets.QMessageBox.warning(
                self, "Categoría",
                "Selecciona una categoría para el evento."
            )
            return

        data = {
            "title": self.txt_title.text(),
            "description": self.txt_desc.toPlainText(),
            "category": selected_cat,
            "date": self.date_event.date(),
            "time_start": self.time_start.time(),
            "time_end": self.time_end.time(),
            "place": self.txt_place.text(),
            "address": self.txt_address.text(),
            "quota": self.spin_quota.value(),
            "cost": self.txt_cost.text(),
        }

        self.event_created.emit(data)
        self.accept()


# ===================== ITEM DE LISTA CON "VER DETALLES" =====================

class EventItemWidget(QtWidgets.QWidget):
    view_details = pyqtSignal(dict)

    def __init__(self, event_data, parent=None):  # ← CORREGIDO
        super().__init__(parent)
        self.event_data = event_data

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        date_str = event_data["date"].toString("dd MMM yyyy")
        summary = f"{event_data['category']} · {event_data['title']} · {date_str} · {event_data['quota']} cupos · {event_data['cost'] or 'Gratis'}"

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


# ===================== DIALOGO DE DETALLES DE EVENTO =====================

class EventDetailsDialog(QtWidgets.QDialog):
    register_requested = pyqtSignal(dict)

    def __init__(self, event_data, parent=None):  # ← CORREGIDO
        super().__init__(parent)
        self.setWindowTitle("Detalles del Evento")
        self.resize(600, 450)
        self.event_data = event_data
        self.setup_ui()

    def setup_ui(self):
        d = self.event_data

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QtWidgets.QLabel(d["title"])
        f = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold)
        title.setFont(f)
        layout.addWidget(title)

        cat_date = QtWidgets.QLabel(
            f"{d['category']} · {d['date'].toString('dd MMM yyyy')} · "
            f"{d['time_start'].toString('HH:mm')} - {d['time_end'].toString('HH:mm')}"
        )
        cat_date.setStyleSheet("color: #C65BFF;")
        layout.addWidget(cat_date)

        layout.addWidget(QtWidgets.QLabel(f"Lugar: {d['place'] or 'Sin especificar'}"))
        layout.addWidget(QtWidgets.QLabel(f"Dirección: {d['address'] or 'Sin especificar'}"))
        layout.addWidget(QtWidgets.QLabel(f"Cupos: {d['quota']}"))
        layout.addWidget(QtWidgets.QLabel(f"Costo: {d['cost'] or 'Gratis'}"))

        layout.addWidget(QtWidgets.QLabel("Descripción:"))
        txt_desc = QtWidgets.QTextEdit()
        txt_desc.setReadOnly(True)
        txt_desc.setPlainText(d["description"] or "Sin descripción.")
        layout.addWidget(txt_desc)

        btn_register = QtWidgets.QPushButton("Registrarme al evento")
        btn_register.clicked.connect(self.on_register_clicked)

        btn_close = QtWidgets.QPushButton("Cerrar")
        btn_close.setObjectName("ghostButton")
        btn_close.clicked.connect(self.close)

        btns = QtWidgets.QHBoxLayout()
        btns.addWidget(btn_register)
        btns.addWidget(btn_close)

        layout.addLayout(btns)

    def on_register_clicked(self):
        self.register_requested.emit(self.event_data)
        QtWidgets.QMessageBox.information(
            self, "Registro",
            "Te has registrado al evento."
        )


# ===================== VENTANA PRINCIPAL =====================

class MainWindow(QtWidgets.QMainWindow):
    logout_requested = pyqtSignal()

    def __init__(self):  # ← CORREGIDO
        super().__init__()
        self.setWindowTitle("Nodus - Eventos")
        self.resize(1100, 650)
        self.setup_ui()

    def setup_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 8)
        main_layout.setSpacing(12)

        top_bar = QtWidgets.QHBoxLayout()

        lbl_logo = QtWidgets.QLabel("Nodus")
        font_logo = QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold)
        lbl_logo.setFont(font_logo)

        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("Buscar eventos...")

        btn_create = QtWidgets.QPushButton("Crear Evento")
        btn_create.clicked.connect(self.open_new_event_dialog)

        btn_logout = QtWidgets.QPushButton("Cerrar Sesión")
        btn_logout.setObjectName("ghostButton")
        btn_logout.clicked.connect(self.logout_requested.emit)

        top_bar.addWidget(lbl_logo)
        top_bar.addSpacing(16)
        top_bar.addWidget(self.search_edit, 1)
        top_bar.addWidget(btn_create)
        top_bar.addWidget(btn_logout)

        main_layout.addLayout(top_bar)

        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setSpacing(12)
        main_layout.addLayout(content_layout, 1)

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

        self.lbl_profile_name = QtWidgets.QLabel("Usuario Nodus")
        self.lbl_profile_name.setStyleSheet("color: #C65BFF;")

        btn_logout_card = QtWidgets.QPushButton("Cerrar Sesión")
        btn_logout_card.setObjectName("ghostButton")
        btn_logout_card.setMinimumHeight(32)
        btn_logout_card.clicked.connect(self.logout_requested.emit)

        profile_layout.addWidget(lbl_profile_title)
        profile_layout.addWidget(self.lbl_profile_name)
        profile_layout.addWidget(btn_logout_card)

        self.tabs_profile = QtWidgets.QTabWidget()
        self.tabs_profile.setDocumentMode(True)
        self.tabs_profile.setTabPosition(QtWidgets.QTabWidget.North)
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
        self.profile_attendance_list = QtWidgets.QListWidget()

        layout_created.addWidget(self.profile_events_list)
        layout_attend.addWidget(self.profile_attendance_list)

        self.tabs_profile.addTab(tab_created, "Mis Eventos Creados")
        self.tabs_profile.addTab(tab_attend, "Mis Asistencias")

        profile_layout.addWidget(self.tabs_profile)
        profile_layout.addStretch()

        content_layout.addWidget(profile_panel)

        right_panel = QtWidgets.QFrame()
        right_panel.setStyleSheet("background-color: transparent;")
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)

        lbl_cat = QtWidgets.QLabel("Explorar por categorías")
        lbl_cat.setStyleSheet("color: #C65BFF; font-size: 10pt;")
        right_layout.addWidget(lbl_cat)

        cat_row = QtWidgets.QHBoxLayout()
        for name in ["Social", "Aprendizaje", "Natural", "Deportes", "Cultural", "Gaming"]:
            b = QtWidgets.QPushButton(name)
            b.setObjectName("ghostButton")
            b.setCheckable(True)
            cat_row.addWidget(b)
        cat_row.addStretch()
        right_layout.addLayout(cat_row)

        lbl_events = QtWidgets.QLabel("Eventos Destacados")
        lbl_events.setStyleSheet("font-size: 14pt; font-weight: 600;")
        right_layout.addWidget(lbl_events)

        self.events_list = QtWidgets.QListWidget()
        self.events_list.setSpacing(4)
        right_layout.addWidget(self.events_list, 1)

        content_layout.addWidget(right_panel, 1)

        status = QtWidgets.QStatusBar()
        status.showMessage("Sesión iniciada · Usuario demo")
        self.setStatusBar(status)

        self.populate_initial_events()

    def open_new_event_dialog(self):
        dlg = NewEventDialog(self)
        dlg.event_created.connect(self.add_event_from_dialog)
        dlg.exec_()

    def add_event_widget(self, data):
        item = QtWidgets.QListWidgetItem()
        widget = EventItemWidget(data)
        item.setSizeHint(widget.sizeHint())
        self.events_list.addItem(item)
        self.events_list.setItemWidget(item, widget)
        widget.view_details.connect(self.show_event_details)

    def add_event_from_dialog(self, data):
        self.add_event_widget(data)
        date_str = data["date"].toString("dd MMM yyyy")
        text = f"{data['category']} · {data['title']} · {date_str}"
        self.profile_events_list.addItem(text)

    def show_event_details(self, data):
        dlg = EventDetailsDialog(data, self)
        dlg.register_requested.connect(self.register_to_event)
        dlg.exec_()

    def register_to_event(self, data):
        date_str = data["date"].toString("dd MMM yyyy")
        text = f"{data['category']} · {data['title']} · {date_str}"
        existing = [self.profile_attendance_list.item(i).text()
                    for i in range(self.profile_attendance_list.count())]
        if text not in existing:
            self.profile_attendance_list.addItem(text)

    def populate_initial_events(self):
        today = QtCore.QDate.currentDate()
        t1 = QtCore.QTime(20, 30)
        t2 = QtCore.QTime(22, 0)

        events = [
            {
                "title": "Noche de Jazz en Vivo",
                "description": "Concierto íntimo de jazz con músicos locales.",
                "category": "Cultural",
                "date": today.addDays(5),
                "time_start": t1,
                "time_end": t2,
                "place": "Auditorio Principal",
                "address": "Campus Ibero León",
                "quota": 45,
                "cost": "$150",
            },
            {
                "title": "Taller de Python Básico",
                "description": "Aprende los fundamentos de Python con ejercicios prácticos.",
                "category": "Aprendizaje",
                "date": today.addDays(10),
                "time_start": QtCore.QTime(18, 0),
                "time_end": QtCore.QTime(20, 0),
                "place": "Sala de Cómputo",
                "address": "Edificio de Ingeniería",
                "quota": 20,
                "cost": "Gratis",
            },
            {
                "title": "Hiking en la Montaña",
                "description": "Caminata guiada por senderos naturales.",
                "category": "Natural",
                "date": today.addDays(15),
                "time_start": QtCore.QTime(7, 0),
                "time_end": QtCore.QTime(12, 0),
                "place": "Punto de reunión: Estacionamiento",
                "address": "Parque Metropolitano",
                "quota": 30,
                "cost": "$80",
            },
        ]

        for e in events:
            self.add_event_widget(e)


# ===================== CONTROLADOR DE LA APP =====================

class AppController:
    def __init__(self):  # ← CORREGIDO
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyleSheet(APP_STYLE)

        self.login = LoginWindow()
        self.register = RegisterWindow()
        self.main = MainWindow()

        self.login.login_success.connect(self.show_main_from_login)
        self.login.register_requested.connect(self.show_register)

        self.register.register_success.connect(self.show_main_from_register)

        self.main.logout_requested.connect(self.show_login)

    def show_login(self):
        self.register.close()
        self.main.close()
        self.login.show()

    def show_register(self):
        self.login.close()
        self.main.close()
        self.register.show()

    def show_main_from_login(self):
        self.login.close()
        self.main.show()

    def show_main_from_register(self):
        self.register.close()
        self.main.show()

    def run(self):
        self.show_login()
        sys.exit(self.app.exec_())


if __name__ == "__main__":  # ← CORREGIDO
    controller = AppController()
    controller.run()