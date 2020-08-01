#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FansWheels import *


class InPaint:
    def __init__(self, img, linethick=30, radius=20):
        self.img = blend_3c(img)
        self.view = self.img.copy()
        self.mask = np.zeros((self.img.shape[0], self.img.shape[1]), dtype=np.uint8)
        self.x_old, self.y_old = 0, 0
        self.linethick = linethick
        self.radius = radius
        self.method = cv2.INPAINT_TELEA
        self.linecolor = (0, 127, 255)
        self.firstRun = True

        self.maxUndoSize = 5
        self.undoPtr = 0
        self.imgUndoStack = []

    def startDrawing(self, x=0, y=0, linethick=None):
        if linethick is not None:
            self.linethick = linethick
        self.mask = np.zeros((self.img.shape[0], self.img.shape[1]), dtype=np.uint8)
        self.x_old, self.y_old = x, y
        cv2.line(self.view, (x, y), (x, y), self.linecolor, self.linethick)
        cv2.line(self.mask, (x, y), (x, y), 255, self.linethick)

    def drawPoint(self, x=0, y=0, linethick=None):
        if linethick is not None:
            self.linethick = linethick
        cv2.line(self.view, (self.x_old, self.y_old), (x, y), self.linecolor, self.linethick)
        cv2.line(self.mask, (self.x_old, self.y_old), (x, y), 255, self.linethick)
        self.x_old, self.y_old = x, y

    def update(self):
        self.firstRun = False
        self.undoPtr += 1
        self.imgUndoStack.append(self.img)
        if self.undoPtr > self.maxUndoSize:
            self.undoPtr -= 1
            del self.imgUndoStack[0]
        del self.imgUndoStack[self.undoPtr:]
        self.img = cv2.inpaint(self.img, self.mask, self.radius, self.method)
        self.view = self.img.copy()
        self.printStackInfo()

    def setParam(self, linethick=None, radius=None, method=None):
        if linethick is not None:
            self.linethick = linethick
        if radius is not None:
            self.radius = radius
        if method is not None:
            if method == 0:
                self.method = cv2.INPAINT_TELEA
            else:
                self.method = cv2.INPAINT_NS

    def getParam(self):
        if self.method == cv2.INPAINT_TELEA:
            method = 0
        else:
            method = 1
        return self.linethick, self.radius, method

    def undo(self):
        if self.undoCheck():
            if self.undoPtr > len(self.imgUndoStack) - 1:
                self.imgUndoStack.append(self.img)
            self.undoPtr -= 1
            self.img = self.imgUndoStack[self.undoPtr]
            self.view = self.img.copy()
        self.printStackInfo()

    def redo(self):
        if self.redoCheck():
            self.undoPtr += 1
            self.img = self.imgUndoStack[self.undoPtr]
            self.view = self.img.copy()
        self.printStackInfo()

    def undoCheck(self):
        if self.undoPtr > 0:
            return True
        else:
            return False

    def redoCheck(self):
        if self.undoPtr < len(self.imgUndoStack) - 1:
            return True
        else:
            return False

    def printStackInfo(self):
        print("ptr:", self.undoPtr, "stack:", len(self.imgUndoStack))

    def getImage(self):
        return self.img

    def getView(self):
        return self.view
