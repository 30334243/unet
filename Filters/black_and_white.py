import cv2 as cv

import os

def global_bin(file, threshhold, path_out):
    img = cv.imread(file)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, img_out = cv.threshold(gray, threshhold, 255, cv.THRESH_BINARY)
    cv.imwrite(path_out, img_out)

def otsu(file, path_out):
    img = cv.imread(file)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, img_out = cv.threshold(gray, 255, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    cv.imwrite(path_out, img_out)

def gaussian_and_otsu(file, path_out):
    img = cv.imread(file,0)
    blur = cv.GaussianBlur(img, (5, 5), 0)
    ret, img_out = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    cv.imwrite(path_out, img_out)

def gaussian(file, path_out):
    img = cv.imread(file)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_out = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    cv.imwrite(path_out, img_out)

def mean(file, path_out):
    img = cv.imread(file)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_out = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
    cv.imwrite(path_out, img_out)

