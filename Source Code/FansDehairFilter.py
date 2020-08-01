#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FansWheels import *

"""
Fanseline's Dehairing & Skin Smoothening Filter
by FerryYoungFan - Twitter @FanKetchup / @FanBuckle
Project start: June 12, 2020
Ver1.0: June 13, 2020
Ver1.1: June 14, 2020
Ver2.0: June 21, 2020
Ver2.1: June 23, 2020
Ver2.2: June 25, 2020
"""


class FDehair:

    def __init__(self, input_img, mask_total):
        self.img = input_img.copy()
        self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.output = input_img.copy()
        self.firstrun = True
        if len(mask_total[mask_total > 0]) == 0 or len(mask_total[mask_total < 255]) == 0:
            self.mask_total = None
        else:
            self.mask_total = mask_total

        self.max_mediank = int(round(max(self.img.shape[0], self.img.shape[1]) * 0.03))
        if self.max_mediank > 120:
            self.max_mediank = 120
        self.mediank = int(round(self.max_mediank * 0.2))

        self.img_median = np.zeros(input_img.shape, np.uint8)

        self.img_diff = np.zeros(input_img.shape, np.uint8)
        self.th_min, self.th_max, self.thi_min, self.thi_max, self.soft = 5, 150, 5, 150, 25

        self.img_binmask = np.zeros(input_img.shape, np.uint8)

        self.default_v = [self.mediank, self.th_min, self.th_max, self.thi_min, self.thi_max, self.soft]

    def start(self):
        self.firstrun = False
        self.median(self.mediank)  # Start processing

    def median(self, median_para=41):
        """
        Customized median filter
        :param median_para: ksize for median filter in cv2
        """
        # Limitation of the median filter's ksize (para)
        self.mediank = int(median_para)
        if self.mediank < 1:
            self.mediank = 1
        elif self.mediank > self.max_mediank:
            self.mediank = self.max_mediank

        # Median Filter ksize (para) must be an ODD Value
        if self.mediank % 2 == 0:
            self.mediank += 1
        if self.mediank > 1:
            self.img_median = cv2.medianBlur(self.img, self.mediank)  # Must be an ODD VALUE
            self.diffmap(self.th_min, self.th_max, self.thi_min, self.thi_max, self.soft)
        else:
            self.output = self.img

    def diffmap(self, th_min=5, th_max=150, thi_min=5, thi_max=150, soft=0):
        # Image difference with threshold
        self.th_min, self.th_max, self.thi_min, self.thi_max, self.soft = th_min, th_max, thi_min, thi_max, soft
        img_median_gray = cv2.cvtColor(self.img_median, cv2.COLOR_BGR2GRAY)

        temp_diff = cv2.subtract(img_median_gray, self.img_gray)  # Dark edge (texture)
        temp_diff_inv = cv2.subtract(self.img_gray, img_median_gray)  # Bright edge (texture)

        # Using LUT for faster double-sided threshold
        lookUpTable = self.getTable(self.th_min, self.th_max, self.soft)
        lookUpTableI = self.getTable(self.thi_min, self.thi_max, self.soft)
        temp_diff = cv2.LUT(temp_diff, lookUpTable)
        temp_diff_inv = cv2.LUT(temp_diff_inv, lookUpTableI)

        self.img_binmask = cv2.add(temp_diff, temp_diff_inv)
        self.blend()

    def blend(self):
        if self.mask_total is None:
            self.output = blend_3c(blend_combine(blend_4c(self.img_median, self.img_binmask), self.img))
        else:
            self.output = blend_3c(
                blend_combine(blend_4c(blend_4c(self.img_median, self.img_binmask), self.mask_total), self.img))

    def result(self):
        return self.output

    def getTable(self, th_min, th_max, soft=0):
        lookUpTable = np.zeros((1, 256), np.uint8)
        soft += 1
        for i in range(256):
            # if th_min - soft <= i < th_min:
            #     lookUpTable[0, i] = (i - th_min + soft) * 255 / soft
            if th_min <= i <= th_max:
                lookUpTable[0, i] = 255
            elif th_max < i <= th_max + soft - 1:
                lookUpTable[0, i] = 255 - (i - th_max - soft) * 255 / soft
        return lookUpTable

    def setDefault(self):
        self.mediank, self.th_min, self.th_max, self.thi_min, self.thi_max, self.soft = self.default_v[0], \
                                                                                        self.default_v[1], \
                                                                                        self.default_v[2], \
                                                                                        self.default_v[3], \
                                                                                        self.default_v[4], \
                                                                                        self.default_v[5]
