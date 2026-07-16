import turtle as tr
from random import randrange as rr

n = 1000

A = ((0, 0), (1,0,0))
B = ((150, int((1.73/2)*300)),(0,0,1))
C = ((300, 0),(0,1,0))

points = [A,B,C]
x ,y = 0,0
tr.penup()

for i in points:
    tr.goto(i[0])
    tr.dot(5,i[1])
    
for i in range(n):
    point = points[rr(0,3)]
    x += ((point[0][0]) - x)/2
    y += ((point[0][1]) - y)/2
    tr.goto(x, y)
    tr.dot(3, point[1])
tr.done()

