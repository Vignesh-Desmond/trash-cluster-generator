# -*- coding: utf-8 -*-
"""ConvexHull.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R25DpMm5FHntGGCXKV111gHSr2L_8yEE
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def binary_thresh(img):
    img_copy = img.copy()
    _, thresh = cv2.threshold(img_copy, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    return thresh


def contour_finder(thresh, drawing=False):
    thresh_copy = thresh.copy()
    contours, hierarchy = cv2.findContours(
        thresh_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    if drawing:
        external = np.ones(thresh_copy.shape, dtype=np.uint8) * 255
        for cnt in range(len(contours)):
            if hierarchy[0][cnt][3] == -1:
                cv2.drawContours(external, contours, cnt, color=(0, 0, 0))
        return contours, external
    return contours


def convex_hull_gen(img, contours, thickness=1):
    external = np.ones(img.shape) * 255
    length = len(contours)
    templist = [contours[i] for i in range(length)]
    cont = np.vstack(templist)
    hull = cv2.convexHull(cont)
    uni_hull = []
    uni_hull.append(hull)
    cv2.drawContours(external, uni_hull, -1, (0, 0, 0), thickness=thickness)
    return external


def show(img, name: str):
    fig = plt.figure(figsize=(5, 5))
    ax = plt.subplot(111)
    plt.axis("off")
    ax.imshow(img, cmap="gray")
    fig.savefig(os.path.join(os.getcwd(), name), bbox_inches="tight")


def convex_hull_image(img, thickness=1):
    img_copy = img.copy()
    thresholded = binary_thresh(img_copy)
    contours = contour_finder(thresholded)
    drawing = convex_hull_gen(img_copy, contours, thickness=thickness)
    drawing_fill = convex_hull_gen(img_copy, contours, thickness=-1)
    return drawing, drawing_fill
