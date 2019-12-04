#!/usr/bin/env python

import cv2
import numpy as np


cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
GREEN = (0,255,0)
font_size = 2
thickness = 2

while (cam.isOpened()):

    ret, frame = cam.read()

    if ret:

        #Read frame from camera as source image
        size = frame.shape
        frame_width = size[1] -1
        frame_height = size[0] -1

        #Add a message
        cv2.putText(frame,'Genius!',(int(frame_width*0.25),int(frame_height*0.1)),
                    font, font_size, GREEN,thickness)
        

        # Create a vector of source points.
        pts_src = np.array([[0,0], [frame_width, 0], [frame_width, frame_height],
                            [0, frame_height]],dtype=float)


        # Read destination image
        img_dst = cv2.imread('Toronto billboard.jpg')
        img_dst_width = img_dst.shape[1]
        img_dst_height = img_dst.shape[0]

        pts_dst = np.float32([[413.0, 131.0], [722.0,54.0],
                    [731.0, 258.0], [400.0, 317.0]]).reshape(-1,2)

        # Calculate Homography between source and destination points
        h, status = cv2.findHomography(pts_src, pts_dst)

        # Warp source image
        img_temp = cv2.warpPerspective(frame, h, (img_dst_width,img_dst_height))

        # Black out polygonal area in destination image.
        cv2.fillConvexPoly(img_dst, pts_dst.astype(int), 0, 16)


        # Add warped source image to destination image.
        img_dst = img_dst + img_temp

        # Display image.
        cv2.imshow("Toronto Billboard", img_dst)
        if cv2.waitKey(1) == 27:
            break

cam.release()
cv2.destroyAllWindows()

