# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator
#
# WARNING: Any manual changes to this file will be lost when pyuic5 is run again.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 400)

        # Replace mainLayout from 2 columns -> 3 columns
        self.mainLayout = QtWidgets.QHBoxLayout(Form)

        # Left: UART receive panel (VBox)
        self.leftPanel = QtWidgets.QVBoxLayout()

        # Mode selection buttons (HEX / ASCII)
        self.modeLayout = QtWidgets.QHBoxLayout()
        self.hexButton = QtWidgets.QPushButton("HEX")
        self.hexButton.setCheckable(True)
        self.asciiButton = QtWidgets.QPushButton("ASCII")
        self.asciiButton.setCheckable(True)

        self.hexButton.setChecked(True)   # default = hex
        self.asciiButton.setChecked(False)   

        self.modeLayout.addWidget(self.hexButton)
        self.modeLayout.addWidget(self.asciiButton)
        self.leftPanel.addLayout(self.modeLayout)

        # Left: UART receive area
        self.rxTextEdit = QtWidgets.QTextEdit(Form)
        self.rxTextEdit.setObjectName("rxTextEdit")
        self.rxTextEdit.setReadOnly(True)
        self.leftPanel.addWidget(self.rxTextEdit, 4)
        # self.mainLayout.addWidget(self.rxTextEdit, 1)  # stretch = 1
        self.mainLayout.addLayout(self.leftPanel,0)

        # Center: Log area
        self.logTextEdit = QtWidgets.QTextEdit(Form)
        self.logTextEdit.setObjectName("logTextEdit")
        self.logTextEdit.setReadOnly(True)
        self.mainLayout.addWidget(self.logTextEdit, 4)

        self.rxTextEdit.setMinimumWidth(300)
        self.rxTextEdit.setMaximumWidth(300)  # effectively fixed

        self.logTextEdit.setMinimumWidth(300)
        self.logTextEdit.setMaximumWidth(300)


        # Right: Buttons & COM controls
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.setObjectName("rightLayout")

        # COM controls (Combo + buttons)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.portComboBox = QtWidgets.QComboBox(Form)
        self.refreshButton = QtWidgets.QPushButton(Form)
        self.openButton = QtWidgets.QPushButton(Form)
        self.horizontalLayout.addWidget(self.portComboBox)
        self.horizontalLayout.addWidget(self.refreshButton)
        self.horizontalLayout.addWidget(self.openButton)
        self.rightLayout.addLayout(self.horizontalLayout)

        # Command buttons area
        self.buttonLayout = QtWidgets.QGridLayout()
        self.rightLayout.addLayout(self.buttonLayout)

        # Status label
        self.statusLabel = QtWidgets.QLabel(Form)
        self.statusLabel.setText("Ready")
        self.rightLayout.addWidget(self.statusLabel)

        self.mainLayout.addLayout(self.rightLayout, 0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "UART Command Tool"))
        self.refreshButton.setText(_translate("Form", "Refresh"))
        self.openButton.setText(_translate("Form", "Open COM"))

