import tkinter as tk
from tkinter import *
import random

# Game configuration
width = 400
height = 400
speed = 200
body_size = 2
space_size = 20
snake_color = "#ffc0cb"
background = "#ADD8E6"
food_color = "#000000"
direction = "right"

class Snake:
    def __init__(self):
        self.body_size = body_size
        self.coordinates = []
        self.squares = []

        for _ in range(body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, width / space_size - 1) * space_size
        y = random.randint(0, height / space_size - 1) * space_size

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + space_size, y + space_size, fill=food_color, tag="food")

class Game:
    def __init__(self):
        self.direction = direction
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.score_label = tk.Label(root, text="Score: {}".format(self.score), font=('consolas', 20))
        self.score_label.pack()
        root.after(speed, self.next_move)

    def next_move(self):
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= space_size
        elif self.direction == "down":
            y += space_size
        elif self.direction == "left":
            x -= space_size
        elif self.direction == "right":
            x += space_size

        self.snake.coordinates.insert(0, (x, y))
        square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color)

        self.snake.squares.insert(0, square)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.score_label.config(text="Score: {}".format(self.score))
            canvas.delete("food")
            self.food = Food()
        else:
            del self.snake.coordinates[-1]
            canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        if self.manage_collision():
            self.game_over()
        else:
            root.after(speed, self.next_move)

    def manage_direction(self, chosen_direction):
        if chosen_direction == "right" and self.direction != "left":
            self.direction = chosen_direction
        elif chosen_direction == "left" and self.direction != "right":
            self.direction = chosen_direction
        elif chosen_direction == "up" and self.direction != "down":
            self.direction = chosen_direction
        elif chosen_direction == "down" and self.direction != "up":
            self.direction = chosen_direction

    def manage_collision(self):
        x, y = self.snake.coordinates[0]
        if x < 0 or x >= width or y < 0 or y >= height:
            return True

        for body_collision in self.snake.coordinates[1:]:
            if x == body_collision[0] and y == body_collision[1]:
                return True

        return False

    def game_over(self):
        canvas.delete(ALL)
        canvas.create_text(width / 2, height / 2, font=('consolas', 60), text="GAME OVER", fill="black", tag="gameover")

# Create the Tkinter root window
root = tk.Tk()
root.title("Snake")

# Create the canvas
canvas = tk.Canvas(root, bg=background, width=width, height=height)
canvas.pack()
root.update()



# Create the game instance
game = Game()


# Bind arrow keys to change the direction of the snake
root.bind('<Left>', lambda event: game.manage_direction('left'))
root.bind('<Right>', lambda event: game.manage_direction('right'))
root.bind('<Up>', lambda event: game.manage_direction('up'))
root.bind('<Down>', lambda event: game.manage_direction('down'))

# Start the Tkinter event loop
root.mainloop()