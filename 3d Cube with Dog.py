'''
 Based on the following tutorial:
   http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_calib3d/py_pose/py_pose.html

 Modified by Robo-Geek Inc. This code is for student's reference.

'''
import numpy as np
import cv2
import glob

BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
BROWN = (0,76,153)
YELLOW = (0,255,255)


# Load the camera calibration data
with np.load('data/calib.npz') as calibData:
    mtx, dist, rvecs, tvecs = [calibData[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]

# Define the chess board rows and columns
rows = 7
cols = 6

# Set the termination criteria for the corner sub-pixel algorithm
criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)

# Prepare the object points: (0,0,0), (1,0,0), (2,0,0), ..., (6,5,0). They are the same for all images
objectPoints = np.zeros((rows * cols, 1, 3), np.float32)
objectPoints[:, :, :2] = np.mgrid[0:rows, 0:cols].T.reshape(-1, 1, 2)

#Draw 3D shapes
def draw_shape(img, cube2DPoints, color, fill = False):

    pts =[]
    for pt in cube2DPoints:
        pts.append(tuple(pt.ravel()))

    pts = np.array(pts, np.int32)
    pts = pts.reshape((-1,1,2))

    if not fill:
        #Set to True to join last point to first point
        cv2.polylines(img, [pts], True, color, 3)
    else:
        cv2.fillPoly(img,[pts],color)

    return img




# 3D Cube points
cube3DPoints = np.float32([[0, 0, 0], [0, 3, 0], [3, 3, 0], [3, 0, 0],[0,0,0],
                         [0,0,-3],[0,3,-3],[0,3,0],[3,3,0],
                         [3,3,-3],[0,3,-3],[0,0,-3],[3,0,-3],
                         [3,3,-3],[3,0,-3],[3,0,0]]).reshape(-1, 3)


dog_3DPoints = np.float32([

    [2.075,1.725,-1.5],[1.98,1.595,-1.5],[1.865,1.5,-1.5],[1.74,1.62,-1.5],
    [1.69,1.75,-1.5],[1.83,1.94,-1.5],[1.94,1.95,-1.5],[2.06,1.88,-1.5],
    [2.21,1.895,-1.5],[2.334,1.9,-1.5],[2.447,1.81,-1.5],[2.44,1.68,-1.5],
    [2.58,1.68,-1.5],[2.72,1.69,-1.5],[2.73,1.56,-1.5],[2.67,1.42,-1.5],
    [2.5,1.4,-1.5],[2.3,1.4,-1.5],[2.1,1.3,-1.5],[2.0,1.3,-1.5],[2.0,1.1,-1.5],
    [1.5,1.4,-1.5],[1.4,1.3,-1.5],[2.1,1.1,-1.5],[2.2,1.0,-1.5],[2.1,0.7,-1.5],
    [2.3,0.2,-1.5],[2.4,0.16,-1.5],[2.4,0.0,-1.5],[2.1,0,-1.5],[2.1,0.2,-1.5],
    [1.9,0.6,-1.5],[1.7,0.7,-1.5],[1.6,0.9,-1.5],[1.7,0.7,-1.5],[1.3,0.7,-1.5],
    [1.0,0.7,-1.5],[1.0,0.96,-1.5],[0.95,0.72,-1.5],[0.88,0.53,-1.5],
    [0.83,0.4,-1.5],[0.86,0.2,-1.5],[0.98,0.13,-1.5],[0.93,0,-1.5],[0.7,0,-1.5],
    [0.6,0.3,-1.5],[0.5,0.67,-1.5],[0.52,0.84,-1.5],[0.18,1.19,-1.5],
    [0.13,1.51,-1.5],[0.313,1.24,-1.5],[0.56,1.0,-1.5],[0.74,1.2,-1.5],
    [1.0,1.2,-1.5],[1.4,1.3,-1.5],[1.7,1.4,-1.5]

    ])

# Loop over the image files
for path in glob.glob('data/left[0-1][0-9].jpg'):
    # Load the image and convert it to gray scale
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (rows, cols), None)

    # Make sure the chess board pattern was found in the image
    if ret:

        # Find the rotation and translation vectors
        val, rvecs, tvecs, inliers = cv2.solvePnPRansac(objectPoints, corners, mtx, dist)

        # Project the 3D points to the image plane
        cube2DPoints, jac = cv2.projectPoints(cube3DPoints, rvecs, tvecs, mtx, dist)
        dog_2DPoints, jac = cv2.projectPoints(dog_3DPoints, rvecs, tvecs, mtx, dist)

        
        # Draw Cube and stars
        img = draw_shape(img, cube2DPoints, GREEN)
        img = draw_shape(img, dog_2DPoints, BROWN, True)

    
    # Display the image
    cv2.imshow('chess board', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
