from FansWheels import *

"""
Select Method - Lasso, Rectangle, Ellipse, Brush
by FerryYoungFan - Twitter @FanKetchup / @FanBuckle
"""

class CSelect:
    def __init__(self, mask_view):
        self.mode = 0
        """
        mode = 0: standby
        mode = 1: brush select
        mode = 2: rectangle select
        mode = 3: ellipse select
        mode = 4: marquee select
        """

        self.INV = False
        self.firstRun = True
        self.img = mask_view.copy()
        self.view = mask_view.copy()
        self.view_d = mask_view.copy()
        self.mask_temp = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.mask_f = np.zeros(self.img.shape[:2], dtype=np.uint8)

        self.x0, self.y0, self.x1, self.y1 = 0, 0, 0, 0
        self.marqueePoints = []

        self.lineColor = (0, 0, 255,255)
        self.lineThick = 3

        self.diak = 0
        self.erok = 0
        self.blurk = 1

        self.maxUndoSize = 5
        self.undoPtr = 0
        self.maskUndoStack = []

    def update(self):
        self.firstRun = False

        self.undoPtr += 1
        self.maskUndoStack.append(self.mask)
        if self.undoPtr > self.maxUndoSize:
            self.undoPtr -= 1
            del self.maskUndoStack[0]
        del self.maskUndoStack[self.undoPtr:]

        if self.mode == 1:
            pass
        elif self.mode == 2:
            cv2.rectangle(self.mask_temp, (self.x0, self.y0), (self.x1, self.y1), 255, -1)
        elif self.mode == 3:
            cv2.ellipse(self.mask_temp, (self.x0, self.y0), (abs(self.x1 - self.x0), abs(self.y1 - self.y0)),
                        0, 0, 360, 255, -1)
        elif self.mode == 4:
            contours = np.array(self.marqueePoints)
            cv2.fillPoly(self.mask_temp, pts=[contours], color=255)
            self.marqueePoints = []

        if not self.INV:
            self.mask = cv2.add(self.mask, self.mask_temp)
        else:
            self.mask = cv2.subtract(self.mask, self.mask_temp)

        self.edgeModify()


    def undo(self):
        if self.undoCheck():
            if self.undoPtr > len(self.maskUndoStack) - 1:
                self.maskUndoStack.append(self.mask)
            self.undoPtr -= 1
            self.mask = self.maskUndoStack[self.undoPtr]
            self.edgeModify()

    def redo(self):
        if self.redoCheck():
            self.undoPtr += 1
            self.mask = self.maskUndoStack[self.undoPtr]
            self.edgeModify()

    def undoCheck(self):
        if self.undoPtr > 0:
            return True
        else:
            return False

    def redoCheck(self):
        if self.undoPtr < len(self.maskUndoStack) - 1:
            return True
        else:
            return False

    def startpoint(self, x0, y0):
        self.x0, self.x1 = x0, x0
        self.y0, self.y1 = y0, y0
        self.view_d = self.view.copy()
        self.mask_temp = np.zeros(self.img.shape[:2], dtype=np.uint8)

        self.marqueePoints = []
        self.marqueePoints.append((x0, y0))

        if not self.INV:
            self.lineColor = (0, 0, 255,255)
        else:
            self.lineColor = (255, 0, 0,255)

    def pushpoint(self, x, y):
        if self.mode in [1, 4]:
            cv2.line(self.view_d, (self.x1, self.y1), (x, y), self.lineColor, self.lineThick)
            if self.mode == 1:
                cv2.line(self.mask_temp, (self.x1, self.y1), (x, y), 255, self.lineThick)
            elif self.mode == 4:
                self.marqueePoints.append([x, y])

        elif self.mode in [2, 3]:
            self.view_d = self.view.copy()
            if self.mode == 2:
                cv2.rectangle(self.view_d, (self.x0, self.y0), (x, y), self.lineColor, self.lineThick)
            elif self.mode == 3:
                cv2.ellipse(self.view_d, (self.x0, self.y0), (abs(x - self.x0), abs(y - self.y0)),
                            0, 0, 360, self.lineColor, self.lineThick)

        self.x1, self.y1 = x, y

    def edgeModify(self,diak=None,erok=None,blurk=None):
        if diak is not None:
            self.diak = diak
        if erok is not None:
            self.erok = erok
        if blurk is not None:
            self.blurk = blurk
        if not self.firstRun:
            self.mask_f = self.mask.copy()
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            if self.diak > 0:
                self.mask_f = cv2.dilate(self.mask_f, kernel, iterations=self.diak)
            if self.erok > 0:
                self.mask_f = cv2.erode(self.mask_f, kernel, iterations=self.erok)
            if self.blurk > 1:
                if self.blurk % 2 == 0:
                    self.blurk += 1
                self.mask_f = cv2.GaussianBlur(self.mask_f, (self.blurk, self.blurk), 0)
        self.view = preview_mask(self.img, self.mask_f)
        self.view_d = self.view

    def setMode(self,mode):
        self.mode = mode

    def getMask(self):
        return self.mask_f

    def getView(self):
        return self.view_d
