#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FansWheels import *

"""
Fanseline's Image Color Adjust Method
by FerryYoungFan - Twitter @FanKetchup / @FanBuckle
Ver1.5: June 29, 2020
"""


class ImageAdj:
    def __init__(self, img, mask=None):
        self.img = blend_3c(img)
        self.img_out = self.img.copy()
        self.img_hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        if mask is not None:
            if len(mask[mask > 0]) == 0 or len(mask[mask < 255]) == 0:
                self.mask = None
            else:
                self.mask = mask
        else:
            self.mask = None

    def basicAdj(self, bright=0, contrast=0, saturation=0, warm=0, magenta=0, highlight=0, shadow=0):

        bright = np.clip(bright, -100, 100) / 2
        contrast = np.clip(contrast, -100, 100) / 2
        saturation = np.clip(saturation, -100, 100)
        highlight = np.clip(highlight, -100, 100)
        shadow = np.clip(shadow, -100, 100)

        if saturation != 0:
            alpha = 1.0 + saturation / 100
            img_hsv_temp = self.img_hsv.copy()
            img_hsv_temp[..., 1] = np.asarray(np.clip(self.img_hsv[..., 1] * alpha, 0, 255), dtype=np.uint8)
            img_temp = cv2.cvtColor(img_hsv_temp, cv2.COLOR_HSV2BGR)
        else:
            img_temp = self.img.copy()

        gamma_b = pow(2, -(bright - warm / 2 + magenta / 3) * 2 / 100)
        gamma_g = pow(2, -(bright - magenta / 3) * 2 / 100)
        gamma_r = pow(2, -(bright + warm / 2 + magenta / 3) * 2 / 100)
        beta = pow(2, contrast / 100)
        lookUpTableb = np.zeros((1, 256), np.uint8)
        lookUpTableg = np.zeros((1, 256), np.uint8)
        lookUpTabler = np.zeros((1, 256), np.uint8)

        gamma_hl = pow(2, -highlight * 2 / 100)
        gamma_sd = pow(2, -shadow * 2 / 100)

        midpoint = int(31 + (1 - (highlight + shadow + 200) / 400) * (255 - 63))
        print(midpoint)

        for i in range(midpoint):
            # gamma = ((gamma/0.25)^2)*0.25
            fac = 255.0 / midpoint
            g_b = pow(pow(i / 256.0, gamma_b) * fac, gamma_sd) / fac
            g_g = pow(pow(i / 256.0, gamma_g) * fac, gamma_sd) / fac
            g_r = pow(pow(i / 256.0, gamma_r) * fac, gamma_sd) / fac
            lookUpTableb[0, i] = np.clip((g_b * 255.0 - midpoint) * beta + midpoint, 0, 255)
            lookUpTableg[0, i] = np.clip((g_g * 255.0 - midpoint) * beta + midpoint, 0, 255)
            lookUpTabler[0, i] = np.clip((g_r * 255.0 - midpoint) * beta + midpoint, 0, 255)

        for i in range(midpoint, 256):
            # gamma = (1-(-gamma*4+4)^(1/gamma_hl))*0.25+0.75
            fac = 255.0 / (255 - midpoint)
            g_b = (1 - pow(-pow(i / 256.0, gamma_b) * fac + fac, (1 / gamma_hl))) / fac + 1.0 - (1 / fac)
            g_g = (1 - pow(-pow(i / 256.0, gamma_g) * fac + fac, (1 / gamma_hl))) / fac + 1.0 - (1 / fac)
            g_r = (1 - pow(-pow(i / 256.0, gamma_r) * fac + fac, (1 / gamma_hl))) / fac + 1.0 - (1 / fac)
            lookUpTableb[0, i] = np.clip((g_b * 255.0 - midpoint) * beta + midpoint, 0, 255)
            lookUpTableg[0, i] = np.clip((g_g * 255.0 - midpoint) * beta + midpoint, 0, 255)
            lookUpTabler[0, i] = np.clip((g_r * 255.0 - midpoint) * beta + midpoint, 0, 255)
        # for i in range(256): # Old Version
        # lookUpTableb[0, i] = np.clip((pow(i / 255.0, gamma_b) * 255.0 - 128.0) * beta + 128.0, 0, 255)
        # lookUpTableg[0, i] = np.clip((pow(i / 255.0, gamma_g) * 255.0 - 128.0) * beta + 128.0, 0, 255)
        # lookUpTabler[0, i] = np.clip((pow(i / 255.0, gamma_r) * 255.0 - 128.0) * beta + 128.0, 0, 255)
        # lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

        resb = cv2.LUT(img_temp[:, :, 0], lookUpTableb)
        resg = cv2.LUT(img_temp[:, :, 1], lookUpTableg)
        resr = cv2.LUT(img_temp[:, :, 2], lookUpTabler)

        if self.mask is None:
            self.img_out = cv2.merge((resb, resg, resr))
        else:
            self.img_out = blend_combine(blend_4c(cv2.merge((resb, resg, resr)), self.mask), blend_4c(self.img))

    def getImage(self):
        return self.img_out
