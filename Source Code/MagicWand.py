from FansWheels import *


class MWand:
    def __init__(self, img, x=None, y=None, ld=None, ud=None):
        self.img = img.copy()
        maxsize = 1024
        if max(self.img.shape)>maxsize:
            self.largePic = True
            self.ratio = maxsize / max(self.img.shape)
            self.oldsize = (self.img.shape[1],self.img.shape[0])
            newh,neww = round(self.img.shape[0]*self.ratio),round(self.img.shape[1]*self.ratio)
            self.newsize = (neww,newh)
            self.img = cv2.resize(self.img,self.newsize)
        else:
            self.ratio = 1
            self.largePic = False
            self.newsize = (self.img.shape[1], self.img.shape[0])
            self.oldsize = (self.img.shape[1], self.img.shape[0])

        self.img = blend_3c(self.img)
        self.w,self.h = self.newsize[0],self.newsize[1]
        self.total_mask = np.zeros([self.h, self.w], dtype=np.uint8)
        self.output_mask_f = self.total_mask.copy()
        self.firstRun = True

        self.fColor = (255, 255, 255)
        self.lowDiff = (50, 50, 50)
        self.upDiff = (50, 50, 50)

        self.diak = 1
        self.erok = 1
        self.blurk = 1

        if (ld is not None) and (ud is not None):
            self.setDiff(ld,ud)
        if (x is not None) and (y is not None):
            self.update(x,y)

    def update(self, x=0, y=0, ld=None, ud=None,INV=False):
        self.firstRun = False
        if  self.largePic:
            x,y = int(round(x*self.ratio)),int(round(y*self.ratio))
        if (ld is not None) and (ud is not None):
            self.setDiff(ld,ud)
        mask_padded = np.zeros([self.h + 2, self.w + 2], dtype=np.uint8)
        cv2.floodFill(self.img.copy(), mask_padded, (x, y), self.fColor, self.lowDiff, self.upDiff,
                      cv2.FLOODFILL_FIXED_RANGE)
        self.total_mask = (mask_padded[1:1 + self.h, 1:1 + self.w]) * 255
        self.edgeModify(self.diak, self.erok,self.blurk)

    def edgeModify(self, diak=None, erok=None, blurk=None):
        if diak is not None:
            self.diak = diak
        if erok is not None:
            self.erok = erok
        if blurk is not None:
            self.blurk = blurk
        self.output_mask_f = self.total_mask.copy()
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

    def setDiff(self, ld, ud):
        self.lowDiff = (ld, ld, ld)
        self.upDiff = (ud, ud, ud)

    def getMask(self):
        return self.output_mask_f
