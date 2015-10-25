#!/usr/bin/env python
import sys
import os.path
import cv2
import cv2.cv as cv
import numpy as np


## DEFAULT PARAMETERS ##
houghParamsA = dict(    dp = 1, # ratio of image res to accumulator res
                        minDist = 500, #min dist btwn circle centers
                        param1 = 51, #upper canny thresh
                        param2 = 8, #lower canny thresh
                        minRadius = 62, #min circle radius
                        maxRadius = 195 #max circle radius
                        )

houghParamsB = dict(    dp = 1, # ratio of image res to accumulator res
                        minDist = 500, #min dist btwn circle centers
                        param1 = 69, #upper canny thresh
                        param2 = 8, #lower canny thresh
                        minRadius = 62, #min circle radius
                        maxRadius = 195 #max circle radius
                        )

if __name__ == '__main__':

    try:
        imgDir = sys.argv[1]
        saveDir = sys.argv[2]
        print "images: " + imgDir + ", output: " + saveDir
    except:
        print "no directory specified, using default: images output"
        imgDir = "images"
        saveDir = "batch_output"

    path = os.path.join(os.getcwd(), imgDir)

    for filename in os.listdir(path):
        if not filename.endswith('.tiff'): continue
        print "opening \'" + filename + "'"
        img_path = os.path.join(path, filename)

        # get image
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        # smoothing
        blurred = cv2.GaussianBlur(img, (5, 5), 0)
        # cv2.imshow('Gaussian', blurred)

        # threshold
        # ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU)
        # cv2.imshow('thresh', thresh)

        # duplicate original image in color for displaying circles
        cimgA = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        # # filter image
        # edge = cv2.Canny(blurred, **cannyParams)
        # cv2.imshow('canny', edge)
        # edge = cv2.Laplacian(blurred, cv2.CV_64F)
        # cv2.imshow('laplacian', edge)

        # get small hough circles
        circles = cv2.HoughCircles(blurred, cv.CV_HOUGH_GRADIENT, **houghParamsA)
        if circles is not None:
            for i in circles[0,:]:
                cv2.circle(cimgA, (i[0], i[1]), i[2], (0, 255, 0), 2)
        else:
            print "No circles found!"

        # get big hough circles
        circles = cv2.HoughCircles(blurred, cv.CV_HOUGH_GRADIENT, **houghParamsB)
        if circles is not None:
            for i in circles[0,:]:
                cv2.circle(cimgA, (i[0], i[1]), i[2], (255, 0, 0), 2)
        else:
            print "No circles found!"

        # display images
        # cv2.imshow('hough', cimgA)
        # cv2.waitKey(0)

        # save image
        head, tail = os.path.split(img_path)
        savePath = os.path.join(saveDir, tail)
        print "saving image to '"+ savePath+'\''
        cv2.imwrite(savePath, cimgA)

        cv2.destroyAllWindows()
