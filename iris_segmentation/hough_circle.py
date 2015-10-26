#!/usr/bin/env python
import sys
import os.path
import cv2
import cv2.cv as cv
import numpy as np

## Usage

## DEFAULT PARAMETERS ##
houghParamsA = dict(    dp = 2, # ratio of image res to accumulator res
                        minDist = 500, #min dist btwn circle centers
                        param1 =  10, #28,#18, #22 28, #upper canny thresh
                        param2 = 22, #lower canny thresh
                        minRadius = 20, #34 #min circle radius
                        maxRadius =  123#95 #121 #max circle radius
                        )

houghParamsB = dict(    dp = 2, # ratio of image res to accumulator res
                        minDist = 500, #min dist btwn circle centers
                        param1 =  28,#40, #upper canny thresh
                        param2 = 24, #lower canny thresh
                        minRadius = 103, #min circle radius
                        maxRadius = 142 #142 #196 #max circle radius
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
        blurred = cv2.GaussianBlur(img, (9, 9), 0)

        # duplicate original image in color for displaying circles
        cimgA = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        # get big hough circles
        circles = cv2.HoughCircles(blurred, cv.CV_HOUGH_GRADIENT, **houghParamsB)
        if circles is not None:
            #for i in circles[0,:]:
            i = circles[0,0]
            cv2.circle(cimgA, (i[0], i[1]), i[2], (255, 0, 0), 2)
            ### updated max radius of small cirlce ####
            houghParamsA['maxRadius'] = int(i[2]*0.7)
            ### MASK #####
            mask = np.zeros(blurred.shape, dtype=np.uint8)
            cv2.circle(mask, (i[0], i[1]), i[2], (255,255,255), -1,8,0)
            
            blurred = blurred&mask
        else:
            print "No circles found!"

        # get small hough circles
        circles = cv2.HoughCircles(blurred, cv.CV_HOUGH_GRADIENT, **houghParamsA)
        if circles is not None:
            #for i in circles[0,:]:
            i = circles[0,0]
            cv2.circle(cimgA, (i[0], i[1]), i[2], (0, 255, 0), 2)
        else:
            print "No circles found!"

        # display images
        # cv2.imshow('hough', cimgA)
        # cv2.waitKey(0)

        # save image
        head, tail = os.path.split(img_path)
        savePath = os.path.join(saveDir, tail)
        #print "saving image to '"+ savePath+'\''
        cv2.imwrite(savePath, cimgA)

        cv2.destroyAllWindows()
