import tkinter
from tkinter import *
import random

from PIL import Image, ImageTk

STATES = {1 : 'released', 2 : 'pressed', 3 : 'held', 4 : 'impulse'}
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500


class  Automat():

    def __init__(self, key):
        self.key = key
        self.state = STATES[1]

    def release(self):
        self.state = STATES[1]

    def press(self):
        self.state = STATES[2]

    def hold(self):
        self.state = STATES[3]

    def impulse(self):
        self.state = STATES[4]

    def is_released(self):
        return self.state == STATES[1]

    def is_pressed(self):
        return self.state == STATES[2]

    def is_held(self):
        return self.state == STATES[3]
    
    def is_impulse(self):
        return self.state == STATES[4]

class Player():

    def __init__(self, image, canvas):
        self.canvas = canvas
        #self.image = ImageTk.PhotoImage(Image.open(image))
        #self.id = self.canvas.create_image(250, 480, image=self.image)
        self.id = self.canvas.create_rectangle(240, 460, 260, 500, fill = 'black')
        self.x = 250
        self.y = 480
            
    def redraw(self):
        self.id = self.canvas.create_rectangle(self.x-10, 460, self.x+10, 500, fill = 'black') 

    def move_left(self, step):
        self.x -= step
        self.canvas.move(self.id, -step, 0)

    def move_right(self, step):
        self.x += step
        self.canvas.move(self.id, step, 0)


class Rectangle():

    def __init__(self, x1, y1, x2, y2, canvas):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.draw()

    def draw(self):
        self.id = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = 'black')

class RoadLine():

    def __init__(self, rect1, rect2):
        self.left_rect = rect1
        self.right_rect = rect2

    def draw(self):
        self.left_rect.draw()
        self.right_rect.draw()

    def shift_down(self):
        self.left_rect.y1 += 20
        self.left_rect.y2 += 20
        self.right_rect.y1 += 20
        self.right_rect.y2 += 20

class Game():

    def __init__(self):
        self.canvas = tkinter.Canvas(width = WINDOW_WIDTH, height = WINDOW_HEIGHT)
        self.canvas.pack()
        self.automata = []
        self.left_key = Automat('Left')
        self.right_key = Automat('Right')
        self.automata.append(self.left_key)
        self.automata.append(self.right_key)
        self.player = Player('car.png', self.canvas)
        self.canvas.bind_all('<Right>', self.right_key_press)
        self.canvas.bind_all("<KeyRelease-Right>", self.right_key_release)
        self.canvas.bind_all('<Left>', self.left_key_press)
        self.canvas.bind_all("<KeyRelease-Left>", self.left_key_release)
        self.road = []
        self.draw_grid()
        self.generate_init_scene()

        self.timer()
        self.canvas.mainloop()

    def redraw_scene(self):
        self.canvas.delete('all')
        self.player.redraw()
        self.draw_grid()
        for line in self.road:
            line.draw()
                       
    def shift_lines_down(self):
        for line in self.road:
            line.shift_down()
    
    def check_collision(self):
        for line in self.road[0:2]:
            if (line.left_rect.x2 > self.player.x - 10 or
                line.right_rect.x1 < self.player.x + 10):
                return True
        return False

    def generate_scene(self):
        self.road.pop(0)
        self.shift_lines_down()
        self.generate_new_line(24) #24th line == top line

    def generate_new_line(self, i):
        if self.right_curve:
            rect1 = Rectangle(0, (25-i-1)*20, 20*self.curve, (25-i)*20, self.canvas)
            rect2 = Rectangle(20*(self.curve+7), (25-i-1)*20, 500, (25-i)*20, self.canvas)
            road_line = RoadLine(rect1, rect2)
            self.road.append(road_line)
            self.curve += 1
        else:
            rect1 = Rectangle(0, (25-i-1)*20, 20*self.curve, (25-i)*20, self.canvas)
            rect2 = Rectangle(20*(self.curve+7), (25-i-1)*20, 500, (25-i)*20, self.canvas)
            road_line = RoadLine(rect1, rect2)
            self.road.append(road_line)
            self.curve -= 1
        if abs(self.curve - self.starting_curve) == self.curve_length:
            self.starting_curve = self.curve
            self.right_curve = not self.right_curve
            self.curve_length = random.randint(4,9)

    def generate_init_scene(self):
        self.starting_curve = self.curve = random.randint(6,9)
        self.curve_length = random.randint(6,9)
        self.right_curve = True
        for i in range(25):
            self.generate_new_line(i)

    def right_key_press(self, event):
        if self.right_key.is_released() or self.right_key.is_impulse():
            self.right_key.press()

    def left_key_press(self, event):
        if self.left_key.is_released() or self.left_key.is_impulse():
            self.left_key.press()

    def right_key_release(self, event):
        if self.right_key.is_pressed():
            self.right_key.impulse()
        elif self.right_key.is_held():
            self.right_key.release()

    def left_key_release(self, event):
        if self.left_key.is_pressed():
            self.left_key.impulse()
        elif self.left_key.is_held():
            self.left_key.release()
        
    def draw_grid(self):
        for i in range(25):
            self.canvas.create_line(i*20, 0, i*20, 500)
            self.canvas.create_line(0, i*20, 500, i*20)


    def timer(self):
        ## pressed
        if self.left_key.is_pressed():
            self.player.move_left(10)
            self.left_key.hold()

        if self.right_key.is_pressed():
            self.player.move_right(10)
            self.right_key.hold()

        ## held
        if self.left_key.is_held():
            self.player.move_left(10)

        if self.right_key.is_held():
            self.player.move_right(10)

        ## impulse
        if self.left_key.is_impulse():
            self.player.move_left(10)
            self.left_key.release()

        if self.right_key.is_impulse():
            self.player.move_right(10)
            self.right_key.release()

        self.generate_scene()
        self.redraw_scene()
        print(self.check_collision())
            
        self.canvas.after(500, self.timer)

a = Game()
