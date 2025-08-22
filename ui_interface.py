# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfacewptADf.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLCDNumber, QLabel,
    QPushButton, QSizePolicy, QWidget)

from pyqtgraph import PlotWidget

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(609, 627)
        self.Graph1 = PlotWidget(Form)
        self.Graph1.setObjectName(u"Graph1")
        self.Graph1.setGeometry(QRect(60, 150, 471, 201))
        self.Graph2 = PlotWidget(Form)
        self.Graph2.setObjectName(u"Graph2")
        self.Graph2.setGeometry(QRect(60, 390, 471, 201))
        self.pushButton_open = QPushButton(Form)
        self.pushButton_open.setObjectName(u"pushButton_open")
        self.pushButton_open.setGeometry(QRect(410, 20, 75, 24))
        self.comboBox_port = QComboBox(Form)
        self.comboBox_port.setObjectName(u"comboBox_port")
        self.comboBox_port.setGeometry(QRect(490, 20, 94, 25))
        self.comboBox_port.setStyleSheet(u"font: 700 12pt \"\ub9d1\uc740 \uace0\ub515\";\n"
"color: rgb(0, 0, 0);")
        self.lcdNumber_aqiValue = QLCDNumber(Form)
        self.lcdNumber_aqiValue.setObjectName(u"lcdNumber_aqiValue")
        self.lcdNumber_aqiValue.setGeometry(QRect(60, 50, 81, 61))
        self.lcdNumber_aqiValue.setStyleSheet(u"font: 14pt \"\ub9d1\uc740 \uace0\ub515\";")
        self.lcdNumber_aqiValue.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.lcdNumber_rpm = QLCDNumber(Form)
        self.lcdNumber_rpm.setObjectName(u"lcdNumber_rpm")
        self.lcdNumber_rpm.setGeometry(QRect(170, 50, 81, 61))
        self.lcdNumber_rpm.setStyleSheet(u"font: 14pt \"\ub9d1\uc740 \uace0\ub515\";")
        self.lcdNumber_rpm.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 30, 81, 16))
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(170, 30, 81, 16))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_open.setText(QCoreApplication.translate("Form", u"open", None))
        self.label.setText(QCoreApplication.translate("Form", u"AQI Value", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"FAN RPM", None))
    # retranslateUi

