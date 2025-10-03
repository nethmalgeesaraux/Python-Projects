import tkinter
import random

ROWS = 20
COLS = 20
TILE_SIZE = 20

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

class tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    #     self.color = "white"
    
    # def draw(self):
    #     x1 = self.x * TILE_SIZE
    #     y1 = self.y * TILE_SIZE
    #     x2 = x1 + TILE_SIZE
    #     y2 = y1 + TILE_SIZE
    #     canvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline="")

#game window

window = tkinter.Tk()
window.title("Snake Game")
window.resizable(False, False)
canvas = tkinter.Canvas(window,bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT,borderwidth=0, highlightthickness=0)

canvas.pack()
window.update()

#window center
window_width = window.winfo_width()
window_height = window.winfo_height()
Screen_width = window.winfo_screenwidth()
Screen_height = window.winfo_screenheight()

window_x = int((Screen_width/2) - (window_width/2))
window_y = int((Screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game

snake = tile(5*TILE_SIZE, 5*TILE_SIZE)
food = tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = []
velocity_x = 0
velocity_y = 0
game_over = False
score = 0

def change_direction(e):
#   print(e.keysym)  
    global velocity_x, velocity_y, game_over
    if game_over:
        return
    
    if (e.keysym == "Up" and velocity_y != 1):
         velocity_x = 0
         
         velocity_y = -1
    elif (e.keysym == "Down" and velocity_y != -1):
        velocity_x = 0
        velocity_y = 1
    elif (e.keysym == "Right"and velocity_x != -1):
        velocity_x = 1
        velocity_y = 0
    elif (e.keysym == "Left" and velocity_x != 1):
        velocity_x = -1
        velocity_y = 0
    

def move():
    global snake,food,snake_body,game_over,score
    if game_over:
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for segment in snake_body:
        if (snake.x == segment.x and snake.y == segment.y):
            game_over = True
            return

    # update body positions (from tail to head)
    if snake_body:
        for i in range(len(snake_body) - 1, 0, -1):
            snake_body[i].x = snake_body[i - 1].x
            snake_body[i].y = snake_body[i - 1].y
        snake_body[0].x = snake.x
        snake_body[0].y = snake.y

    # collision with food
    if snake.x == food.x and snake.y == food.y:
        # grow snake: add new tile at the last position
        if snake_body:
            last = snake_body[-1]
            snake_body.append(tile(last.x, last.y))
        else:
            snake_body.append(tile(snake.x, snake.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE



def draw():
    global snake, food, game_over,score
    move()
    canvas.delete("all")

    # food.draw()
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")
    
    # snake.draw()
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="green")
    window.after(100, draw)
    for segment in snake_body:
        canvas.create_rectangle(segment.x, segment.y, segment.x + TILE_SIZE, segment.y + TILE_SIZE, fill="green")

    if(game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20",text=f"GAME OVER :{score}", fill="white")
    else:
        canvas.create_text(30,20, font="Arial 14",text=f"Score: {score}", fill="white")


draw()
window.bind("<KeyPress>", change_direction)
window.mainloop()