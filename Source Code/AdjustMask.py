#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FansWheels import *


class MaskAdj:
    def __init__(self, current_img, current_mask):
        self.img = current_img.copy()
        self.mask = current_mask.copy()
        self.mask_f = current_mask.copy()
        self.view = preview_mask(self.img, self.mask)

        self.firstRun = True

        self.diak = 0
        self.erok = 0
        self.blurk = 1
        self.alpha = 100

    def edgeModify(self, diak=None, erok=None, blurk=None, alpha=None):
        if diak is not None:
            self.diak = diak
        if erok is not None:
            self.erok = erok
        if blurk is not None:
            self.blurk = blurk
        if alpha is not None:
            self.alpha = alpha

        self.firstRun = False

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
        if self.alpha < 100:
            fac = int(255 - round(255 * self.alpha / 100))
            submat = np.ones((self.mask.shape[0], self.mask.shape[1]), dtype=np.uint8) * fac
            self.mask_f = cv2.subtract(self.mask_f, submat)

        self.view = preview_mask(self.img, self.mask_f)

    def getMask(self):
        return self.mask_f

    def getView(self):
        return self.view
