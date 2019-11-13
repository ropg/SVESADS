#!/usr/bin/env python
import sys
import numpy as np
import cv2


lower_color = np.array([240, 222, 173])
upper_color = np.array([255, 255, 255])


img = cv2.imread(sys.argv[1])
height, width, channels = img.shape


img_bw = cv2.inRange(
        img,
        lower_color,
        upper_color)

#img_edged = cv2.Canny(img_bw, 30, 200)
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
#img_dilated = cv2.dilate(img_bw, kernel)

contours, hierarchy = cv2.findContours(
        img_bw,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE)


img_orig = img
canvas = np.zeros((height, width, 3), np.uint8)
count = 0
for c in contours:
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.024 * peri, True)
    corners = len(approx)
    if area > 2 and corners == 3:
        count += 1
        cv2.drawContours(img_orig, [approx,], -1, (0xff, 0xff, 0xff), -1)
        cv2.drawContours(img_orig, [c,],      -1, (0x00, 0x00, 0xff),  1)
        cv2.drawContours(canvas,   [approx,], -1, (0xff, 0xff, 0xff), -1)
        cv2.drawContours(canvas,   [c,],      -1, (0x00, 0x00, 0xff),  1)
print(count)


cv2.imshow('original', img_orig)
cv2.imshow('result',   canvas)

cv2.moveWindow('original', 0, 0)
cv2.moveWindow('result', 700, 0)
#cv2.moveWindow('original', 1500, 50)
#cv2.moveWindow('result',   2200, 50)


cv2.waitKey(0)
cv2.destroyAllWindows()
