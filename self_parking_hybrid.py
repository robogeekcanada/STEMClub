from animation_support import *
from obstacles import *
from support.reeds_shepp_path_planning import *
from support.a_star import *
import math


def analyze_path(px,py):

    #analyze the path lists from px,py that has (x,y, direction, flag)
    #if direction is North, South, East or West then flag is True
    #otherwise moving in an angle, then flag is False  
    temp_x = px[0]
    temp_y = py[0]

    path = []
    
    for x,y in zip(px, py):
        
        x = int(x)
        y = int(y)
        temp_x = int(temp_x)
        temp_y = int(temp_y)

        if y != temp_y and x != temp_x:
            direction = math.atan((x-temp_x)/(y-temp_y))
            print(np.rad2deg(direction))
            path.append((x,y,int(np.rad2deg(direction)), False))

        if x == temp_x and y > temp_y:
            print("moving south")
            path.append((x,y,90, True))

        if x == temp_x and temp_y > y:
            print("moving north")
            path.append((x,y,-90, True))
           
        if y == temp_y and x > temp_x:
            print("moving west")
            path.append((x,y,0, True))
            
        if y == temp_y and temp_x > x:
            print("moving east")
            path.append((x,y,180, True))

        temp_x = x
        temp_y = y

    return path

def revise_path(path, goal, curvature = 0.05, step_size = 0.5):

    #where flag is False, moving in an angle
    #calculate the RS path to connect from the last point flag was True
    #to next point Flag is True
    #for the end of path, then set direction to gyaw -- goal yaw

    gx,gy,gyaw = goal[:3]

    tempx = None
    tempy = None
    tempdir = None

    first_point = False

    tempx2 = None
    tempy2 = None
    tempdir2 = None

    revised_path = []
    counter = 0
    for x,y,direction,flag in path:

        if flag:
            revised_path.append((x,y,direction))
            tempx = x
            tempy = y
            tempdir =direction
            first_point = False
        else:            
            tempx2 = x
            tempy2 = y

        if tempx2 != None and not first_point:
            #check if reaching the last point
            if counter != (len(path)-1):
                cx, cy, cyaw, mode, clen = reeds_shepp_path_planning(tempx, tempy, tempdir,
                                                             tempx2, tempy2, direction,
                                                             curvature, step_size)
            else:
                cx, cy, cyaw, mode, clen = reeds_shepp_path_planning(tempx, tempy, tempdir,
                                                             gx, gy, gyaw,
                                                             curvature, step_size)

            for x, y, yaw in zip(cx,cy,cyaw):
                revised_path.append((x,y,int(np.rad2deg(yaw))))

            tempx2 = None
            tempy2 = None
            tempdir2 = None
            first_point = True

        counter +=1 
    return revised_path

    
def main():

    parking_img = cv2.imread("images\parking_lot.jpg")

    sx = 10.0
    sy = 10.0
    
    gx = 320.0
    gy = 275.0
    gyaw = 115

    grid_size = 10.0  # [m]
    robot_size = 5.0  # [m]
    
    #Set and then draw obstacles and save picture to always display obstacles
    ox, oy = set_obstacles()
    parking_w_obstacles = draw_obstacles(parking_img, ox, oy)
    cv2.imwrite("images\parking_w_obstacles.jpg", parking_w_obstacles)

    #Using A* caculate the path 
    px, py, _ = dp_planning(sx, sy, gx, gy, ox, oy, grid_size, robot_size)
 
    #insert one more coordinate, required later as we want the car
    #not to finish in an angle as this will be a problem with RS algorithm
    px.append(gx)
    py.append(gy)

    #
    # A* has some limitations as it will not consider that a vehicle can't
    # turn immediate angles or make sharp 90 or 180 degrees turns
    #
    path = analyze_path(px,py)
    goal = [gx, gy, gyaw]
    revised_path = revise_path(path, goal, curvature = 0.1, step_size = 0.5)
    
    #Display car moving in revised path
    for p in revised_path:
        parking_img = cv2.imread("images\parking_w_obstacles.jpg")
        img = set_car_position(parking_img, int(p[0]),int(p[1]),int(p[2])) 
        cv2.imshow('Parking Lot', img)
        cv2.waitKey(15)

    #Display the trail car travelled using red circles
    for p in revised_path:
        if int(p[0]) > 0:
            cv2.circle(img,(int(p[0])+52, int(p[1])),2,RED,-1)
        else:
            cv2.circle(img,(int(p[0]), int(p[1])),2,RED,-1)
        cv2.imshow('Parking Lot', img)

if __name__ == '__main__':
    main()
 
    




