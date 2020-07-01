from FansWheels import *

"""
Optimized Grabcut method
by FerryYoungFan - Twitter @FanKetchup / @FanBuckle
Ver1.2: June 28, 2020
"""


class GCut:
    def __init__(self, img):
        self.img = img.copy()
        maxsize = 1024
        if max(self.img.shape) > maxsize:
            self.largePic = True
            self.ratio = maxsize / max(self.img.shape)
            self.oldsize = (self.img.shape[1], self.img.shape[0])
            newh, neww = round(self.img.shape[0] * self.ratio), round(self.img.shape[1] * self.ratio)
            self.newsize = (neww, newh)
            self.img = cv2.resize(self.img, self.newsize)
        else:
            self.ratio = 1
            self.largePic = False
            self.newsize = (self.img.shape[1], self.img.shape[0])
            self.oldsize = (self.img.shape[1], self.img.shape[0])
        self.img = blend_3c(self.img)
        self.gbcmask = np.zeros(self.img.shape[:2], dtype=np.uint8)

        self.output_mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.output_mask_f = self.output_mask.copy()
        self.output_maskb = np.zeros(self.img.shape[:2], dtype=np.uint8)

        self.bgdmodel = np.zeros((1, 65), np.float64)
        self.fgdmodel = np.zeros((1, 65), np.float64)
        self.rect = (0, 0, 1, 1)
        self.iterk = 1

        self.newrect = False
        self.drawmask = False
        self.firstRun = True

        self.diak = 1
        self.erok = 1
        self.blurk = 1

    def update(self, diak=0, erok=0, blurk=0):
        print("grabcut - updating...")
        if self.newrect:
            cv2.grabCut(self.img, self.gbcmask, self.rect, self.bgdmodel,
                        self.fgdmodel, self.iterk, cv2.GC_INIT_WITH_RECT)
            self.newrect = False
            if len(self.gbcmask[self.gbcmask==1])+ len(self.gbcmask[self.gbcmask==3])== 0:
                self.firstRun = True
                self.gbcmask = np.zeros(self.img.shape[:2], dtype=np.uint8)
            else:
                self.firstRun = False
        elif self.drawmask:
            if len(self.gbcmask[self.gbcmask==1])+ len(self.gbcmask[self.gbcmask==3])== 0:
                self.firstRun = True
                self.gbcmask = np.zeros(self.img.shape[:2], dtype=np.uint8)
            else:
                self.firstRun = False
                cv2.grabCut(self.img, self.gbcmask, None, self.bgdmodel,
                            self.fgdmodel, self.iterk, cv2.GC_INIT_WITH_MASK)

        self.output_maskb = np.where((self.gbcmask == 2) | (self.gbcmask == 0), 0, 1).astype("uint8")
        self.output_mask = self.output_maskb * 255
        self.edgeModify()
        print("grabcut - done!")

    def setRect(self, x0, y0, x1, y1):
        if abs(x0 - x1) > 5 and abs(y0 - y1) > 5:
            self.newrect = True
            if self.largePic:
                x0, y0 = round(x0 * self.ratio), round(y0 * self.ratio)
                x1, y1 = round(x1 * self.ratio), round(y1 * self.ratio)
            self.rect = (min(x0, x1), min(y0, y1), abs(x0 - x1), abs(y0 - y1))

    def addMask(self, mask):
        if self.largePic:
            mask = cv2.resize(mask, self.newsize)
        self.gbcmask[mask > 127] = 1
        self.drawmask = True

    def removeMask(self, mask):
        if self.largePic:
            mask = cv2.resize(mask, self.newsize)
        self.gbcmask[mask > 127] = 0
        self.drawmask = True

    def setIter(self, iterk):
        if 0 < iterk <= 5:
            self.iterk = round(iterk)

    def edgeModify(self, diak=None, erok=None, blurk=None):
        if diak is not None:
            self.diak = diak
        if erok is not None:
            self.erok = erok
        if blurk is not None:
            self.blurk = blurk
        self.output_mask_f = self.output_mask.copy()
        if not self.firstRun:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            if self.diak > 0:
                self.output_mask_f = cv2.dilate(self.output_mask_f, kernel, iterations=self.diak)
            if self.erok > 0:
                self.output_mask_f = cv2.erode(self.output_mask_f, kernel, iterations=self.erok)
            if self.blurk > 1:
                if self.blurk % 2 == 0:
                    self.blurk += 1
                self.output_mask_f = cv2.GaussianBlur(self.output_mask_f, (self.blurk, self.blurk), 0)

        if self.largePic:
            self.output_mask_f = cv2.resize(self.output_mask_f, self.oldsize)

    def getMask(self):
        return self.output_mask_f
