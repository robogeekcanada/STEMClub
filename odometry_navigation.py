import numpy as np
import cv2
import matplotlib.pyplot as plt
from monovideoodometery import MonoVideoOdometery
import os

BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 0.5

img_path = "./00/image_0/"
pose_path = "./00/00.txt"

#Camera Parameters
focal = 718.8560
pp = (607.1928, 185.2157)
R_total = np.zeros((3, 3))
t_total = np.empty(shape=(3, 1))

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (21,21),
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))


vo = MonoVideoOdometery(img_path, pose_path, focal, pp, lk_params)
traj = np.zeros(shape=(600, 800, 3))


while(vo.hasNextFrame()):

    #Read frame and process frame
    frame = vo.current_frame
    vo.process_frame()

    mono_coord = vo.get_mono_coordinates()
    true_coord = vo.get_true_coordinates()

    #Calculate Mean Square Error, round up mono and true coordinates
    MSE_error = np.linalg.norm(mono_coord - true_coord)
    mono_x, mono_y, mono_z = [int(round(x)) for x in mono_coord]
    true_x, true_y, true_z = [int(round(x)) for x in true_coord]

    print("MSE Error: ", MSE_error)

    #Draw Trajectories
    cv2.circle(traj, (true_x + 400, true_z + 100), 1, RED, 4)
    cv2.circle(traj, (mono_x + 400, mono_z + 100), 1, GREEN, 4)

    #Labels Trajectories
    cv2.putText(traj, 'Actual Position:', (140,90), font, font_size, WHITE, 1)
    cv2.putText(traj, 'RED', (270,90), font, font_size, RED, 1)
    cv2.putText(traj, 'Estimated Odometry position:', (30,120), font, font_size, WHITE, 1)
    cv2.putText(traj, 'GREEN', (270,120), font, font_size, GREEN, 1)

    #Display original and trajectories
    cv2.imshow('frame', frame)
    cv2.imshow('trajectory', traj)

    k = cv2.waitKey(1)
    if k == 27:
        break

cv2.destroyAllWindows()   
    
    
    
    



















