#Original code from Joseph Bakulikira
#https://github.com/Josephbakulikira/Astar-PathFinding-Python
#main_turtle.py

import algorithm as AL
import turtle
import time

t = turtle.Turtle()
t.speed(0)

top_left = (-300,300)
grid_size = 50

def draw_grid():

    t.pensize(2)
    t.pu()
    t.goto(top_left)
    t.pd()

    #Draw rows
    for i in range(11):
        t.pu()
        t.goto(top_left[0], top_left[1] - grid_size*i)
        t.pd()
        t.goto(top_left[0] + grid_size*10, top_left[1] - grid_size*i)

    #Draw columns
    for i in range(11):
        t.pu()
        t.goto(top_left[0] + grid_size*i, top_left[1])
        t.pd()
        t.goto(top_left[0] + grid_size*i, top_left[1] - grid_size*10)

def draw_square(x,y,color):

    t.pu()
    t.fillcolor(color)
    t.begin_fill()
    t.goto(x,y)
    t.pd()
    t.goto(x+ grid_size, y)
    t.goto(x+ grid_size, y - grid_size)
    t.goto(x, y - grid_size)
    t.goto(x,y)
    t.end_fill()
    t.pu()


def color_square(Node, color):

    draw_square(top_left[0] + grid_size*Node[1],
                top_left[1] - grid_size*Node[0], color)

def color_row(row_data, row = 1):

    for i in range(len(row_data)):

        if row_data[i] == 1:
            draw_square(top_left[0] + grid_size*i,
                        top_left[1] - grid_size*row, 'green')


def main():

    draw_grid()
    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    for i in range(len(grid)):
        color_row(grid[i], i)

    StartNode = (0,0)
    EndNode = (9,9)

    color_square(StartNode,'yellow')
    color_square(EndNode, 'red')

    layout = AL.algorithm(grid, StartNode, EndNode)
    print(layout)

    time.sleep(2)

    for node in layout:
        color_square(node, 'blue')
    

main()
