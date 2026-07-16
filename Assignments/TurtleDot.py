import turtle as tr

points = [(50,30),(-20,10),(0,0),(30,-40),(-10,-20)]

for x, y in points:
    tr.penup()
    tr.goto(x ,y)
    tr.dot(5, "red")
tr.done()