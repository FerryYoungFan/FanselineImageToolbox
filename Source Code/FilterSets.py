from FansWheels import *

"""
Just Some Common Filters
by FerryYoungFan - Twitter @FanKetchup / @FanBuckle
Ver1.1: June 30, 2020
"""

class FilterSets:
    def __init__(self, img, mask):
        self.firstRun = True
        self.mode = 0
        self.img = blend_3c(img)
        if len(mask[mask > 0]) == 0 or len(mask[mask < 255]) == 0:
            self.mask = None
        else:
            self.mask = mask

        self.img_out = None
        self.buffer = None
        self.buffer2 = None
        self.maskBuffer = None
        self.max_k = int(max(self.img.shape[0], self.img.shape[1]) * 0.03)
        if self.max_k > 150:
            self.max_k = 150

    def skinPolish(self, v_d, v_s, opacity=100, white=0, refresh=True):
        self.firstRun = False
        if refresh or self.buffer is None:
            diameter = int(round(v_d * self.max_k / 100))
            sigColor = int(round(v_s * self.max_k / 100))
            sigSpace = int(round(v_s * self.max_k / 100))
            if diameter > 1:
                self.buffer = cv2.bilateralFilter(self.img, diameter, sigColor, sigSpace)
            else:
                self.buffer = self.img.copy()
        self.buffer2 = blend_3c(
            cv2.addWeighted(self.buffer[:, :, 2], 0.6, self.buffer[:, :, 1], 0.4, 0))  # Orange Channel
        alpha = opacity / 100.0
        wv = white / 500.0
        self.img_out = cv2.addWeighted(cv2.addWeighted(self.buffer, alpha, self.img, 1 - alpha, 0), 1, self.buffer2, wv,
                                       0)

    def skinGlow(self, v_k, opacity=100, glow=50):
        self.firstRun = False
        blurk = int(round(v_k * self.max_k / 50))
        alpha = opacity / 100.0
        offset = glow / 500.0
        if blurk % 2 == 0:
            blurk += 1
        if blurk > 1:
            img_blur = cv2.GaussianBlur(self.img, (blurk, blurk), 0)
            self.buffer = cv2.addWeighted(img_blur, alpha + offset, self.img, 1 - alpha, 0)
            self.img_out = self.buffer
        else:
            self.img_out = self.img

    def bilateral(self, v_d, sharpen, refresh=True):
        self.firstRun = False
        alpha = -sharpen / 100.0
        if refresh or self.buffer is None:
            diameter = int(round(v_d * self.max_k / 200))
            sigColor = self.max_k
            sigSpace = self.max_k
            if diameter > 1:
                self.buffer = cv2.bilateralFilter(self.img, diameter, sigColor, sigSpace)
            else:
                self.buffer = self.img.copy()
        self.img_out = cv2.addWeighted(self.buffer, alpha, self.img, 1 - alpha, 0)

    def bilateral2(self, v_d, v_c, v_s, sharpen, refresh=True):
        self.firstRun = False
        alpha = -sharpen / 100.0
        if refresh or self.buffer is None:
            diameter = int(round(v_d * self.max_k / 100))
            sigColor = int(round(v_c * self.max_k / 100))
            sigSpace = int(round(v_s * self.max_k / 100))
            if diameter > 1:
                self.buffer = cv2.bilateralFilter(self.img, diameter, sigColor, sigSpace)
            else:
                self.buffer = self.img.copy()
        self.img_out = cv2.addWeighted(self.buffer, alpha, self.img, 1 - alpha, 0)

    def median(self, v_k, sharpen):
        blurk = int(round(v_k * self.max_k / 80))
        alpha = -sharpen / 100.0
        if blurk < 1:
            blurk = 1
        if blurk % 2 == 0:
            blurk += 1
        self.buffer = cv2.medianBlur(self.img, blurk)
        self.img_out = cv2.addWeighted(self.buffer, alpha, self.img, 1 - alpha, 0)

    def Gaussian(self, v_k, sig, sharpen):
        blurk = int(round(v_k * self.max_k / 80))
        sigma = int(round(sig * self.max_k / 800))
        alpha = -sharpen / 100.0
        if blurk < 1:
            blurk = 1
        if blurk % 2 == 0:
            blurk += 1
        self.buffer = cv2.GaussianBlur(self.img, (blurk, blurk), sigma)
        self.img_out = cv2.addWeighted(self.buffer, alpha, self.img, 1 - alpha, 0)

    def boxBlur(self, v_k, sharpen):
        blurk = int(round(v_k * self.max_k / 80))
        alpha = -sharpen / 100.0
        if blurk < 1:
            blurk = 1
        if blurk % 2 == 0:
            blurk += 1
        self.buffer = cv2.blur(self.img, (blurk, blurk))
        self.img_out = cv2.addWeighted(self.buffer, alpha, self.img, 1 - alpha, 0)

    def simpleSharpen(self, opacity):
        alpha = opacity / 100.0
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        self.buffer = cv2.filter2D(self.img, -1, kernel)
        self.img_out = cv2.addWeighted(self.buffer, alpha, self.img, 1 - alpha, 0)

    def pixelation(self, v_pix):
        h, w = self.img.shape[0], self.img.shape[1]
        minRatio = 0.001
        ratio = 1 - (1 - minRatio) * (np.power(v_pix / 100, 1 / 30))
        new_h, new_w = int(round(h * ratio)), int(round(w * ratio))
        if new_h < 2:
            new_h = 2
        if new_w < 2:
            new_w = 2
        print(new_h, new_w)
        self.buffer = cv2.resize(self.img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        self.img_out = cv2.resize(self.buffer, (w, h), interpolation=cv2.INTER_NEAREST)

    def setVignette(self):

        maxsize = 1024
        if max(self.img.shape) > maxsize:

            ratio = maxsize / max(self.img.shape)
            oldsize = (self.img.shape[1], self.img.shape[0])
            newh, neww = int(round(self.img.shape[0] * ratio)), int(round(self.img.shape[1] * ratio))
            blurk = 541
            self.maskBuffer = np.ones((newh, neww), np.uint8) * 255
            h_center = int(round(newh / 2))
            w_center = int(round(neww / 2))
            center = (w_center, h_center)
            axes = (int(round(w_center*0.8)),int(round(h_center*0.8)))
            cv2.ellipse(self.maskBuffer, center, axes, 0, 0, 360, 0, -1)
            self.maskBuffer = cv2.GaussianBlur(self.maskBuffer, (blurk, blurk), 0)
            self.maskBuffer = cv2.resize(self.maskBuffer,oldsize)
        else:
            blurk = int(round(self.max_k)*20)
            if blurk < 1:
                blurk = 1
            if blurk % 2 == 0:
                blurk += 1
            h, w = self.img.shape[0], self.img.shape[1]
            self.maskBuffer = np.ones((h,w),np.uint8)*255
            h_center = int(round(h/2))
            w_center = int(round(w / 2))
            center = (w_center,h_center)
            axes = (int(round(w_center * 0.8)), int(round(h_center * 0.8)))
            cv2.ellipse(self.maskBuffer,center,axes,0,0,360,0,-1)
            self.maskBuffer = cv2.GaussianBlur(self.maskBuffer,(blurk,blurk),0)


    def vignette(self,v_vig):
        if v_vig > 0:
            opacity =  (v_vig/100)*0.3
            self.buffer = blend_3c(np.asarray(self.maskBuffer*opacity,np.uint8))
            self.img_out = cv2.subtract(self.img,self.buffer)
        else:
            opacity = (-v_vig / 100) * 0.3
            self.buffer = blend_3c(np.asarray(self.maskBuffer * opacity, np.uint8))
            self.img_out = cv2.add(self.img, self.buffer)


    def denoise(self,v_h,v_hc):
        h = v_h*3/100
        hc = v_hc*3/100
        self.img_out = cv2.fastNlMeansDenoisingColored(self.img,None,h,hc,7,21)

    def getImage(self):
        if self.img_out is None:
            return self.img
        else:
            if self.mask is None:
                return self.img_out
            else:
                return blend_combine(blend_4c(self.img_out, self.mask), self.img)


if __name__ == '__main__':
    # file_ = r"./Sample/香菇腿子原图.jpg"
    file_ = r"./Sample/Ai-Shinozaki-24.jpg"
    imgt = cv_imread(file_)
