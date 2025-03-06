import turtle
import random
import time

# Setup layar
window = turtle.Screen()
window.title("Game Turtle Menghindari Rintangan")
window.bgcolor("lightblue")
window.setup(width=600, height=600)
window.tracer(0)  # Mematikan animasi otomatis untuk kontrol manual

# Membuat turtle pemain
player = turtle.Turtle()
player.shape("turtle")
player.color("green")
player.penup()
player.goto(0, -250)

# Membuat rintangan
obstacle = turtle.Turtle()
obstacle.shape("square")
obstacle.color("red")
obstacle.shapesize(stretch_wid=1, stretch_len=3)
obstacle.penup()
obstacle.goto(random.randint(-280, 280), 300)

# Kecepatan awal
obstacle_speed = 5
player_speed = 20

# Fungsi gerakan pemain
def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += player_speed
    if x > 280:
        x = 280
    player.setx(x)

def move_up():
    y = player.ycor()
    y += player_speed
    if y > 280:
        y = 280
    player.sety(y)

def move_down():
    y = player.ycor()
    y -= player_speed
    if y < -280:
        y = -280
    player.sety(y)

# Mengontrol pemain dengan keyboard
window.listen()
window.onkey(move_left, "Left")
window.onkey(move_right, "Right")
window.onkey(move_up, "Up")
window.onkey(move_down, "Down")

# Game loop utama
game_running = True
while game_running:
    window.update()  # Update layar
    
    # Gerakan rintangan
    y = obstacle.ycor()
    y -= obstacle_speed
    obstacle.sety(y)
    
    # Reset posisi rintangan jika keluar dari layar
    if y < -300:
        x = random.randint(-280, 280)
        obstacle.goto(x, 300)
    
    # Periksa tabrakan
    if player.distance(obstacle) < 20:
        print("Game Over!")
        game_running = False

    time.sleep(0.02)  # Delay agar game tidak terlalu cepat

# Menutup window saat game selesai
window.bye()
