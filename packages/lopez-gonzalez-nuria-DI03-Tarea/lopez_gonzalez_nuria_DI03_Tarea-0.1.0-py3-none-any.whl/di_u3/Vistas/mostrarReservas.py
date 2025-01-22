# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mostrarReservasBZiAxv.ui'
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
    QImage, QKeySequence, QLinearGradient, QPainter,QFont,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit, # type: ignore
    QFrame, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpinBox, QStatusBar,QTableWidget,QTableWidgetItem,
    QWidget)



class Ui_nlgReservas(object):
    def setupUi(self, nlgReservas):
        if not nlgReservas.objectName():
            nlgReservas.setObjectName(u"nlgReservas")
        nlgReservas.setWindowModality(Qt.ApplicationModal)
        nlgReservas.resize(756, 705)
        nlgReservas.setStyleSheet(u"background-color: rgb(239, 227, 208);")
        self.centralwidget = QWidget(nlgReservas)
        self.centralwidget.setObjectName(u"centralwidget")
        self.comboBoxSalones = QComboBox(self.centralwidget)
        self.comboBoxSalones.addItem("")
        self.comboBoxSalones.setObjectName(u"comboBoxSalones")
        self.comboBoxSalones.setGeometry(QRect(180, 20, 191, 27))
        font = QFont()
        font.setBold(True)
        font.setWeight(QFont.Bold)
        self.comboBoxSalones.setFont(font)
        self.comboBoxSalones.setEditable(True)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 141, 31))
        font1 = QFont()
        font1.setFamily(u"C059")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setWeight(QFont.Bold)
        self.label.setFont(font1)
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(50, 70, 491, 461))
        self.tableWidget.setColumnCount(5)
        self.pushButtonReserva = QPushButton(self.centralwidget)
        self.pushButtonReserva.setObjectName(u"pushButtonReserva")
        self.pushButtonReserva.setGeometry(QRect(130, 560, 88, 27))
        self.pushButtonReserva.setFont(font)
        self.pushButtonModificar = QPushButton(self.centralwidget)
        self.pushButtonModificar.setObjectName(u"pushButtonModificar")
        self.pushButtonModificar.setGeometry(QRect(280, 560, 131, 27))
        nlgReservas.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(nlgReservas)
        self.statusbar.setObjectName(u"statusbar")
        nlgReservas.setStatusBar(self.statusbar)

        self.retranslateUi(nlgReservas)

        QMetaObject.connectSlotsByName(nlgReservas)
    # setupUi

    def retranslateUi(self, nlgReservas):
        nlgReservas.setWindowTitle(QCoreApplication.translate("nlgReservas", u"nlgReservas", None))
        self.comboBoxSalones.setItemText(0, QCoreApplication.translate("nlgReservas", u"Selecciona un sal\u00f3n", None))

        self.comboBoxSalones.setCurrentText(QCoreApplication.translate("nlgReservas", u"Selecciona un sal\u00f3n", None))
        self.label.setText(QCoreApplication.translate("nlgReservas", u"Tipos de Salones", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("nlgReservas", u"ID", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("nlgReservas", u"FECHA", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("nlgReservas", u"CLIENTE", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("nlgReservas", u"TELEFONO", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("nlgReservas", u"EVENTO", None));
        self.pushButtonReserva.setText(QCoreApplication.translate("nlgReservas", u"Reservar", None))
        self.pushButtonModificar.setText(QCoreApplication.translate("nlgReservas", u"Modificar Reserva", None))
    # retranslateUi

