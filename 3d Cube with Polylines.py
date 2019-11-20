
import numpy as np
import cv2
import glob

BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
PURPLE = (255,0,255)
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

#Star Points
star1_3DPoints =  np.float32([[3,3,-1],[3,0,-1],[3,2.5,-3],[3,1.5,0],[3,0.25,-3]]).reshape(-1,3)
star2_3DPoints =  np.float32([[0,3,-1],[0,0,-1],[0,2.5,-3],[0,1.5,0],[0,0.25,-3]]).reshape(-1,3)
star3_3DPoints =  np.float32([[3,1,0],[0,1,0],[2.5,3,0],[1.5,0,0],[0.25,3,0]]).reshape(-1,3)
star4_3DPoints =  np.float32([[3,1,-3],[0,1,-3],[2.5,3,-3],[1.5,0,-3],[0.25,3,-3]]).reshape(-1,3)

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
        star1_2DPoints, jac = cv2.projectPoints(star1_3DPoints, rvecs, tvecs, mtx, dist)
        star2_2DPoints, jac = cv2.projectPoints(star2_3DPoints, rvecs, tvecs, mtx, dist)
        star3_2DPoints, jac = cv2.projectPoints(star3_3DPoints, rvecs, tvecs, mtx, dist)
        star4_2DPoints, jac = cv2.projectPoints(star4_3DPoints, rvecs, tvecs, mtx, dist)
        
        # Draw Cube and stars
        img = draw_shape(img, cube2DPoints, BLUE)
        img = draw_shape(img, star1_2DPoints, YELLOW,True)
        img = draw_shape(img, star2_2DPoints, YELLOW,True)
        img = draw_shape(img, star3_2DPoints, PURPLE,True)
        img = draw_shape(img, star4_2DPoints, PURPLE, True)
    
    # Display the image
    cv2.imshow('chess board', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
