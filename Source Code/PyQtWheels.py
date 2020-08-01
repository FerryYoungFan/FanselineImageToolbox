#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
import cv2
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from PyQtStyle import *


class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = PixmapWithDrop(self, parent.loadImage)

        self._scene.addItem(self._photo)
        self.parent = parent
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(10, 10, 10)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.draw_x0, self.draw_y0, self.draw_x1, self.draw_y1 = 0, 0, 0, 0
        self.isDrawing = False
        self.mode = 0  # 0-view, 1-draw rectangle, 2-draw add mask, 3-draw remove mask
        self.tempmode = 0
        self.spaceFlag = False

        self.parent.setAcceptDrops(True)

        def dragEnterEvent(event):
            if event.mimeData().hasUrls:
                event.accept()
            else:
                event.ingore()

        def dropEvent(event):
            for url in event.mimeData().urls():
                self.parent.loadImage(url.toLocalFile())
                break

        self.parent.dragEnterEvent = dragEnterEvent
        self.parent.dropEvent = dropEvent

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
        self._zoom = 0

    def getSelectBrushSize(self):
        if self.hasPhoto():
            rect = QtCore.QRectF(self._photo.pixmap().rect())
            scenerect = self.transform().mapRect(rect)
            factor = self._photo.pixmap().width() / scenerect.width()
            if factor < 1:
                return 1
            else:
                return int(round(factor))
        else:
            return 1

    def setPhoto(self, pixmap=None):
        self._empty = False
        self._photo.setPixmap(pixmap)

    def wheelEvent(self, event):
        if self.hasPhoto() and self.mode in [-1, 0]:
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom <= 0:
                self.fitInView()

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def keyPressEvent(self, event):
        key = event.key()
        if key == 32 and self.spaceFlag == False and self.isDrawing == False and not event.isAutoRepeat():
            if self.mode not in [0, -64]:
                self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
                self.tempmode = self.mode
                self.mode = -1
                self.parent.crosshairCursor(False)
            self.spaceFlag = True
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == 32 and self.spaceFlag == True and self.isDrawing == False and not event.isAutoRepeat():
            if self.mode == -1:
                self.mode = self.tempmode
                self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                self.parent.crosshairCursor(True)
            self.spaceFlag = False
        else:
            super().keyReleaseEvent(event)

    def mousePressEvent(self, event):
        point = self.mapToScene(event.pos()).toPoint()
        if self.mode in [0, -1]:
            self.photoClicked.emit(point)
            super(PhotoViewer, self).mousePressEvent(event)
        elif self.mode in [1, 2, 3]:
            self.draw_x0, self.draw_y0 = point.x(), point.y()
            self.draw_x1, self.draw_y1 = point.x(), point.y()
            self.isDrawing = True
            self.parent.newMaskCanvas()
            self.parent.drawMaskCanvas(self.draw_x1, self.draw_y1, point.x(), point.y(), self.draw_x0, self.draw_y0,
                                       self.mode)
        elif self.mode in [4, 5, 6] and self._photo.isUnderMouse():
            self.parent.setMagicWand(point.x(), point.y())
        elif self.mode in [7, 8]:
            self.isDrawing = True
            self.parent.setCommonSelect(point.x(), point.y())
        elif self.mode == 9:
            self.isDrawing = True
            self.parent.startInpaint(point.x(), point.y())
        elif self.mode == 10 and self._photo.isUnderMouse():
            self.parent.setColorRange(point.x(), point.y())

    def mouseMoveEvent(self, event):
        if self.mode in [0, -1]:
            super(PhotoViewer, self).mouseMoveEvent(event)
        elif self.isDrawing:
            point = self.mapToScene(event.pos()).toPoint()
            self.parent.drawMaskCanvas(self.draw_x1, self.draw_y1, point.x(), point.y(), self.draw_x0, self.draw_y0,
                                       self.mode)
            self.draw_x1, self.draw_y1 = point.x(), point.y()

    def mouseReleaseEvent(self, event):
        if self.mode in [0, -1]:
            super(PhotoViewer, self).mouseReleaseEvent(event)
        elif self.isDrawing:
            self.isDrawing = False
            point = self.mapToScene(event.pos()).toPoint()
            self.draw_x1, self.draw_y1 = point.x(), point.y()
            self.parent.showDrawMask(self.draw_x1, self.draw_y1, point.x(), point.y(), self.draw_x0, self.draw_y0,
                                     self.mode)

    def startDrawing(self, mode=1):
        self.mode = mode
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

    def stopDrawing(self):
        self.mode = 0
        if not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def getPixmap(self):
        return self._photo.pixmap()


class PixmapWithDrop(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, parent, fileEvent=None):
        super(PixmapWithDrop, self).__init__()
        self.parent = parent
        self.setAcceptDrops(True)
        self.fileEvent = fileEvent
        self.setTransformationMode(1)
        self.setShapeMode(1)  # For Drop Event

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if self.fileEvent is not None:
                self.fileEvent(url.toLocalFile())
            break


def genSlider(window, slName="mySlider", minv=0, maxv=100, stepv=1, value=0, releaseEvent=None, changeEvent=None,
              sl_type=0):
    slider = QtWidgets.QSlider(window)
    label_minimum = QtWidgets.QLabel(alignment=QtCore.Qt.AlignLeft)
    label_maximum = QtWidgets.QLabel(alignment=QtCore.Qt.AlignRight)
    label_name = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
    label_minimum.setNum(minv)
    label_maximum.setNum(maxv)
    label_name.setText(slName)
    label_minimum.setProperty("fontset", 0)
    label_maximum.setProperty("fontset", 0)
    label_name.setProperty("fontset", 1)

    slider.setOrientation(QtCore.Qt.Horizontal)
    slider.resize(400, 100)
    slider.setMinimum(minv)
    slider.setMaximum(maxv)
    slider.setSingleStep(stepv)
    slider.setValue(value)

    if sl_type == 1:
        slider.setStyleSheet(sliderStyle1)
    elif sl_type == 2:
        slider.setStyleSheet(sliderStyle2)
    elif sl_type == 3:
        slider.setStyleSheet(sliderStyle3)
    elif sl_type == 4:
        slider.setStyleSheet(sliderStyle4)
    elif sl_type == 5:
        slider.setStyleSheet(sliderStyle5)
    else:
        slider.setStyleSheet(sliderStyleDefault)

    def nullEvent(*args):
        pass

    slider.keyPressEvent = nullEvent
    slider.wheelEvent = nullEvent
    slider.dragMoveEvent = nullEvent
    slider.setFocusPolicy(QtCore.Qt.NoFocus)

    if releaseEvent is not None:
        slider.sliderReleased.connect(releaseEvent)

    if changeEvent is not None:
        slider.valueChanged.connect(changeEvent)

    def showValues():
        slider.setToolTip(slName + ": " + str(slider.value()))

    slider.valueChanged.connect(showValues)

    sl_vbox = QtWidgets.QVBoxLayout()
    sl_hbox = QtWidgets.QHBoxLayout()
    sl_hbox.setAlignment(QtCore.Qt.AlignBottom)
    sl_hbox.addWidget(label_minimum)
    sl_hbox.addWidget(label_name)
    sl_hbox.addWidget(label_maximum)
    sl_vbox.addLayout(sl_hbox)
    sl_vbox.addWidget(slider)

    def setText(text="text"):
        label_name.setText(text)

    def value():
        return slider.value()

    def setValue(input_value):
        slider.setValue(input_value)

    def close():
        label_minimum.close()
        label_maximum.close()
        label_name.close()
        slider.close()

    def show():
        label_minimum.show()
        label_maximum.show()
        label_name.show()
        slider.show()

    def reset(new_minv=0, new_maxv=100, new_stepv=1, new_value=0):
        slider.setMinimum(new_minv)
        slider.setMaximum(new_maxv)
        slider.setSingleStep(new_stepv)
        slider.setValue(new_value)
        label_minimum.setNum(new_minv)
        label_maximum.setNum(new_maxv)

    sl_vbox.value = value
    sl_vbox.setValue = setValue
    sl_vbox.setText = setText
    sl_vbox.reset = reset
    sl_vbox.close = close
    sl_vbox.show = show
    showValues()

    return sl_vbox


def genLabel(window, content="No Content", fonttype=2):
    label = QtWidgets.QLabel(content, window)
    label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
    label.setProperty("fontset", fonttype)
    return label


def genButton(window, text="", press_event=None, release_event=None, shortcut=None, style=1, tooltip=None):
    btn = QtWidgets.QPushButton(window)
    btn.setText(text)
    btn.setFocusPolicy(QtCore.Qt.NoFocus)
    if press_event is not None:
        btn.pressed.connect(press_event)
    if release_event is not None:
        btn.released.connect(release_event)
    if shortcut is not None:
        btn.setShortcut(QtGui.QKeySequence(shortcut))

    if style == 2:
        btn.setStyleSheet(pushButtonStyle2)
    elif style == 3:
        btn.setStyleSheet(pushButtonStyle3)
    elif style == 4:
        btn.setStyleSheet(pushButtonStyle4)
    elif style == 5:
        btn.setStyleSheet(pushButtonStyle5)
    elif style == 6:
        btn.setStyleSheet(pushButtonStyle6)
    else:
        btn.setStyleSheet(pushButtonStyle1)

    btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    if tooltip is None and shortcut is not None:
        if shortcut == "Return":
            shortcut = "Enter"
        elif shortcut == "Escape":
            shortcut = "Esc"
        btn.setToolTip(text + ": (" + shortcut + ")")
    return btn


def genHist(window):
    hist_view = QtWidgets.QLabel(window)
    hist_view.resize(150, 80)
    return hist_view


def cv2qtPhoto(img):
    if len(img.shape) == 3:
        if img.shape[2] == 4:
            qformat = QtGui.QImage.Format_RGBA8888
        else:
            qformat = QtGui.QImage.Format_RGB888
        img = QtGui.QImage(img.data,
                           img.shape[1],
                           img.shape[0],
                           img.strides[0],
                           qformat)
        img = img.rgbSwapped()
    return QtGui.QPixmap.fromImage(img)


def qtpix2cv(qpixmap):
    """
    Converts a QPixmap into an opencv MAT format
    """
    qimg = qpixmap.toImage().convertToFormat(4)
    width, height = qimg.width(), qimg.height()
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    arr = np.array(ptr).reshape((height, width, 4))  # Copies the data
    return arr


def setWindowIcons(app):
    app_icon = QtGui.QIcon()
    logopath = r"GUI/Image/"
    app_icon.addFile(logopath + 'Logo_Desktop_16x16.ico', QtCore.QSize(16, 16))
    app_icon.addFile(logopath + 'Logo_Desktop_24x24.ico', QtCore.QSize(24, 24))
    app_icon.addFile(logopath + 'Logo_Desktop_32x32.ico', QtCore.QSize(32, 32))
    app_icon.addFile(logopath + 'Logo_Desktop_48x48.ico', QtCore.QSize(48, 48))
    app_icon.addFile(logopath + 'Logo_Desktop_128x128.ico', QtCore.QSize(128, 128))
    app_icon.addFile(logopath + 'Logo_Desktop_256x256.ico', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
