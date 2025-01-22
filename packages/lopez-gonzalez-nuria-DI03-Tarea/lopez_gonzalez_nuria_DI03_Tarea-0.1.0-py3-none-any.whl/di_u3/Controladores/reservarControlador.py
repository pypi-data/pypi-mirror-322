import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QMainWindow, QMessageBox,QInputDialog# type: ignore
from PySide6.QtWidgets import QApplication # type: ignore
from PySide6.QtCore import Qt, QDate,QTimer # type: ignore
from Vistas.reservar import Ui_nlgConfirmarReserva
from Conexion_BBDD.connectionBBDD import Connectionbd 
#from Controladores.modificarReservaControlador import ModificarReservaControlador
import sqlite3


class ReservarControlador(QMainWindow):
    """
    Interfaz 3 para gestionar las reservas
    Permite dar de alta una reserva, 
    asignado automaticamente al crear una reserva un localizador ID, 
    todo ello guardado en la base de datos
    """
    
    def __init__(self,salon_id=None,parent=None):
        """
        Inicializa la gestión de reservas
        Args: 
            salon_id (int, optional): ID del salon asociado en la base de datos, por defecto es None
            parent(QWidget, optional): Widget padre de la ventana, por defecto es None
        """
        super().__init__(parent)
        self.ui = Ui_nlgConfirmarReserva()
        self.ui.setupUi(self)

        #almacenar el salon_id recibido
        self.salon_id=salon_id
        
        # Inicializar la base de datos
        self.db_path = 'Conexion_BBDD/reservasHotel.sql'
        self.dbManager = Connectionbd(self.db_path)

        # Conectar botones a funciones
        self.ui.ButtonConfirmarReserva.clicked.connect(self.confirmar_reserva)
        self.ui.pushButtonVolver.clicked.connect(self.volver)
        #self.ui.pushButtonModificarReserva.clicked.connect(self.modificar_reserva)

        # Cargar los tipos en los comboboxes
        self.cargar_tipos_reserva()
        self.cargar_tipos_cocina()
    
        # Configuración predeterminada de fecha
        self.ui.dateEditReserva.setDate(QDate.currentDate())  
        self.ui.dateEditReserva.setMinimumDate(QDate.currentDate()) 
        self.ui.dateEditReserva.setDisplayFormat("dd-MM-yyyy")
        self.ui.dateEditReserva.setFocusPolicy(Qt.StrongFocus)  
        self.ui.dateEditReserva.setCalendarPopup(True)  # Muestra el calendario

        # Ocultar campos por defecto
        self.ui.labelNumJornadas.setVisible(False)
        self.ui.spinBoxNumHab.setVisible(False)
        self.ui.labelHabitacion.setVisible(False)
        self.ui.checkBoxHabitacion.setVisible(False)

        # Conectar señales
        self.ui.comboBoxTipoReserva.currentTextChanged.connect(self.on_tipo_reserva_changed)

   
    def cargar_tipos_reserva(self):
        """
        Carga los tipos de reserva desde la base de datos y los muestra en el ComboBox
        """
        try:
            conexion = sqlite3.connect(self.db_path)
            cursor = conexion.cursor()
            cursor.execute("SELECT tipo_reserva_id, nombre FROM tipos_reservas")  # Asegúrate de que la tabla sea correcta
            tipos_reserva = cursor.fetchall()

            #self.ui.comboBoxTipoReserva.clear()  # Limpiar el comboBox antes de llenarlo
            for tipo_reserva_id, nombre in tipos_reserva:
                self.ui.comboBoxTipoReserva.addItem(nombre, tipo_reserva_id)

            conexion.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los tipos de reserva: {e}")

    def cargar_tipos_cocina(self):
        """
        Carga los tipos de cocina desde la base de datos y los muestra en el ComboBox
        """
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
        Muestra u oculta campos adicionales según el tipo de reserva->nºjornadas y habitaciones
        Args:
            text(str): texto del tipo de reserva seleccionado
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

    def confirmar_reserva(self):
        """
        Guarda la reserva en la base de datos con los datos insertados 
        por el usuario
        """
        try:
            # Obtener los datos del formulario
            persona = self.ui.lineEditNombrePersona.text()
            telefono = self.ui.lineEditTlPersona.text()
            fecha = self.ui.dateEditReserva.date().toString("dd-MM-yyyy")
            salon_id = self.ui.comboBoxTipoReserva.currentData()
            tipo_cocina_id = self.ui.comboBoxTipoCocina.currentData()
            ocupacion = self.ui.lineEdit_2.text()
            tipo_reserva_id = self.ui.comboBoxTipoReserva.currentData()

            # Obtener valores de jornadas y habitaciones
            jornadas = self.ui.spinBoxNumHab.value() if self.ui.labelNumJornadas.isVisible() else 0
            habitaciones = 1 if self.ui.checkBoxHabitacion.isChecked() else 0

            # Validaciones
            if not persona or not telefono or not salon_id or not tipo_cocina_id or not ocupacion:
                QMessageBox.warning(self, "Error", "Todos los campos deben estar completos.")
                return

            if not ocupacion.isdigit():
                QMessageBox.warning(self, "Error", "El número de personas debe ser un valor numérico.")
                return

            # Conectar a la base de datos y guardar la reserva
            conexion = sqlite3.connect(self.db_path)
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO reservas (salon_id, persona, telefono, fecha, tipo_reserva_id, tipo_cocina_id, ocupacion, jornadas, habitaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (salon_id, persona, telefono, fecha, tipo_reserva_id, tipo_cocina_id, int(ocupacion), jornadas, habitaciones))

            conexion.commit()

            # Obtener el ID de la reserva recién insertada
            reserva_id = cursor.lastrowid
            self.ui.lineEdit_2.setText(str(reserva_id))  # Establecer el ID de la reserva en el QLineEdit

            self.ui.lineEdit_2.setReadOnly(True) #para que no pueda escribir sobre campo de id al registrarse

            QMessageBox.information(self, "Éxito", f"Reserva confirmada. Su localizador es {reserva_id}.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la reserva: {e}")
        finally:
            conexion.close()

    def volver(self):
        """
        Vuelve a la interfaz anterior (2)
        """
        self.close()  # Cierra la interfaz actual y vuelve a la anterior
       
    """
    def modificar_reserva(self):
        
        Abre la interfaz 4 (ModificarReservaControlador) al hacer clic en el botón "Modificar Reserva".
        Pide el ID de la reserva que se desea modificar.
     
        reserva_id , ok= QInputDialog.getInt(self, "Modificar Reserva", "Introduce el número de localizador:", 
                                             minValue=1)
     
     
        if ok:  # Si el usuario hace clic en OK
                # Verificar que el ID de reserva existe en la base de datos
            if self.verificar_reserva_existe(reserva_id):
                # Si la reserva existe, abrir la interfaz de modificación
                self.modificar_ventana = ModificarReservaControlador(reserva_id, self)
                self.modificar_ventana.show()  # Mostrar la interfaz de modificación
              
            else:
                # Si la reserva no existe, mostrar un mensaje de error
                QMessageBox.warning(self, "Error", "El número de localizador no existe.")"""
    
    def verificar_reserva_existe(self, reserva_id):
        """
        Verifica si el número de localizador existe en la base de datos.
        """
        try:
            conexion = sqlite3.connect(self.db_path)
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM reservas WHERE reserva_id = ?", (reserva_id,))
            existe = cursor.fetchone()[0] > 0
            conexion.close()
            return existe
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error al verificar el localizador: {e}")
            return False


if __name__ == "__main__":
    import sys
    app = QApplication([])
    ventana = ReservarControlador()
    ventana.show()  # Muestra la ventana
    app.exec()  # Inicia el ciclo de eventos
