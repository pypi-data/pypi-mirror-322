import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Vistas')))

from PySide6 import QtWidgets  # type: ignore
from Vistas.miHotel import Ui_nlgMainWindow
from Controladores.mostrarReservasControlador import MostrarReservasControlador

class MainWindow(QtWidgets.QMainWindow):
    """
    Clase Main que corresponde a la ventana principal de la aplicación
    """
    def __init__(self):
        """
        Constructor de la clase Main, inicializa la interfaz gráfica 
        principal, conecta el botón de abrir la reservas con la función
        de abrir()
        """
        super().__init__()
        self.ui = Ui_nlgMainWindow()
        self.ui.setupUi(self)

        #conectar el botón de mostrarReservas con la función abrir()
        self.ui.buttonMostrarReserva.clicked.connect(self.abrir)
        self.ventana2=None

    def abrir(self):
        """
        método para abrir la interfaz 2 de mostrarReservasControlador

        """
        self.ventana2=MostrarReservasControlador()
        self.ventana2.show()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana=MainWindow ()
    ventana.show()
    sys.exit(app.exec())
