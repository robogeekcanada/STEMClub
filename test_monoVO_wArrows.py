import numpy as np
import cv2
import matplotlib.pyplot as plt
from monovideoodometery import MonoVideoOdometery
import os
import math

BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 0.5

img_path = "./00/image_0_condensed/"
pose_path = "./00/00.txt"

focal = 718.8560
pp = (607.1928, 185.2157)
R_total = np.zeros((3, 3))
t_total = np.empty(shape=(3, 1))

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (21,21),
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))


vo = MonoVideoOdometery(img_path, pose_path, focal, pp, lk_params)
##traj = np.zeros(shape=(600, 800, 3))

arrows = []


def draw_flow(img, flow, step=32):

    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    fx, fy = 3*fx, 3*fy
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)   #Round up

    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        arrows.append([x1,y1, math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))])
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis


while(vo.hasNextFrame()):


    vo.process_frame(False)
    prev = vo.old_frame
    current = vo.current_frame

    flow = cv2.calcOpticalFlowFarneback(prev, current, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    arrows.clear()
    result = draw_flow(current,flow)
    
    #Display current frame
    cv2.imshow('Mono Video Odometry with Arrows', result)

    k = cv2.waitKey(1)
    if k == 27:
        break

cv2.destroyAllWindows()
