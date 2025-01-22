# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reservarNIzQvg.ui'
##
## Created by: Qt User Interface Compiler version 5.15.13
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale, # type: ignore
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, # type: ignore
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit, # type: ignore
    QFrame, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpinBox, QStatusBar,
    QWidget)


class Ui_nlgConfirmarReserva(object):
    def setupUi(self, nlgConfirmarReserva):
        if not nlgConfirmarReserva.objectName():
            nlgConfirmarReserva.setObjectName(u"nlgConfirmarReserva")
        nlgConfirmarReserva.setWindowModality(Qt.ApplicationModal)
        nlgConfirmarReserva.resize(963, 811)
        nlgConfirmarReserva.setStyleSheet(u"background-color: rgb(239, 227, 208);")
        self.centralwidget = QWidget(nlgConfirmarReserva)
        self.centralwidget.setObjectName(u"centralwidget")
        self.labelNombrePersona = QLabel(self.centralwidget)
        self.labelNombrePersona.setObjectName(u"labelNombrePersona")
        self.labelNombrePersona.setGeometry(QRect(30, 70, 131, 19))
        self.lineEditNombrePersona = QLineEdit(self.centralwidget)
        self.lineEditNombrePersona.setObjectName(u"lineEditNombrePersona")
        self.lineEditNombrePersona.setGeometry(QRect(170, 60, 221, 27))
        self.lineEditNombrePersona.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.labelTlPersona = QLabel(self.centralwidget)
        self.labelTlPersona.setObjectName(u"labelTlPersona")
        self.labelTlPersona.setGeometry(QRect(30, 110, 66, 19))
        self.lineEditTlPersona = QLineEdit(self.centralwidget)
        self.lineEditTlPersona.setObjectName(u"lineEditTlPersona")
        self.lineEditTlPersona.setGeometry(QRect(170, 110, 221, 27))
        self.lineEditTlPersona.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.labelFechaReserva = QLabel(self.centralwidget)
        self.labelFechaReserva.setObjectName(u"labelFechaReserva")
        self.labelFechaReserva.setGeometry(QRect(30, 150, 111, 31))
        self.labelFechaReserva.setFrameShape(QFrame.NoFrame)
        self.dateEditReserva = QDateEdit(self.centralwidget)
        self.dateEditReserva.setObjectName(u"dateEditReserva")
        self.dateEditReserva.setGeometry(QRect(170, 150, 110, 31))
        self.labeltipoReserva = QLabel(self.centralwidget)
        self.labeltipoReserva.setObjectName(u"labeltipoReserva")
        self.labeltipoReserva.setGeometry(QRect(30, 200, 111, 19))
        self.labelNpersonas = QLabel(self.centralwidget)
        self.labelNpersonas.setObjectName(u"labelNpersonas")
        self.labelNpersonas.setGeometry(QRect(30, 250, 111, 19))
        self.labelTipoCocina = QLabel(self.centralwidget)
        self.labelTipoCocina.setObjectName(u"labelTipoCocina")
        self.labelTipoCocina.setGeometry(QRect(30, 290, 101, 19))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(170, 250, 111, 27))
        self.lineEdit_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.ButtonConfirmarReserva = QPushButton(self.centralwidget)
        self.ButtonConfirmarReserva.setObjectName(u"ButtonConfirmarReserva")
        self.ButtonConfirmarReserva.setGeometry(QRect(220, 350, 151, 31))
        self.ButtonConfirmarReserva.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"font-weight:bold;")
        self.comboBoxTipoReserva = QComboBox(self.centralwidget)
        self.comboBoxTipoReserva.setObjectName(u"comboBoxTipoReserva")
        self.comboBoxTipoReserva.setGeometry(QRect(170, 200, 111, 27))
        self.comboBoxTipoCocina = QComboBox(self.centralwidget)
        self.comboBoxTipoCocina.setObjectName(u"comboBoxTipoCocina")
        self.comboBoxTipoCocina.setGeometry(QRect(170, 290, 111, 27))
        self.pushButtonVolver = QPushButton(self.centralwidget)
        self.pushButtonVolver.setObjectName(u"pushButtonVolver")
        self.pushButtonVolver.setGeometry(QRect(420, 350, 88, 31))
        self.pushButtonVolver.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.labelNumJornadas = QLabel(self.centralwidget)
        self.labelNumJornadas.setObjectName(u"labelNumJornadas")
        self.labelNumJornadas.setGeometry(QRect(310, 190, 81, 19))
        self.labelHabitacion = QLabel(self.centralwidget)
        self.labelHabitacion.setObjectName(u"labelHabitacion")
        self.labelHabitacion.setGeometry(QRect(310, 220, 141, 19))
        self.spinBoxNumHab = QSpinBox(self.centralwidget)
        self.spinBoxNumHab.setObjectName(u"spinBoxNumHab")
        self.spinBoxNumHab.setGeometry(QRect(460, 180, 44, 28))
        self.checkBoxHabitacion = QCheckBox(self.centralwidget)
        self.checkBoxHabitacion.setObjectName(u"checkBoxHabitacion")
        self.checkBoxHabitacion.setGeometry(QRect(460, 220, 41, 21))
        self.checkBoxHabitacion.setStyleSheet(u"")
        self.pushButtonModificarReserva = QPushButton(self.centralwidget)
        self.pushButtonModificarReserva.setObjectName(u"pushButtonModificarReserva")
        self.pushButtonModificarReserva.setGeometry(QRect(40, 350, 131, 31))
        self.pushButtonModificarReserva.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        nlgConfirmarReserva.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(nlgConfirmarReserva)
        self.statusbar.setObjectName(u"statusbar")
        nlgConfirmarReserva.setStatusBar(self.statusbar)

        self.retranslateUi(nlgConfirmarReserva)

        QMetaObject.connectSlotsByName(nlgConfirmarReserva)
    # setupUi

    def retranslateUi(self, nlgConfirmarReserva):
        nlgConfirmarReserva.setWindowTitle(QCoreApplication.translate("nlgConfirmarReserva", u"MainWindow", None))
        self.labelNombrePersona.setText(QCoreApplication.translate("nlgConfirmarReserva", u"Nombre y apellidos", None))
        self.labelTlPersona.setText(QCoreApplication.translate("nlgConfirmarReserva", u"Tel\u00e9fono", None))
        self.labelFechaReserva.setText(QCoreApplication.translate("nlgConfirmarReserva", u"Fecha Reserva", None))
        self.labeltipoReserva.setText(QCoreApplication.translate("nlgConfirmarReserva", u"Tipo de reserva", None))
        self.labelNpersonas.setText(QCoreApplication.translate("nlgConfirmarReserva", u"N\u00ba de personas", None))
        self.labelTipoCocina.setText(QCoreApplication.translate("nlgConfirmarReserva", u"Tipo de cocina", None))
        self.ButtonConfirmarReserva.setText(QCoreApplication.translate("nlgConfirmarReserva", u"Confirmar Reserva", None))
        self.pushButtonVolver.setText(QCoreApplication.translate("nlgConfirmarReserva", u"Volver", None))
        self.labelNumJornadas.setText(QCoreApplication.translate("nlgConfirmarReserva", u"N\u00ba jornadas", None))
        self.labelHabitacion.setText(QCoreApplication.translate("nlgConfirmarReserva", u"Necesita habitaci\u00f3n", None))
        self.checkBoxHabitacion.setText("")
        self.pushButtonModificarReserva.setText(QCoreApplication.translate("nlgConfirmarReserva", u"Modificar Reserva", None))
    # retranslateUi

