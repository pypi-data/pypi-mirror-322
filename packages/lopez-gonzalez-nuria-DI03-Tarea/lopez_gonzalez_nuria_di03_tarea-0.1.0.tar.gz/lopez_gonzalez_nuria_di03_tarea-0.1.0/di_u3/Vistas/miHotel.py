# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'miHotel.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow, # type: ignore
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_nlgMainWindow(object):
    def setupUi(self, nlgMainWindow):
        if not nlgMainWindow.objectName():
            nlgMainWindow.setObjectName(u"nlgMainWindow")
        nlgMainWindow.setWindowModality(Qt.WindowModal)
        nlgMainWindow.resize(559, 598)
        font = QFont()
        font.setFamilies([u"URW Bookman"])
        font.setBold(True)
        font.setItalic(True)
        nlgMainWindow.setFont(font)
        nlgMainWindow.setStyleSheet(u"background-color: rgb(239, 227, 208);")
        self.centralwidget = QWidget(nlgMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.nlgHabitaciones = QLineEdit(self.centralwidget)
        self.nlgHabitaciones.setObjectName(u"nlgHabitaciones")
        self.nlgHabitaciones.setGeometry(QRect(150, 80, 101, 31))
        font1 = QFont()
        font1.setFamilies([u"C059"])
        font1.setBold(False)
        font1.setItalic(False)
        self.nlgHabitaciones.setFont(font1)
        self.nlgHabitaciones.setFrame(False)
        self.nlgMenuPrincipal = QLineEdit(self.centralwidget)
        self.nlgMenuPrincipal.setObjectName(u"nlgMenuPrincipal")
        self.nlgMenuPrincipal.setGeometry(QRect(20, 80, 121, 31))
        self.nlgMenuPrincipal.setFont(font1)
        self.nlgMenuPrincipal.setFrame(False)
        self.nlgSalones = QPushButton(self.centralwidget)
        self.nlgSalones.setObjectName(u"nlgSalones")
        self.nlgSalones.setGeometry(QRect(270, 80, 88, 31))
        self.nlgSalones.setFont(font1)
        self.buttonMostrarReserva = QPushButton(self.centralwidget)
        self.buttonMostrarReserva.setObjectName(u"buttonMostrarReserva")
        self.buttonMostrarReserva.setGeometry(QRect(370, 80, 161, 31))
        font2 = QFont()
        font2.setFamilies([u"C059"])
        font2.setBold(True)
        font2.setItalic(True)
        self.buttonMostrarReserva.setFont(font2)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 0, 66, 71))
        self.label.setPixmap(QPixmap(u"Imagenes/LogoHotel.png"))
        self.label.setScaledContents(True)
        self.nlgFotoHotel = QLabel(self.centralwidget)
        self.nlgFotoHotel.setObjectName(u"nlgFotoHotel")
        self.nlgFotoHotel.setGeometry(QRect(30, 140, 501, 311))
        self.nlgFotoHotel.setPixmap(QPixmap(u"Imagenes/salon1.png"))
        self.nlgFotoHotel.setScaledContents(True)
        self.nlgMiHotel = QLineEdit(self.centralwidget)
        self.nlgMiHotel.setObjectName(u"nlgMiHotel")
        self.nlgMiHotel.setGeometry(QRect(170, 10, 261, 51))
        font3 = QFont()
        font3.setFamilies([u"Sans"])
        font3.setBold(True)
        font3.setItalic(False)
        self.nlgMiHotel.setFont(font3)
        self.nlgMiHotel.setStyleSheet(u"color: rgb(99, 69, 44);\n"
"font-size:40px;\n"
"\n"
"")
        self.nlgMiHotel.setFrame(False)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(490, 20, 31, 31))
        self.label_5.setPixmap(QPixmap(u"Imagenes/key1.png"))
        self.label_5.setScaledContents(True)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 480, 511, 111))
        self.widget.setStyleSheet(u"background-color: rgb(181, 131, 90);")
        self.labelTituloContacto = QLabel(self.widget)
        self.labelTituloContacto.setObjectName(u"labelTituloContacto")
        self.labelTituloContacto.setGeometry(QRect(20, 10, 161, 19))
        self.labelTituloContacto.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.labelLocalizacion = QLabel(self.widget)
        self.labelLocalizacion.setObjectName(u"labelLocalizacion")
        self.labelLocalizacion.setGeometry(QRect(20, 40, 381, 21))
        self.labelTl = QLabel(self.widget)
        self.labelTl.setObjectName(u"labelTl")
        self.labelTl.setGeometry(QRect(20, 70, 161, 19))
        self.labelTl.setStyleSheet(u"color: rgb(246, 245, 244);")
        nlgMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(nlgMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        nlgMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(nlgMainWindow)

        QMetaObject.connectSlotsByName(nlgMainWindow)
    # setupUi

    def retranslateUi(self, nlgMainWindow):
        nlgMainWindow.setWindowTitle(QCoreApplication.translate("nlgMainWindow", u"nlgMiHotel", None))
        self.nlgHabitaciones.setText(QCoreApplication.translate("nlgMainWindow", u"Habitaciones", None))
        self.nlgMenuPrincipal.setText(QCoreApplication.translate("nlgMainWindow", u"Men\u00fa Principal", None))
        self.nlgSalones.setText(QCoreApplication.translate("nlgMainWindow", u"Salones", None))
        self.buttonMostrarReserva.setText(QCoreApplication.translate("nlgMainWindow", u"Mostrar Reservas", None))
        self.label.setText("")
        self.nlgFotoHotel.setText("")
#if QT_CONFIG(tooltip)
        self.nlgMiHotel.setToolTip(QCoreApplication.translate("nlgMainWindow", u"<html><head/><body><p align=\"center\"><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.nlgMiHotel.setText(QCoreApplication.translate("nlgMainWindow", u"   Mi  Hotel", None))
        self.label_5.setText("")
        self.labelTituloContacto.setText(QCoreApplication.translate("nlgMainWindow", u"<html><head/><body><p><span style=\" text-decoration: underline; color:#ffffff;\">Contacta con nosotros</span></p></body></html>", None))
        self.labelLocalizacion.setText(QCoreApplication.translate("nlgMainWindow", u"<html><head/><body><p><a href=\"https://www.google.com/url?sa=t&amp;source=web&amp;rct=j&amp;opi=89978449&amp;url=/maps/place//data%3D!4m2!3m1!1s0xd43ab80e7b9facf:0xfafe80f46fc8cfc5%3Fsa%3DX%26ved%3D1t:8290%26ictx%3D111&amp;ved=2ahUKEwj48tC8q6KKAxUGUqQEHYtPHyMQ4kB6BAgmEAM&amp;usg=AOvVaw1HypJaJCUcnbp1AeJAdMDm\"><span style=\" text-decoration: underline; color:#0000ff;\">C/ Hermanos Fern\u00e1ndez Galiano, 6, 19004 Guadalajara</span></a></p><p><br/></p></body></html>", None))
        self.labelTl.setText(QCoreApplication.translate("nlgMainWindow", u"<html><head/><body><p><span style=\" color:#f6f5f4;\">Tel\u00e9fono 666 33 44 55</span></p></body></html>", None))
    # retranslateUi

