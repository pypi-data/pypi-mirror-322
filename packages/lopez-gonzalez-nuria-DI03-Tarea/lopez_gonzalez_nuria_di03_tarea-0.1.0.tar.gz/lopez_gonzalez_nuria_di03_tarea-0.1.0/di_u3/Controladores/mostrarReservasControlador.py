import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Controladores.reservarControlador import ReservarControlador
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem # type: ignore
from PySide6.QtWidgets import QApplication # type: ignore
from Vistas.mostrarReservas import Ui_nlgReservas
#from Vistas.reservar import Ui_nlgConfirmarReserva
from Conexion_BBDD.connectionBBDD import Connectionbd # type: ignore
from Controladores.modificarReservaControlador import ModificarReservaControlador
import sqlite3


class MostrarReservasControlador(QMainWindow):

    """
        Interfaz 2, en la que se selecciona el tipo de salón que buscamos para reservas
        y celebrar un evento, si no se selecciona ningún tipo de salón no debe poder
        acceder a la interfaz 3 

        Métodos:
        cargarSalones():carga los salones que hay en la base de datos
        abrirReserva(): abrir la ventana 3
        cargarReservas(tipoSalon): carga reservas asociadas a cada tipo de salon seleccionado
        """

    def __init__(self, parent=None):

        """
        Inicializa la interfaz y configura la conexion con la base de datos
        cargando los tipos de salones y las reservas que tienen
        """
        
        super().__init__(parent)
        self.ui = Ui_nlgReservas()
        self.ui.setupUi(self)

        # Conectar los eventos con las funciones
        self.ui.pushButtonReserva.clicked.connect(self.abrirReserva)
        self.ui.comboBoxSalones.currentTextChanged.connect(self.cargarReservas)
        self.ui.pushButtonModificar.clicked.connect(self.modificar_reserva)

        # Iniciar la conexión con la BBDD
        self.db_path = "Conexion_BBDD/reservasHotel.sql"
        self.dbManager = Connectionbd(self.db_path)
       

        # Cargar los salones desde la base de datos
        self.cargarSalones()

        # Establecer el valor por defecto en el comboBox
        self.ui.comboBoxSalones.setCurrentIndex(0)  # Establece el primer ítem como seleccionado

    def cargarSalones(self):
        """
        carga los salones disponibles en la base de datos y añade al comboBox
        """
        
        # Realizar la consulta a la base de datos para obtener los salones
        salones= self.dbManager.get_salones()
        
        # Limpiar el comboBox antes de agregar nuevos datos
        self.ui.comboBoxSalones.clear()
        
        # Agregar un valor por defecto al comboBox
        self.ui.comboBoxSalones.addItem("Selecciona un salón")
        
        # Agregar los salones obtenidos de la base de datos
        for salon_id, salon_nombre in salones:
            self.ui.comboBoxSalones.addItem(salon_nombre, salon_id)
        
    
    def abrirReserva(self):
        """
        Abrir la interfaz de reserva (Ventana 3) pero verifica antes que se haya seleccionado
        un salón de los que hay en la base de datos
        """
        # Verificar que haya 1 salón seleccionado
        salon_id = self.ui.comboBoxSalones.currentData()  # Obtiene el salon_id, no solo el texto
        tipoSalon = self.ui.comboBoxSalones.currentText()

        if tipoSalon == "Selecciona un salón":
            QMessageBox.warning(self, 
                "Advertencia",
                "Debes seleccionar un salón para la reserva."
            )
            return  # Salir si no hay salón seleccionado

        # Para abrir la ventana de reserva y pasar el el salon_id
        self.ventana3=ReservarControlador(salon_id=salon_id)
        self.ventana3.show()


    def cargarReservas(self, tipoSalon):
        """
        Carga las reservas que hay en la base de datos asociadas a cada tipo de salon
        """
       
        # Vaciar la tabla para cargar los nuevos datos
        self.ui.tableWidget.setRowCount(0)

        # Verificar que no se cargue nada si el usuario no selecciona un salón válido
        if tipoSalon == "Selecciona un salón":
            return

        # Limpiar espacios en blanco extra antes de hacer la consulta
        tipoSalon = tipoSalon.strip()
        print(f"Consultando reservas para el salón: '{tipoSalon}'")

         # Crear una instancia de la clase Connectionbd y obtener las reservas para el salón seleccionado
        conexion_bd = Connectionbd(self.db_path)  # Suponiendo que self.db_path es la ubicación de la base de datos
        reservas = conexion_bd.get_reservasSalon(tipoSalon)
        print(f"Reservas encontradas: {len(reservas)}")

        # Comprobamos si no se encontraron reservas
        if not reservas:
            print(f"No se encontraron reservas para el salón: {tipoSalon}")
            return  # No se hace nada si no hay resultados

        # Configurar el número de columnas de la tabla a 4 (para las 4 columnas que vamos a mostrar)
        self.ui.tableWidget.setColumnCount(5)#una columna de + para ocultar id

        # Agregar cada reserva a la tabla
        for row_number, row_data in enumerate(reservas):
            self.ui.tableWidget.insertRow(row_number)
          
            

              # Extraer los datos de la reserva
            reserva_id = row_data [0] # Si tienes un ID real, usa ese valor aquí
            fecha = row_data[1]  # Suponiendo que 'fecha' es la primera columna en la consulta
            persona = row_data[2]  # Suponiendo que 'persona' es la segunda columna
            telefono = row_data[3]  # Suponiendo que 'telefono' es la tercera columna
            tipo_reserva_id = row_data[4]  # Suponiendo que 'tipo_reserva_id' es la cuarta columna

            # Insertar el valor del reserva_id en la primera columna (ahora visible)
            self.ui.tableWidget.setItem(row_number, 0, QTableWidgetItem(str(reserva_id)))

            # Insertar el valor de la fecha en la segunda columna
            self.ui.tableWidget.setItem(row_number, 1, QTableWidgetItem(str(fecha)))
            # Insertar el valor de la persona en la tercera columna
            self.ui.tableWidget.setItem(row_number, 2, QTableWidgetItem(str(persona)))
            # Insertar el valor del teléfono en la cuarta columna
            self.ui.tableWidget.setItem(row_number, 3, QTableWidgetItem(str(telefono)))
            # Insertar el valor del tipo de reserva en la quinta columna
            self.ui.tableWidget.setItem(row_number, 4, QTableWidgetItem(str(tipo_reserva_id)))   
            
        # Configurar los encabezados de las columnas (solo una vez)
        self.ui.tableWidget.setHorizontalHeaderLabels(["ID","Fecha", "Persona", "Teléfono", "Tipo Reserva"])

        # Ocultar la columna del ID
       # self.ui.tableWidget.setColumnHidden(0, True)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.ui.tableWidget.resizeColumnsToContents()

            
        # Forzar actualización de la tabla
       # self.ui.tableWidget.repaint() 

    def modificar_reserva(self):
        """
        Abre la interfaz 4 (ModificarReservaControlador) al hacer clic en el botón "Modificar Reserva".
        Hay que seleccionar un dato de la fila que se desea modificar.
     """
       
         # Obtener la fila seleccionada
        row = self.ui.tableWidget.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una reserva para modificar.")
            return

         # Obtener el reserva_id desde la fila seleccionada (este es el valor oculto en la tabla)
        reserva_id = self.ui.tableWidget.item(row, 0) 
        if not reserva_id:
            QMessageBox.critical(self, "Error", "No se pudo obtener el ID de la reserva seleccionada.")
            return
        reserva_id=reserva_id.text()
        print(f"ID de la reserva seleccionada: {reserva_id}")

        # Ahora obtenemos todos los datos completos de la reserva usando reserva_id
        try:
            conexion = sqlite3.connect(self.db_path)
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT persona, telefono, fecha, tipo_reserva_id, tipo_cocina_id, ocupacion, jornadas, habitaciones
                FROM reservas
                WHERE reserva_id = ?
            """, (reserva_id,))

            datos_reserva = cursor.fetchone()
            #conexion.close()

            if  datos_reserva:
                 # Ahora pasamos los datos completos a la ventana de modificación
                persona, telefono, fecha, tipo_reserva_id, tipo_cocina_id, ocupacion, jornadas, habitaciones = datos_reserva
            else:
                QMessageBox.warning(self, "Error", "No se encontró la reserva con ese ID.")
                return

           
            # Crear una instancia de la ventana de modificación y pasarle los datos
            datos_completos = {
                "persona": persona,
                "telefono": telefono,
                "fecha": fecha,
                "tipo_reserva_id": tipo_reserva_id,
                "tipo_cocina_id": tipo_cocina_id,
                "ocupacion": ocupacion,
                "jornadas": jornadas,
                "habitaciones": habitaciones
            }

            self.ventana4 = ModificarReservaControlador(datos_reserva=datos_completos, reserva_id=reserva_id)
            self.ventana4.show()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los datos de la reserva: {e}")

    def obtener_datos_reserva(self, reserva_id):
        """
        Obtiene los datos completos de una reserva usando su ID.
        """
        try:
            conexion = sqlite3.connect(self.db_path)
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT persona, telefono, fecha, tipo_reserva_id, tipo_cocina_id, ocupacion, jornadas, habitaciones
                FROM reservas
                WHERE reserva_id = ?
                ORDER BY fecha DESC
            """, (reserva_id,))

            # Obtener los resultados
            datos_reserva = cursor.fetchone()

            conexion.close()

            # Si no se encontró la reserva, devolver None
            if not datos_reserva:
                return None

            return datos_reserva

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo obtener los datos de la reserva: {e}")
            return None

    
if __name__ == "__main__":
    import sys
    app = QApplication([])
    ventana = MostrarReservasControlador()
    ventana.show()
    app.exec()

