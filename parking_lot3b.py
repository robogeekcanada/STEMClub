#parking_lot3b.py

import cv2
import numpy as np

WHITE = (255, 255, 255)

def rotate_car(img, center, angle, rotation_scale, output_scale):

    rotation_matrix = cv2.getRotationMatrix2D(center, angle, rotation_scale)
    img_rotated = cv2.warpAffine(img, rotation_matrix, output_scale)
    return img_rotated


def main():

    background = cv2.imread("parking_lot.jpg")
    #cv2.imshow("Parking Lot", background)

    b2 = background.copy()
    empty_canvas = np.zeros((600,600,3), np.uint8)
    empty_canvas[:,:] = WHITE

    red_car = cv2.imread("red_car.png")
    h,w = red_car.shape[:2]
    center = (int(w/2), int(h/2))
    rotation_scale = 1.0
    output_scale = (int(w*1.0),int(h*1.0))

    for angle in range(0,361,5):

        background = cv2.imread("parking_lot.jpg")
        b2 = background.copy()

        rotated_car = rotate_car(red_car, center, angle*-1,
                                 rotation_scale, output_scale)

        cv2.waitKey(50)
        cv2.imshow("Rotated Car", rotated_car)

main()
