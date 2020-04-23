#hog_detection.py

from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2

RED = (0,0,255)
GREEN = (0,255,0)

#Initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# loop over the image paths
imagePaths = list(paths.list_images("images"))

for imagePath in imagePaths:

    #Load the image and resize it to reduce detection time
    # and also we will improve detection accuracy
    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=min(400, image.shape[1]))
    orig = image.copy()

    #Detect people in the image
    (rects, weights) = hog.detectMultiScale(image, winStride=(4,4),
                                            padding=(8,8), scale = 1.05)

    #Show detection by drawing bounding boxes
    for (x,y,w,h) in rects:
        cv2.rectangle(orig, (x,y), (x+w, y+h), RED, 2)

    #Apply non-maxima suppression to the bounding boxes using a overlap
    #threshold to mantain overlapping boxes

    rects = np.array([[x, y, x+w, y+h] for (x,y,w,h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA,yA), (xB, yB), GREEN, 2)
    

    cv2.imshow("HOG image", orig)
    cv2.imshow("Non Max Suppression", image)
    cv2.waitKey(0)

