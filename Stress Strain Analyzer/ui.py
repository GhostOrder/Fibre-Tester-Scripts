# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(856, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphWidget = PlotWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(19, 19, 541, 521))
        self.graphWidget.setObjectName("graphWidget")
        self.setup_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.setup_groupBox.setGeometry(QtCore.QRect(570, 10, 271, 71))
        self.setup_groupBox.setObjectName("setup_groupBox")
        self.gaugeLength_label = QtWidgets.QLabel(self.setup_groupBox)
        self.gaugeLength_label.setGeometry(QtCore.QRect(10, 20, 121, 21))
        self.gaugeLength_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gaugeLength_label.setObjectName("gaugeLength_label")
        self.gaugeLength_lineEdit = QtWidgets.QLineEdit(self.setup_groupBox)
        self.gaugeLength_lineEdit.setGeometry(QtCore.QRect(140, 20, 91, 20))
        self.gaugeLength_lineEdit.setObjectName("gaugeLength_lineEdit")
        self.gaugeLengthUnits_label = QtWidgets.QLabel(self.setup_groupBox)
        self.gaugeLengthUnits_label.setGeometry(QtCore.QRect(240, 20, 21, 21))
        self.gaugeLengthUnits_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.gaugeLengthUnits_label.setObjectName("gaugeLengthUnits_label")
        self.controls_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.controls_groupBox.setGeometry(QtCore.QRect(570, 90, 271, 111))
        self.controls_groupBox.setObjectName("controls_groupBox")
        self.selectBackground_pushButton = QtWidgets.QPushButton(self.controls_groupBox)
        self.selectBackground_pushButton.setGeometry(QtCore.QRect(20, 30, 131, 28))
        self.selectBackground_pushButton.setObjectName("selectBackground_pushButton")
        self.selectBackground_pushButton.setCheckable(True)
        self.selectSlope_pushButton = QtWidgets.QPushButton(self.controls_groupBox)
        self.selectSlope_pushButton.setGeometry(QtCore.QRect(20, 70, 131, 28))
        self.selectSlope_pushButton.setObjectName("selectSlope_pushButton")
        self.selectSlope_pushButton.setCheckable(True)
        self.backgroundXRange_label = QtWidgets.QLabel(self.controls_groupBox)
        self.backgroundXRange_label.setGeometry(QtCore.QRect(160, 30, 101, 21))
        self.backgroundXRange_label.setText("")
        self.backgroundXRange_label.setObjectName("backgroundXRange_label")
        self.slopeXRange_label = QtWidgets.QLabel(self.controls_groupBox)
        self.slopeXRange_label.setGeometry(QtCore.QRect(160, 70, 101, 21))
        self.slopeXRange_label.setText("")
        self.slopeXRange_label.setObjectName("slopeXRange_label")
        self.results_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.results_groupBox.setGeometry(QtCore.QRect(570, 220, 271, 111))
        self.results_groupBox.setObjectName("results_groupBox")
        self.strength_header_label = QtWidgets.QLabel(self.results_groupBox)
        self.strength_header_label.setGeometry(QtCore.QRect(20, 20, 141, 16))
        self.strength_header_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.strength_header_label.setObjectName("strength_header_label")
        self.modulus_header_label = QtWidgets.QLabel(self.results_groupBox)
        self.modulus_header_label.setGeometry(QtCore.QRect(20, 40, 141, 16))
        self.modulus_header_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.modulus_header_label.setObjectName("modulus_header_label")
        self.correctedGaugeLength_header_label = QtWidgets.QLabel(self.results_groupBox)
        self.correctedGaugeLength_header_label.setGeometry(QtCore.QRect(10, 60, 151, 16))
        self.correctedGaugeLength_header_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.correctedGaugeLength_header_label.setObjectName("correctedGaugeLength_header_label")
        self.strength_value_label = QtWidgets.QLabel(self.results_groupBox)
        self.strength_value_label.setGeometry(QtCore.QRect(170, 20, 81, 16))
        self.strength_value_label.setText("")
        self.strength_value_label.setObjectName("strength_value_label")
        self.modulus_value_label = QtWidgets.QLabel(self.results_groupBox)
        self.modulus_value_label.setGeometry(QtCore.QRect(170, 40, 81, 16))
        self.modulus_value_label.setText("")
        self.modulus_value_label.setObjectName("modulus_value_label")
        self.correctedGaugeLength_value_label = QtWidgets.QLabel(self.results_groupBox)
        self.correctedGaugeLength_value_label.setGeometry(QtCore.QRect(170, 60, 81, 16))
        self.correctedGaugeLength_value_label.setText("")
        self.correctedGaugeLength_value_label.setObjectName("correctedGaugeLength_value_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stress-Strain Analyzer"))
        self.setup_groupBox.setTitle(_translate("MainWindow", "Setup"))
        self.gaugeLength_label.setText(_translate("MainWindow", "Gauge Length"))
        self.gaugeLength_lineEdit.setText(_translate("MainWindow", "10"))
        self.gaugeLengthUnits_label.setText(_translate("MainWindow", "mm"))
        self.controls_groupBox.setTitle(_translate("MainWindow", "Controls"))
        self.selectBackground_pushButton.setText(_translate("MainWindow", "Select Background"))
        self.selectSlope_pushButton.setText(_translate("MainWindow", "Select Slope"))
        self.results_groupBox.setTitle(_translate("MainWindow", "Results"))
        self.strength_header_label.setText(_translate("MainWindow", "Tensile Strength:"))
        self.modulus_header_label.setText(_translate("MainWindow", "Elastic Modulus:"))
        self.correctedGaugeLength_header_label.setText(_translate("MainWindow", "Corrected Gauge Length:"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
