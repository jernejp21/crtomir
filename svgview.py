# -*- coding: utf-8 -*-

#############################################################################
#
# Copyright (c) 2020 Jernej Pangerc
# See LICENCE file for details [2].
#
#############################################################################

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg


class SvgView(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)

        self.svg_file = None
        self.items = None
        self.svgItem = None
        self.backgroundItem = None
        self.outlineItem = None

    def run(self):
        self.setScene(QtWidgets.QGraphicsScene(self))

    def openFile(self, svg_file):

        if not svg_file.exists():
            return

        s = self.scene()

        if self.backgroundItem:
            drawBackground = self.backgroundItem.isVisible()
        else:
            drawBackground = False

        if self.outlineItem:
            drawOutline = self.outlineItem.isVisible()
        else:
            drawOutline = True

        s.clear()

        self.svgItem = QtSvg.QGraphicsSvgItem(svg_file.fileName())
        self.svgItem.setFlags(QtWidgets.QGraphicsItem.ItemClipsToShape)
        self.svgItem.setCacheMode(QtWidgets.QGraphicsItem.NoCache)
        self.svgItem.setZValue(0)

        self.backgroundItem = QtWidgets.QGraphicsRectItem(
            self.svgItem.boundingRect())
        self.backgroundItem.setBrush(QtCore.Qt.white)
        self.backgroundItem.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.backgroundItem.setVisible(drawBackground)
        self.backgroundItem.setZValue(-1)

        self.outlineItem = QtWidgets.QGraphicsRectItem(
            self.svgItem.boundingRect())
        outline = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.DashLine)
        outline.setCosmetic(True)
        self.outlineItem.setPen(outline)
        self.outlineItem.setBrush(QtGui.QBrush(QtCore.Qt.NoBrush))
        self.outlineItem.setVisible(drawOutline)
        self.outlineItem.setZValue(1)

        s.addItem(self.backgroundItem)
        s.addItem(self.svgItem)
        s.addItem(self.outlineItem)

        s.setSceneRect(
            self.outlineItem.boundingRect().adjusted(-10, -10, 10, 10))

    def setViewBackground(self, enable):
        if self.backgroundItem:
            self.backgroundItem.setVisible(enable)

    def setViewOutline(self, enable):
        if self.outlineItem:
            self.outlineItem.setVisible(enable)

    def wheelEvent(self, event):
        factor = pow(1.2, event.angleDelta().y() / 240.0)
        self.scale(factor, factor)
        event.accept()
