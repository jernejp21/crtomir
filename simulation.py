# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulation.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 768)
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(105, 11, 911, 751))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.graphicsView.setBackgroundBrush(brush)
        self.graphicsView.setAlignment(QtCore.Qt.AlignCenter)
        self.graphicsView.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.graphicsView.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.graphicsView.setObjectName("graphicsView")
        self.stepFwdButton = QtWidgets.QPushButton(Dialog)
        self.stepFwdButton.setGeometry(QtCore.QRect(10, 80, 81, 31))
        self.stepFwdButton.setObjectName("stepFwdButton")
        self.runButton = QtWidgets.QPushButton(Dialog)
        self.runButton.setGeometry(QtCore.QRect(10, 40, 81, 31))
        self.runButton.setObjectName("runButton")
        self.stepBackButton = QtWidgets.QPushButton(Dialog)
        self.stepBackButton.setGeometry(QtCore.QRect(10, 120, 81, 31))
        self.stepBackButton.setObjectName("stepBackButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.stepFwdButton.setText(_translate("Dialog", "Step Fwd"))
        self.runButton.setText(_translate("Dialog", "Run"))
        self.stepBackButton.setText(_translate("Dialog", "Step Back"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
