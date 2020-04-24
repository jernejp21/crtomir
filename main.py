# -*- coding: utf-8 -*-

#############################################################################
##
## Copyright (c) 2020 Jernej Pangerc
## See LICENCE file for details [1].
##
#############################################################################

import sys
import os
import xml.etree.ElementTree as ET
import re
import time
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg, Qt

from mainwindow import Ui_MainWindow
from simulation import Ui_Dialog
from svgview import SvgView
from createPaths import CreatePaths as cp


class DialogWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.elementsClasses = None
        self.timer = QtCore.QTimer()

        self.runButton.clicked.connect(self.run)
        self.stepFwdButton.clicked.connect(self.stepFwd)
        self.stepBackButton.clicked.connect(self.stepBack)
        self.graphicsView.setScene(QtWidgets.QGraphicsScene(self.graphicsView))
        self.scene = self.graphicsView.scene()

    def initialise(self):
        self.lines = []
        self.isFirstRun = True
        self.pathIndex = 0
        self.scene.clear()
        self.timer.setInterval(100)
        self.timer.timeout.connect(lambda: self.startNewThread('forward'))

    def wheelEvent(self, event):
        factor = pow(1.2, event.angleDelta().y() / 240.0)
        self.graphicsView.scale(factor, factor)
        event.accept()

    def run(self):
        if self.runButton.text() == 'Run':
            self.runButton.setText('Stop')
            self.stepFwdButton.setDisabled(True)
            self.stepBackButton.setDisabled(True)

            if self.isFirstRun:
                self.scene = self.graphicsView.scene()
                self.clearScene()

                # Set outline for A4 paper size
                outlineItem = QtWidgets.QGraphicsRectItem(0, 0, 210, 297)
                outline = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.DashLine)
                outline.setCosmetic(True)
                outlineItem.setPen(outline)
                outlineItem.setBrush(QtGui.QBrush(QtCore.Qt.NoBrush))
                outlineItem.setVisible(True)
                outlineItem.setZValue(1)

                self.scene.addItem(outlineItem)
                #self.worker = DrawPlot(self.graphicsView)
                self.pathIndex = 0
                self.xIndex = 1
                self.timer.start()

            else:
                self.timer.start()

        else:
            self.isFirstRun = False
            self.runButton.setText('Run')
            self.stepFwdButton.setEnabled(True)
            self.stepBackButton.setEnabled(True)
            self.timer.stop()

    def stepFwd(self):
        if self.isFirstRun:
            self.scene = self.graphicsView.scene()
            self.clearScene()

            # Set outline for A4 paper size
            outlineItem = QtWidgets.QGraphicsRectItem(0, 0, 210, 297)
            outline = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.DashLine)
            outline.setCosmetic(True)
            outlineItem.setPen(outline)
            outlineItem.setBrush(QtGui.QBrush(QtCore.Qt.NoBrush))
            outlineItem.setVisible(True)
            outlineItem.setZValue(1)

            self.scene.addItem(outlineItem)
            self.scene.setSceneRect(
                outlineItem.boundingRect().adjusted(-10, -10, 10, 10))

            self.isFirstRun = False

        self.startNewThread('forward')

    def stepBack(self):
        self.startNewThread('backward')

    def setElementsClasses(self, classes):
        self.elementsClasses = classes

    def setSimulationPath(self):
        path = {'x': [], 'y': []}
        self.paths = []
        for element in self.elementsClasses:
            path = {'x': [], 'y': []}
            if 'rect' == element.classType:
                path = cp().getRectPath(element)
                self.paths.append(path)

            if 'circle' == element.classType:
                path = cp().getCircPath(element)
                self.paths.append(path)

            if 'ellipse' == element.classType:
                path = cp().getEllipsePath(element)
                self.paths.append(path)

            if 'line' == element.classType:
                path = cp().getLinePath(element)
                self.paths.append(path)

    def setLineItems(self):
        for path in self.paths:
            for xIndex in range(1, len(path['x'])):
                x1 = path['x'][xIndex-1]
                y1 = path['y'][xIndex-1]
                x2 = path['x'][xIndex]
                y2 = path['y'][xIndex]

                pen = QtGui.QPen()
                pen.setWidth(0.5)
                pen.setColor(QtGui.QColor("#FFFF0000"))
                line = QtWidgets.QGraphicsLineItem(x1, y1, x2, y2)
                line.setPen(pen)

                self.lines.append(line)

    def startNewThread(self, direction):
        nrOfPaths = len(self.lines)
        if self.pathIndex < nrOfPaths:
            #self.scene = self.graphicsView.scene()

            if direction == 'forward':
                line = self.lines[self.pathIndex]
                self.pathIndex += 1
                self.scene.addItem(line)
            else:
                if self.pathIndex > 0:
                    self.pathIndex -= 1
                    line = self.lines[self.pathIndex]
                    self.scene.removeItem(line)

        else:
            self.timer.stop()
            # self.timer.timeout.disconnect(self.startNewThread)
            self.runButton.setText('Run')
            self.stepFwdButton.setEnabled(True)
            self.stepBackButton.setEnabled(True)
            self.pathIndex = 0
            self.isFirstRun = True

    def clearScene(self):
        #scene = self.graphicsView.scene()
        items = self.scene.items()
        if len(items) > 0:
            for item in items:
                self.scene.removeItem(item)


class AppWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.simDialog = DialogWindow()
        self.simDialog.finished.connect(self.closeDialog)

        self.graphicsView.run()
        #self.view = SvgView()
        self.setCentralWidget(self.centralwidget)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionExit.triggered.connect(self.exitProgram)
        self.actionSimulation.triggered.connect(self.simulation)
        self.actionBackground.triggered.connect(
            self.graphicsView.setViewBackground)
        self.actionOutline.triggered.connect(self.graphicsView.setViewOutline)

        #----------------test------------------------#

        self.treeWidget.itemClicked.connect(self.checkBoxClick)

        self.name = ''
        self.path = ''
        self.temp = ''

    def treeViev(self):  # fc:startStop AppWindow treeView
        self.treeWidget.clear()  # fc:middleware "Clear tree struct" QTreeWidget.clear()

        tree = ET.parse(self.path)
        root = tree.getroot()
        namespace = '{' + re.split('[{}]', root.tag)[1] + '}'

        elements = Elements(root, self.treeWidget, namespace)

        classes = elements.getClasses()
        self.simDialog.initialise()
        self.simDialog.setElementsClasses(classes)
        self.simDialog.setSimulationPath()
        self.simDialog.setLineItems()

        self.temp = self.path.replace('.svg', '_temp.svg')
        tree.write(self.temp)

        self.treeWidget.setHeaderLabel(self.name)
        self.treeWidget.expandAll()
        self.treeWidget.show()

    # fc:startStop end

    def checkBoxClick(self, event):
        iterator = QtWidgets.QTreeWidgetItemIterator(
            self.treeWidget, QtWidgets.QTreeWidgetItemIterator.NotChecked)
        items = []
        while iterator.value():
            item = iterator.value()
            text = item.text(0)
            itemID = text.split(': ')[1]
            items.append(itemID)
            iterator += 1

        tree = ET.parse(self.temp)
        root = tree.getroot()
        namespace = '{' + re.split('[{}]', root.tag)[1] + '}'
        HideElements(root, items, namespace)
        tree.write(self.temp)

        tmp = QtCore.QFile(self.temp)
        self.graphicsView.openFile(tmp)

        #-----------------test konec--------------------#

    def openFile(self, path=None):
        if not path:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open SVG File",
                                                            '', "SVG files (*.svg)")

        if path:
            self.path = path
            self.name = os.path.split(path)[1]

            self.treeViev()
            tmp = QtCore.QFile(self.temp)
            self.graphicsView.openFile(tmp)
            self.treeWidget.setHeaderLabel(self.name)
            self.actionSimulation.setEnabled(True)

    def exitProgram(self):
        self.close()

    def simulation(self):
        self.simDialog.show()

    def closeDialog(self, event):
        print('Close sim dialog')

    def closeEvent(self, event):
        if w.temp:
            os.remove(w.temp)

        self.simDialog.close()


class Elements():
    def __init__(self, root, tree, namespace):
        self.tree = [tree]
        self.classes = []
        self.razred = None
        self.indent = 0
        self.namespace = namespace
        self.useElements = (namespace + 'g',
                            namespace + 'rect',
                            namespace + 'circle',
                            namespace + 'ellipse',
                            namespace + 'path',
                            namespace + 'polyline')

        self.printRecur(root)

    def printRecur(self, root):
        """Recursively prints the tree."""
        # print(' '*self.indent + '%s: %s' %
        #      (root.tag.replace(self.namespace, ''), root.attrib.get('id', root.text)))
        string = str(root.tag.replace(self.namespace, '')) + \
            ': ' + str(root.attrib.get('id', root.text))
        parent = QtWidgets.QTreeWidgetItem(self.tree[-1])
        parent.setText(0, string)
        root.set("visibility", "visible")

        var = 'self.razred'  # root.attrib.get('id', root.text)
        classType = root.tag.replace(self.namespace, '')
        clas = classType.capitalize()
        execStr = var + '=' + clas + \
            '(args=' + str(root.items()) + ', classType="' + classType + '")'
        # print(execStr)
        exec(execStr)
        self.classes.append(self.razred)
        self.indent += 2
        parent.setFlags(parent.flags() | Qt.Qt.ItemIsTristate |
                        Qt.Qt.ItemIsUserCheckable)
        self.tree.append(parent)
        for elem in root:
            if elem.tag in self.useElements:
                self.printRecur(elem)
        self.indent -= 2
        parent.setFlags(parent.flags() | Qt.Qt.ItemIsUserCheckable)
        parent.setCheckState(0, Qt.Qt.Checked)
        del(self.tree[-1])

    def getClasses(self):
        return self.classes


class HideElements:
    def __init__(self, root, items, namespace):
        self.items = items
        self.useElements = (namespace + 'g',
                            namespace + 'rect',
                            namespace + 'circle',
                            namespace + 'ellipse',
                            namespace + 'path',
                            namespace + 'text',
                            namespace + 'polyline')

        self.printRecur(root)

    def printRecur(self, root):
        """Recursively prints the tree."""
        elementID = root.get('id')
        root.set("visibility", "visible")

        if elementID:
            for item in self.items:
                if elementID in item:
                    root.set("visibility", "hidden")

        for elem in root:
            if elem.tag in self.useElements:
                self.printRecur(elem)


class Rect:
    def __init__(self, args, classType):
        self.style = None
        self.id = None
        self.x = 0
        self.y = 0
        self.width = None
        self.height = None
        self.rx = None
        self.ry = None
        self.classType = classType

        validArgs = ('style', 'id', 'x', 'y', 'width', 'height', 'rx', 'ry')

        for arg in args:
            if arg[0] in validArgs:
                var = 'self.' + arg[0]
                val = arg[1]
                str = var + '=' + 'val'
                exec(str)

        if self.rx or self.ry:
            if self.rx and self.ry:
                pass
            else:
                if self.rx:
                    self.ry = self.rx
                elif self.ry:
                    self.rx = self.ry
        else:
            self.rx = 0
            self.ry = 0


class Circle:
    def __init__(self, args, classType):
        self.style = None
        self.id = None
        self.cx = None
        self.cy = None
        self.r = None
        self.classType = classType

        validArgs = ('style', 'id', 'cx', 'cy', 'r')

        for arg in args:
            if arg[0] in validArgs:
                var = 'self.' + arg[0]
                val = arg[1]
                str = var + '=' + 'val'
                exec(str)


class Ellipse:
    def __init__(self, args, classType):
        self.style = None
        self.id = None
        self.cx = None
        self.cy = None
        self.rx = None
        self.ry = None
        self.classType = classType

        validArgs = ('style', 'id', 'cx', 'cy', 'rx', 'ry')

        for arg in args:
            if arg[0] in validArgs:
                var = 'self.' + arg[0]
                val = arg[1]
                str = var + '=' + 'val'
                exec(str)


class Line:
    def __init__(self, args, classType):
        self.style = None
        self.id = None
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.classType = classType

        validArgs = ('style', 'id', 'x1', 'x2', 'y1', 'y2')

        for arg in args:
            if arg[0] in validArgs:
                var = 'self.' + arg[0]
                val = arg[1]
                str = var + '=' + 'val'
                exec(str)


class Polyline:
    def __init__(self, args, classType):
        self.style = None
        self.id = None
        self.points = None
        self.classType = classType

        validArgs = ('style', 'id', 'points')

        for arg in args:
            if arg[0] in validArgs:
                var = 'self.' + arg[0]
                val = arg[1]
                str = var + '=' + 'val'
                exec(str)


class Path:
    def __init__(self, args, classType):
        self.style = None
        self.id = None
        self.d = None
        self.classType = classType

        validArgs = ('style', 'id', 'd')

        for arg in args:
            if arg[0] in validArgs:
                var = 'self.' + arg[0]
                val = arg[1]
                str = var + '=' + 'val'
                exec(str)


class Svg:
    def __init__(self, args, classType):
        self.classType = classType


class G:
    def __init__(self, args, classType):
        self.classType = classType


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = AppWindow()
    w.show()
    # w.showMaximized()
    sys.exit(app.exec_())
