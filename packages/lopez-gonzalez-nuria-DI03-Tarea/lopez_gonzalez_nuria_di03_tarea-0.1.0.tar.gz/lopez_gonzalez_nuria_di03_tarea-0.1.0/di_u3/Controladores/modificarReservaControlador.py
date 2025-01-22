import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QMainWindow, QMessageBox# type: ignore
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton, QCheckBox, QMessageBox
from PySide6.QtCore import Qt,QDate
from PySide6.QtWidgets import QApplication # type: ignore
from Vistas.modificarReserva import Ui_nlgModificarReserva
from Conexion_BBDD.connectionBBDD import Connectionbd
import sqlite3

class ModificarReservaControlador(QMainWindow):
    """
    Interfaz 4 para modificar una reserva.
    Permite cargar y modificar una reserva existente a partir de un ID.
    """


    def __init__(self, datos_reserva,reserva_id, parent=None):
        """
        Inicializa la interfaz de modificación de reserva
       
        """
        super().__init__(parent)
        self.ui = Ui_nlgModificarReserva()
        self.ui.setupUi(self)

        # Guardamos los datos de la reserva a modificar
        self.datos_reserva = datos_reserva

        # Guardar el ID de la reserva a modificar
        self.reserva_id = reserva_id

        self.db_path = 'Conexion_BBDD/reservasHotel.sql'
        #self.dbManager = Connectionbd(self.db_path)

         # Cargar tipos de datos en combo boxes
        self.cargar_tipos_reserva()
        self.cargar_tipos_cocina()

        # Cargar los datos de la reserva
        self.cargar_datos_reserva()
        

        # Conectar botones a funciones
        self.ui.ButtonConfirmarModificacion.clicked.connect(self.modificar_reserva)
        self.ui.comboBoxTipoReserva.currentTextChanged.connect(self.on_tipo_reserva_changed)
        self.ui.pushButtonVolver.clicked.connect(self.volver)

        # Configuración predeterminada de fecha
        self.ui.dateEditReserva.setDate(QDate.currentDate())  
        self.ui.dateEditReserva.setMinimumDate(QDate.currentDate()) 
        self.ui.dateEditReserva.setDisplayFormat("dd-MM-yyyy")
        self.ui.dateEditReserva.setCalendarPopup(True)  # Muestra el calendario

        # Ocultar campos por defecto
        self.ui.labelNumJornadas.setVisible(False)
        self.ui.spinBoxNumHab.setVisible(False)
        self.ui.labelHabitacion.setVisible(False)
        self.ui.checkBoxHabitacion.setVisible(False)

        # Conectar señales
        self.ui.comboBoxTipoReserva.currentTextChanged.connect(self.on_tipo_reserva_changed)
       
    def cargar_tipos_reserva(self):
        try:
            conexion = sqlite3.connect(self.db_path)
            cursor = conexion.cursor()
            cursor.execute("SELECT tipo_reserva_id, nombre FROM tipos_reservas")
            tipos_reserva = cursor.fetchall()

            for tipo_reserva_id, nombre in tipos_reserva:
                self.ui.comboBoxTipoReserva.addItem(nombre, tipo_reserva_id)

            conexion.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los tipos de reserva: {e}")

    def cargar_tipos_cocina(self):
        try:
            conexion = sqlite3.connect(self.db_path)
            cursor = conexion.cursor()
            cursor.execute("SELECT tipo_cocina_id, nombre FROM tipos_cocina")
            tipos_cocina = cursor.fetchall()

            for tipo_cocina_id, nombre in tipos_cocina:
                self.ui.comboBoxTipoCocina.addItem(nombre, tipo_cocina_id)

            conexion.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los tipos de cocina: {e}")

    def on_tipo_reserva_changed(self, text):
        """
        Muestra u oculta campos adicionales según el tipo de reserva.
        """
        if text == "Congreso":
            self.ui.labelNumJornadas.setVisible(True)
            self.ui.spinBoxNumHab.setVisible(True)
            self.ui.labelHabitacion.setVisible(True)
            self.ui.checkBoxHabitacion.setVisible(True)
        else:
            self.ui.labelNumJornadas.setVisible(False)
            self.ui.spinBoxNumHab.setVisible(False)
            self.ui.labelHabitacion.setVisible(False)
            self.ui.checkBoxHabitacion.setVisible(False)

    def cargar_datos_reserva(self):
        """
        Carga los datos de la reserva a modificar desde los datos pasados al constructor
        """      
        persona = self.datos_reserva["persona"]
        telefono = self.datos_reserva["telefono"]
        fecha = self.datos_reserva["fecha"]
        tipo_reserva_id = self.datos_reserva["tipo_reserva_id"]
        tipo_cocina_id = self.datos_reserva["tipo_cocina_id"]
        ocupacion = self.datos_reserva["ocupacion"]
        jornadas = self.datos_reserva["jornadas"]
        habitaciones = self.datos_reserva["habitaciones"]

        # Llenar los campos de la interfaz con los datos de la reserva
        self.ui.lineEditNombrePersona.setText(persona)
        self.ui.lineEditNombrePersona.setEnabled(True)
        self.ui.lineEditTlPersona.setText(telefono)
        self.ui.lineEditTlPersona.setEnabled(True)
        self.ui.dateEditReserva.setDate(QDate.fromString(fecha, "dd-MM-yyyy"))
        self.ui.comboBoxTipoReserva.setCurrentIndex(self.ui.comboBoxTipoReserva.findData(tipo_reserva_id))
        self.ui.comboBoxTipoCocina.setCurrentIndex(self.ui.comboBoxTipoCocina.findData(tipo_cocina_id))
        self.ui.lineEdit_2.setText(str(ocupacion))
        self.ui.lineEdit_2.setEnabled(True)

        if tipo_reserva_id == "Congreso":  # Si el tipo de reserva es "Congreso"
            self.ui.spinBoxNumHab.setValue(jornadas)
            self.ui.spinBoxNumHab.setEnabled(True)
            self.ui.checkBoxHabitacion.setChecked(habitaciones == 1)
            self.ui.checkBoxHabitacion.setEnabled(True)
                    
        else:
                    
            self.ui.spinBoxNumHab.setVisible(False)    
            self.ui.checkBoxHabitacion.setVisible(False)
    

    def modificar_reserva(self):
        """
        Modifica la reserva en la BBDD con los nuevos datos
        """

        try:

            conexion = sqlite3.connect(self.db_path)
            cursor = conexion.cursor()

            persona = self.ui.lineEditNombrePersona.text()
            telefono = self.ui.lineEditTlPersona.text()
            fecha = self.ui.dateEditReserva.date().toString("dd-MM-yyyy")
            tipo_reserva_id = self.ui.comboBoxTipoReserva.currentData()
            tipo_cocina_id = self.ui.comboBoxTipoCocina.currentData()
            ocupacion = self.ui.lineEdit_2.text()

            # Obtener valores de jornadas y habitaciones
            jornadas = self.ui.spinBoxNumHab.value() if self.ui.labelNumJornadas.isVisible() else 0
            habitaciones = 1 if self.ui.checkBoxHabitacion.isChecked() else 0

            # Validaciones
            if not persona or not telefono or not tipo_reserva_id or not tipo_cocina_id or not ocupacion:
                QMessageBox.warning(self, "Error", "Todos los campos deben estar completos.")
                return

            if not ocupacion.isdigit():
                QMessageBox.warning(self, "Error", "El número de personas debe ser un valor numérico.")
                return

            
            cursor.execute("""
                UPDATE reservas
                SET persona = ?, telefono = ?, fecha = ?, tipo_reserva_id = ?, tipo_cocina_id = ?, ocupacion = ?, jornadas = ?, habitaciones = ?
                WHERE reserva_id = ?
            """, (persona, telefono, fecha, tipo_reserva_id, tipo_cocina_id, int(ocupacion), jornadas, habitaciones, self.reserva_id))

            conexion.commit()
            conexion.close()

            QMessageBox.information(self, "Éxito", f"Reserva {self.reserva_id} modificada con éxito.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo modificar la reserva: {e}")

    def volver(self):
        """
        Cierra la interfaz actual y vuelve a la interfaz anterior
        """
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication([])

     # Diccionario con los datos de la reserva a modificar
    datos_reserva = {
        "reserva_id": 1,
        "persona": "Juan Pérez",
        "telefono": "123456789",
        "fecha": "01-01-2025",
        "tipo_reserva_id": 1,
        "tipo_cocina_id": 2,
        "ocupacion": 2,
        "jornadas": 3,
        "habitaciones": 1
    }
    ventana = ModificarReservaControlador(datos_reserva=datos_reserva)
    ventana.show()  # Muestra la ventana
    app.exec()  # Inicia el ciclo de eventos

