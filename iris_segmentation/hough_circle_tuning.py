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
fname = ''

## TESTING PARAMETERS ##
cv2.namedWindow('hough', cv2.CV_WINDOW_AUTOSIZE)
cv2.createTrackbar('minD', 'hough', 80, 100, nothing)
cv2.createTrackbar('p1', 'hough', 10, 100, nothing)
cv2.createTrackbar('p2', 'hough', 10, 100, nothing)
cv2.createTrackbar('minR', 'hough', 1, 20, nothing)
cv2.createTrackbar('maxR', 'hough', 10, 100, nothing)


## TUNING PARAMETERS ##
hough_params = dict( #dp = 1, #inverse ratio of accumulator : img resolution (1 for same res as img, 2 for 1/2 width & height of img)
                     # min_dist = 20,
                     param1 = p1, #upper threshold for
                     param2 = p2, #accumulator threshold
                     minRadius = minR, #min circle radius
                     maxRadius = maxR #max circle radius
                     )

canny_params = dict( threshold1 = 10,
                     threshold2 = 200,
                     apertureSize = 3,
                     L2gradient = True )


if __name__ == '__main__':

    try:
        # get image specified in command line argument
        fname = sys.argv[1]
        img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
    except:
        # get hard coded image if not specified...should be in same directory as executed code
        fname = 'images/05462d99.tiff'
        img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)

    # smoothing - TODO: try other filters like Canny Edge etc.
    bimg = cv2.GaussianBlur(img, (3, 3), 0)
    bimg = cv2.Canny(bimg, **canny_params)
    # cv2.imshow('filtered', bimg)

    # make a duplicate color image
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    ## TODO: testing parameters on fly ##
    while (1):

        # get circles
        circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, dp, minD, param1=p1, param2=p2, minRadius=minR, maxRadius=maxR)
        if circles is not None:
            for i in circles[0,:]:
                cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        else:
            print 'No circles found!'
        # display
        cv2.imshow('hough', cimg)
        cv2.waitKey(100)

        minD = cv2.getTrackbarPos('minD', 'hough')
        p1 = cv2.getTrackbarPos('p1', 'hough')
        p2 = cv2.getTrackbarPos('p2', 'hough')
        minR = cv2.getTrackbarPos('minR', 'hough')
        maxR = cv2.getTrackbarPos('maxR', 'hough')

        # reset image
        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        # print 'vals: ' + str(minD) + ', ' + str(p1) + ', ' + str(p2) + ', ' + str(minR) + ', ' + str(maxR)

        k = cv2.waitKey(30) & 0xff
        if k == 27: #escape key
            break
        elif k == ord('s'):
            cv2.imwrite('./output/'+fname,cimg)

    cv2.destroyAllWindows()
