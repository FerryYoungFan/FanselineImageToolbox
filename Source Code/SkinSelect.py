from FansWheels import *


class SkinSelect:
    def __init__(self, img):
        self.firstRun = True
        self.mode = 0 # 0-color range, 1-otsu
        self.img = blend_3c(img)
        maxsize = 2048
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

        self.mask = np.zeros([self.img.shape[0], self.img.shape[1]], dtype=np.uint8)
        self.mask_f = np.zeros(self.oldsize, dtype=np.uint8)

        self.diak, self.erok, self.bluredge = 0, 0, 0

        self.ycrcb = cv2.cvtColor(self.img, cv2.COLOR_BGR2YCR_CB)
        (self.y_c, self.cr_c, self.cb_c) = cv2.split(self.ycrcb)

        self.hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV_FULL)
        (self.h_c, self.s_c, self.v_c) = cv2.split(self.hsv)

        self.thumbW, self.thumbH = 100,100
        self.thumb = np.zeros((self.thumbH,self.thumbW,3),np.uint8)


    def otsuSelect(self, blurk=5):
        """
        Skin Selector:
        Cr + Otsu Method
        """
        self.firstRun = False
        self.mode = 1
        if blurk > 1:
            if blurk % 2 == 0:
                blurk += 1
            cr_blur = cv2.GaussianBlur(self.cr_c, (blurk, blurk), 0)
            _, self.mask = cv2.threshold(cr_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        else:
            _, self.mask = cv2.threshold(self.cr_c, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    def HSVSelect(self):
        self.firstRun = False
        self.mode = 2
        lower = np.array([0, 48, 80], dtype="uint8")
        upper = np.array([40, 255, 255], dtype="uint8")
        self.mask = cv2.inRange(self.hsv, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        self.mask = cv2.erode(self.mask, kernel, iterations=2)
        self.mask = cv2.dilate(self.mask, kernel, iterations=2)


    def YCrCbSelect(self):
        self.firstRun = False
        self.mode = 3
        lower = np.array([0, 133, 77], np.uint8)
        upper = np.array([235, 173, 127], np.uint8)
        self.mask = cv2.inRange(self.ycrcb, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        self.mask = cv2.erode(self.mask, kernel, iterations=2)
        self.mask = cv2.dilate(self.mask, kernel, iterations=2)


    def colorRange(self, x, y, hdiff=15, sdiff=120, vdiff=120, soft=30):
        """
        Color range method for selecting skin
        :param x: sample x
        :param y: sample y
        :param hdiff: difference tolerance for H channel
        :param sdiff: difference tolerance for S channel
        :param vdiff: difference tolerance for V channel
        :param soft: soft edge (feathering)
        """
        print("run!")
        self.firstRun = False
        self.mode = 0
        if self.largePic:
            x, y = int(round(x * self.ratio)), int(round(y * self.ratio))
        h_se, s_se, v_se = self.h_c[y][x], self.s_c[y][x], self.v_c[y][x]
        self.genThumb(self.img[y][x])
        h_diff = self.h_c - h_se
        s_diff = self.s_c - s_se
        v_diff = self.v_c - v_se
        lookUpTableh = self.getTable(hdiff, soft)
        lookUpTables = self.getTable(sdiff, soft)
        lookUpTablev = self.getTable(vdiff, soft)
        h_mask = cv2.LUT(h_diff, lookUpTableh)
        s_mask = cv2.LUT(s_diff, lookUpTables)
        v_mask = cv2.LUT(v_diff, lookUpTablev)
        self.mask = cv2.addWeighted(cv2.addWeighted(v_mask,0.5, s_mask,0.5,0),0.4, h_mask,1.0,0)

    def getTable(self, diff, soft):
        lookUpTable = np.zeros((1, 256))
        for i in range(256):
            if i <= diff:
                lookUpTable[0, i] = 255.0
            elif diff < i <= diff + soft:
                lookUpTable[0, i] = 255.0 - 255.0 * (i - diff) / soft
            else:
                lookUpTable[0, i] = 0.0
        return np.asarray(lookUpTable, np.uint8)

    def updateEdge(self, diak=None, erok=None, bluredge=None):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        self.setEdge(diak, erok, bluredge)
        self.mask_f = self.mask.copy()
        if self.diak > 0:
            self.mask_f = cv2.dilate(self.mask_f, kernel, iterations=self.diak)
        if self.erok > 0:
            self.mask_f = cv2.erode(self.mask_f, kernel, iterations=self.erok)
        if self.bluredge > 1:
            print("start blur")
            self.mask_f = cv2.GaussianBlur(self.mask_f, (self.bluredge, self.bluredge), 0)
            print("stop blur")
        self.largepicResize()

    def setEdge(self, diak=None, erok=None, bluredge=None):
        if diak is not None and diak >= 0:
            self.diak = int(round(diak))
        if erok is not None and erok >= 0:
            self.erok = int(round(erok))
        if bluredge is not None and bluredge >= 0:
            self.bluredge = int(round(bluredge))
            if self.bluredge % 2 == 0:
                self.bluredge += 1

    def largepicResize(self):
        if self.largePic:
            self.mask_f = cv2.resize(self.mask_f, self.oldsize)

    def getMask(self):
        return self.mask_f

    def genThumb(self,color):
        thumb_B = np.zeros((self.thumbH, self.thumbW), np.uint8) + color[0]
        thumb_G = np.zeros((self.thumbH, self.thumbW), np.uint8) + color[1]
        thumb_R = np.zeros((self.thumbH, self.thumbW), np.uint8) + color[2]
        self.thumb = cv2.merge((thumb_B,thumb_G,thumb_R))

    def getThumb(self):
        return self.thumb


