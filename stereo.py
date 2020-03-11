#stereo.py
#Read 2 pictures and generate a Meshlab file .ply

#Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


def main():

    print("Loading images...")

    #pyrDown means to downscale fast
    imgL = cv2.pyrDown(cv2.imread('aloeL.jpg'))
    imgR = cv2.pyrDown(cv2.imread('aloeR.jpg'))


    #Initialize settings for 'aloe' image pair
    window_size = 3
    min_disp = 16
    num_disp = 112 - min_disp

    
    stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
        numDisparities = num_disp,
        blockSize = 16,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        disp12MaxDiff = 1,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 32)

    print("Computing disparity....")
    disp = stereo.compute(imgL, imgR).astype(np.float32)/16.0

    print("Generating 3D point cloud ... ")
    h, w = imgL.shape[:2]
    f = 0.8*w    #this is an initial guess
    Q = np.float32([[1, 0, 0, -0.5*w],
                    [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
                    [0, 0, 0,     -f], # so that y-axis looks up
                    [0, 0, 1,      0]])


    points = cv2.reprojectImageTo3D(disp, Q)
    colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]
    out_fn = 'Aloe 3D cloud.ply'
    write_ply(out_fn, out_points, out_colors)
    print('%s saved' % out_fn)

    cv2.imshow("Left image", imgL)
    cv2.imshow("Disparity", (disp-min_disp)/num_disp)
    cv2.waitKey()

    print("Transaction Completed...")
    


main()
