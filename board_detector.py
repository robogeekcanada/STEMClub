#This progam uses two methods to detect checkers board pieces
#circle detection and template matching

import numpy as np
import cv2
import time


def find_circles(image):

    copy_image = np.copy(image)
    gray = cv2.cvtColor(copy_image, cv2.COLOR_BGR2GRAY)

    # detect circles in the image
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20, param1=50,param2=20,minRadius=20,maxRadius=30)

    circle_counter = 0
    
    # ensure at least some circles were found
    if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
     
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(copy_image, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(copy_image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    circle_counter +=1

    
    missing_circles = 24 - circle_counter
    print ("Number of circles found", circle_counter, "and", missing_circles, "missing circle(s)") 

    return circles, copy_image       


def draw_boardboundary(image):

    w, h = image.shape[:2]
    x1 = 160
    y1 = 18
    x2 = x1 + 100*8
    y2 = y1 + 82*8
    
    cv2.rectangle(image, (x1,y1),(x2,y2),(255,0,0), 3)


def main():

    image = cv2.imread('checkers_board.jpg')
    draw_boardboundary(image)

    circles, circles_image = find_circles(image)

    #Resize image to help display
    resize_circles_image = cv2.resize(circles_image,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)

    cv2.imshow("Circles detection", resize_circles_image)
    
    cv2.waitKey(1)

main()

