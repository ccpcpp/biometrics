#!/usr/bin/env python
import sys
import cv2
import cv2.cv as cv
import numpy as np

# callback for trackbar
def nothing(x):
    pass

## GLOBAL VARS ##
dp = 1
minD = 80
p1 = 90
p2 = 30
minR = 30
maxR = 150
loop = 0

## TESTING PARAMETERS ##
cv2.namedWindow('hough')
cv2.createTrackbar('minD', 'hough', 1, 100, nothing)
cv2.createTrackbar('p1', 'hough', 1, 100, nothing)
cv2.createTrackbar('p2', 'hough', 1, 100, nothing)
cv2.createTrackbar('minR', 'hough', 0, 20, nothing)
cv2.createTrackbar('maxR', 'hough', 1, 100, nothing)


## TUNING PARAMETERS ##
hough_params = dict( #dp = 1, #inverse ratio of accumulator : img resolution (1 for same res as img, 2 for 1/2 width & height of img)
                     # min_dist = 20,
                     param1 = p1, #upper threshold for
                     param2 = p2, #accumulator threshold
                     minRadius = minR, #min circle radius
                     maxRadius = maxR #max circle radius
                     )

canny_params = dict( threshold1 = 200,
                     threshold2 = 250,
                     apertureSize = 3,
                     L2gradient = True )


if __name__ == '__main__':

    try:
        # get image specified in command line argument
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    except:
        # get hard coded image if not specified...should be in same directory as executed code)
        img = cv2.imread('02463d1926.tiff', cv2.IMREAD_GRAYSCALE)

    # smoothing - TODO: try other filters like Canny Edge etc.
    bimg = cv2.medianBlur(img, 5)
    bimg = cv2.Laplacian(bimg,cv2.CV_8U)
    # bimg = cv2.Canny(img, **canny_params)
    cv2.imshow('filtered', bimg)

    # make a duplicate color image
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # compute hough circles
    circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, dp, minD, **hough_params)

    for i in circles[0,:]:
        # draw circles on color image
        cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        
    ## TODO: testing parameters on fly ##
    while (1):
        # cv2.imshow('hough', cimg)
        cv2.waitKey(0)
        minD = cv2.getTrackbarPos('minD', 'hough')
        p1 = cv2.getTrackbarPos('p1', 'hough')
        p2 = cv2.getTrackbarPos('p2', 'hough')
        minR = cv2.getTrackbarPos('minR', 'hough')
        maxR = cv2.getTrackbarPos('maxR', 'hough')
        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, dp, minD, param1=p1, param2=p2, minRadius=minR, maxRadius=maxR) #, **hough_params)
        
        if not circles:
            pass
        else:
            for i in circles[0,:]:
                cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        
        k = cv2.waitKey(30) & 0xff
        if k == 27: #escape key
            break
        elif k == ord('s'):
            cv2.imwrite('hough_img.png',cimg)
        
    ## DISPLAY IMAGES ##
    # cv2.imshow('original', img)

    cv2.destroyAllWindows()
