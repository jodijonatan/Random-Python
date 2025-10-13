import turtle

screen = turtle.Screen()
screen.bgcolor("black")

pen = turtle.Turtle()
pen.speed(0)
pen.width(2)

colors = ["red", "yellow", "blue", "green", "purple", "orange"]

for i in range(360):
    pen.pencolor(colors[i % 6])
    pen.forward(i * 3 / 2 + i)
    pen.left(59)

pen.hideturtle()

turtle.done()
