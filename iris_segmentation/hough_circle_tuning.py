#!/usr/bin/env python
import sys
import os.path
import cv2
import cv2.cv as cv

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

cannyParams = dict(    threshold1 = 10, #first threshold for hysteresis
                        threshold2 = 200, #second threshold for hysteresis
                        apertureSize = 3, #Sobel aperture
                        L2gradient = True #use more accurate gradient
                        )

## GUI CALLBACK FUNCTIONS ##
def houghCbA(x):
    global houghParamsA
    houghParamsA['dp'] = cv2.getTrackbarPos('dp', 'houghA')
    houghParamsA['minDist'] = cv2.getTrackbarPos('minD', 'houghA')
    houghParamsA['param1'] = cv2.getTrackbarPos('p1', 'houghA')
    houghParamsA['param2'] = cv2.getTrackbarPos('p2', 'houghA')
    houghParamsA['minRadius'] = cv2.getTrackbarPos('minR', 'houghA')
    houghParamsA['maxRadius'] = cv2.getTrackbarPos('maxR', 'houghA')
    return

def houghCbB(x):
    global houghParamsB
    houghParamsB['dp'] = cv2.getTrackbarPos('dp', 'houghB')
    houghParamsB['minDist'] = cv2.getTrackbarPos('minD', 'houghB')
    houghParamsB['param1'] = cv2.getTrackbarPos('p1', 'houghB')
    houghParamsB['param2'] = cv2.getTrackbarPos('p2', 'houghB')
    houghParamsB['minRadius'] = cv2.getTrackbarPos('minR', 'houghB')
    houghParamsB['maxRadius'] = cv2.getTrackbarPos('maxR', 'houghB')
    return

def cannyCb(x):
    global cannyParams
    cannyParams['threshold1'] = cv2.getTrackbarPos('t1', 'canny')
    cannyParams['threshold2'] = cv2.getTrackbarPos('t2', 'canny')
    cannyParams['apertureSize'] = cv2.getTrackbarPos('apSize', 'canny')

## PARAMETER GUI ##

# for canny edge parameters
cv2.namedWindow('canny', cv2.CV_WINDOW_AUTOSIZE)
cv2.createTrackbar('t1', 'canny', cannyParams.get('threshold1'), 255, cannyCb)
cv2.createTrackbar('t2', 'canny', cannyParams.get('threshold2'), 255, cannyCb)
cv2.createTrackbar('apSize', 'canny', cannyParams.get('apertureSize'), 5, cannyCb)


# for hough circle parameters
cv2.namedWindow('houghA', cv2.CV_WINDOW_AUTOSIZE)
cv2.createTrackbar('dp', 'houghA', houghParamsA.get('dp'), 5, houghCbA)
cv2.createTrackbar('minD', 'houghA', houghParamsA.get('minDist'), 500, houghCbA)
cv2.createTrackbar('p1', 'houghA', houghParamsA.get('param1'), 255, houghCbA)
cv2.createTrackbar('p2', 'houghA', houghParamsA.get('param2'), 255, houghCbA)
cv2.createTrackbar('minR', 'houghA', houghParamsA.get('minRadius'), 255, houghCbA)
cv2.createTrackbar('maxR', 'houghA', houghParamsA.get('maxRadius'), 255, houghCbA)

cv2.namedWindow('houghB', cv2.CV_WINDOW_AUTOSIZE)
cv2.createTrackbar('dp', 'houghB', houghParamsB.get('dp'), 5, houghCbB)
cv2.createTrackbar('minD', 'houghB', houghParamsB.get('minDist'), 500, houghCbB)
cv2.createTrackbar('p1', 'houghB', houghParamsB.get('param1'), 255, houghCbB)
cv2.createTrackbar('p2', 'houghB', houghParamsB.get('param2'), 255, houghCbB)
cv2.createTrackbar('minR', 'houghB', houghParamsB.get('minRadius'), 255, houghCbB)
cv2.createTrackbar('maxR', 'houghB', houghParamsB.get('maxRadius'), 255, houghCbB)


if __name__ == '__main__':

    try:
        # get image path from command line argument
        fname = sys.argv[1]
    except:
        # get hard coded image if not specified, relative to executed code
        fname = 'images/05462d99.tiff'
    
    # read in image
    img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)

    # smoothing
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    # cv2.imshow('Gaussian', blurred)

    # threshold
    # ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU)
    # cv2.imshow('thresh', thresh)

    # update output based on GUI parameters
    while (1):

        # duplicate original image in color for displaying circles
        cimgA = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cimgB = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

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
            print 'No circles found!'
        cv2.imshow('houghA', cimgA)

        # get big hough circles
        circles = cv2.HoughCircles(blurred, cv.CV_HOUGH_GRADIENT, **houghParamsB)
        if circles is not None:
            for i in circles[0,:]:
                cv2.circle(cimgA, (i[0], i[1]), i[2], (255, 0, 0), 2)
                cv2.circle(cimgB, (i[0], i[1]), i[2], (255, 0, 0), 2)
        else:
            print 'No circles found!'
        cv2.imshow('houghB', cimgB)

        # display images
        cv2.imshow('hough', cimgA)

        # print 'vals: ' + str(minD) + ', ' + str(p1) + ', ' + str(p2) + ', ' + str(minR) + ', ' + str(maxR)

        k = cv2.waitKey(30) & 0xff
        if k == 27: # wait for 'ESC' to exit loop
            break
        elif k == ord('s'): # wait for 's' to save
            head, tail = os.path.split(fname)
            print tail
            savePath = os.path.join('output', tail)
            cv2.imwrite(savePath, cimgA)
            print "saved image to '"+ savePath+'\'' 

    cv2.destroyAllWindows()
