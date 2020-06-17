#parking_lot3b.py

import cv2
import numpy as np
from rs_test import *

WHITE = (255, 255, 255)

def rotate_car(img, center, angle, rotation_scale, output_scale):

    rotation_matrix = cv2.getRotationMatrix2D(center, angle, rotation_scale)
    img_rotated = cv2.warpAffine(img, rotation_matrix, output_scale)
   
    return img_rotated

def mask_and_crop(img, background, x, y, size):

    black = np.array([0,0,0])
    mask = cv2.inRange(img, black, black)
    
    masked_image = np.copy(img)
    masked_image[mask !=0] = [0,0,0]

    cropped_image = background[y:y+size[0], x:x+size[1]]
    cropped_image[mask == 0] = [0,0,0]
    output_image = cropped_image + masked_image

    return output_image

def set_car_position(x,y,direction):

    red_car = cv2.imread("red_car.png")
    h,w = red_car.shape[:2]
    center = (int(w/2), int(h/2))
    rotation_scale = 1.0
    output_scale = (int(w*1.0), int(h*1.0))
    angle = 0

    rotated_car = rotate_car(red_car, center,
                             direction*-1, rotation_scale, output_scale)

    size = rotated_car.shape
    background = cv2.imread("parking_lot.jpg")
    b2 = background.copy()

    translated_car = mask_and_crop(rotated_car, b2, x, y, size)
    background[y:y+size[0], x:x+size[1]] = translated_car

    cv2.imshow("Car rotation", background)


def main():

    print("Start program....")
    #set_car_position(0,0,30)

    start_x = 40
    start_y = 130
    start_yaw = np.deg2rad(90.0)

    end_x = 320
    end_y = 275
    end_yaw = np.deg2rad(115.0)

    curvature = 0.05
    step_size = 0.5

    px, py, pyaw, mode, clen = reeds_shepp_path_planning(start_x, start_y, start_yaw,
                                                         end_x, end_y, end_yaw, curvature,
                                                         step_size)

    for x,y,yaw in zip(px,py,pyaw):

        set_car_position(int(x), int(y), int(np.rad2deg(yaw)))
        cv2.waitKey(5)



if __name__ == '__main__':
    main()




##    # SECTION 1
##    #-----------------------------------------------------------------------
##    #
##
##    background = cv2.imread("parking_lot.jpg")
##    #cv2.imshow("Parking Lot", background)
##
##    b2 = background.copy()
##    empty_canvas = np.zeros((600,600,3), np.uint8)
##    empty_canvas[:,:] = WHITE
##
##    red_car = cv2.imread("red_car.png")
##    h,w = red_car.shape[:2]
##    center = (int(w/2), int(h/2))
##    rotation_scale = 1.0
##    output_scale = (int(w*1.0),int(h*1.0))
##
##    for angle in range(0,361,5):
##
##        background = cv2.imread("parking_lot.jpg")
##        b2 = background.copy()
##
##        rotated_car = rotate_car(red_car, center, angle*-1,
##                                 rotation_scale, output_scale)
##
##        (x,y) = (100,100)
##        size = rotated_car.shape
##        output_image = mask_and_crop(rotated_car, b2, x, y, size)
##
##        background[x:x+size[0], y:y+size[1]] = output_image
##
##        cv2.waitKey(50)
##        cv2.imshow("Car rotation", background)

##    # SECTION 2
##    #----------------------------------------------------------------------------
##    #
##
##    #Show in 2 location in the parking lot
##    #Start position
##
##    red_car = cv2.imread("red_car.png")
##    h,w = red_car.shape[:2]
##    center = (int(w/2), int(h/2))
##    rotation_scale = 1.0
##    output_scale = (int(w*1.0), int(h*1.0))
##    angle = 0
##    rotated_car = rotate_car(red_car, center, angle*-1, rotation_scale, output_scale)
##    #cv2.imshow("rotated car", rotated_car)
##
##    background = cv2.imread("parking_lot.jpg")
##    b2 = background.copy()
##    (x1,y1) = (40,230)
##    size = rotated_car.shape
##
##    p1 = mask_and_crop(rotated_car, b2, x1, y1, size)
##    background[y1:y1+size[0], x1:x1+size[1]] = p1
##
##    cv2.waitKey(50)
##    cv2.imshow("Car rotation", background)
   


