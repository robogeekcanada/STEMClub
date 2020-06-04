#delaunay.py

import cv2
import numpy as np
import random

WHITE = (255,255,255)
RED = (0,0,255)

font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 0.5


#Draw a point
def draw_point(img, p, color):
    cv2.circle(img, p, 2, color, -1, cv2.LINE_AA, 0)

def label_point(img, p, label):
    cv2.putText(img, label ,p, font, font_size, WHITE ,1)

#Check if a point inside a rectangle
def rect_contains(rect, point):
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True    

#Draw delaunay triangles
def draw_delaunay(img, subdiv, delaunay_color):

    triangleList = subdiv.getTriangleList()
    size = img.shape

    r = (0,0, size[1], size[0])

    for t in triangleList:

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rect_contains(r,pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
            cv2.line(img, pt1, pt2, delaunay_color, 1)
            cv2.line(img, pt2, pt3, delaunay_color, 1)
            cv2.line(img, pt3, pt1, delaunay_color, 1)  

if __name__ == '__main__':

    win_delaunay = "Delaunay"
    animate = True

    img = cv2.imread("obama.jpg")
    img_orig = img.copy()

    #Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0,0,size[1],size[0])

    subdiv = cv2.Subdiv2D(rect)
    points = []

    with open("obama.txt") as file:
        for line in file:

            x,y = line.split()
            points.append((int(x), int(y)))

    for counter, p in enumerate (points,1):
        subdiv.insert(p)
        #print(p)
        draw_point(img, p, RED)
        label_point(img, p, str(counter))

    #draw_delaunay(img, subdiv, WHITE)
        

    cv2.imshow(win_delaunay, img)
    cv2.waitKey(0)
                          
                        
                          
        

    
