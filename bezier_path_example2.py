#bezier_path_example.py

import matplotlib.pyplot as plt
import numpy as np
import scipy.special
from bezier_module2 import *


def main():

    #Plot an example of a bezier curve
    start_x = 10.0
    start_y = 1.0
    start_yaw = np.radians(180)

    end_x = -0.0
    end_y = -3.0
    end_yaw = np.radians(-45)
    offset = 3.0

    path, control_points = calc_4points_bezier_path(
        start_x, start_y, start_yaw, end_x, end_y, end_yaw, offset)

    #Alternatively we could specify the path control_points**

    #Display the tangent, normal and radius of curvature at any given point
    t = 0.86
    x_target, y_target = bezier(t, control_points)
    derivatives_cp = bezier_derivatives_control_points(control_points, 2)

    point = bezier(t, control_points)
    dt = bezier(t, derivatives_cp[1])
    ddt = bezier(t, derivatives_cp[2])

    #Radius of curvature
    radius = 1/ curvature(dt[0], dt[1], ddt[0], ddt[1])
    #Normalize derivative
    dt /= np.linalg.norm(dt,2)

    tangent = np.array([point, point +dt])
    normal = np.array([point, point + [-dt[1], dt[0]]])
    curvature_center = point + np.array([- dt[1], dt[0]]) * radius

    circle = plt.Circle(tuple(curvature_center),radius,
                        color=(0, 0.8, 0.8), fill = False, linewidth =1)

    assert path.T[0][0] == start_x, "path is invalid"
    assert path.T[1][0] == start_y, "path is invalid"
    assert path.T[0][-1] == end_x, "path is invalid"
    assert path.T[1][-1] == end_y, "path is invalid"

    if show_animation:

        fig, ax = plt.subplots()
        ax.plot(path.T[0], path.T[1], label="Bezier Path")
        ax.plot(control_points.T[0], control_points.T[1],
                '--o', label ="Control Points")

        ax.plot(x_target, y_target)
        ax.plot(tangent[:, 0], tangent[:,1], label="Tangent")
        ax.plot(normal[:,0], normal[:,1], label="Normal")
        ax.add_artist(circle)
        plot_arrow(start_x, start_y, start_yaw)
        plot_arrow(end_x, end_y, end_yaw)
        ax.legend()
        ax.axis("equal")
        ax.grid(True)
        plt.show()

main()





        

    
    

    









    

    
    


