import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox




class Cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dx = 1, dy = 0, color = (255, 0, 0)):
        self.pos = start
        self.dx = 1
        self.dy = 0
        self.color = color
    
    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)

    def draw(self, surface, eyes = False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

# End of Cube


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dx = 0
        self.dy = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dx = -1
                    self.dy = 0
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]
                elif keys[pygame.K_RIGHT]:
                    self.dx = 1
                    self.dy = 0
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]
                elif keys[pygame.K_UP]:
                    self.dx = 0
                    self.dy = -1
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]
                elif keys[pygame.K_DOWN]:
                    self.dx = 0
                    self.dy = 1
                    self.turns[self.head.pos[:]] = [self.dx, self.dy]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dx == -1 and c.pos[0] <= 0:
                    message_box('You died!', 'Play again')
                    self.reset((10, 10))
                elif c.dx == 1 and c.pos[0] >= c.rows - 1:
                    message_box('You died!', 'Play again')
                    self.reset((10, 10))
                elif c.dy == 1 and c.pos[1] >= c.rows - 1:
                    message_box('You died!', 'Play again')
                    self.reset((10, 10))
                elif c.dy == -1 and c.pos[1] <= 0:
                    message_box('You died!', 'Play again')
                    self.reset((10, 10))
                else:
                    c.move(c.dx, c.dy)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dx = 0
        self.dy = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dx, tail.dy

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dx = dx
        self.body[-1].dy = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)  # draw eyes
            else:
                c.draw(surface)
# End of Snake


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0

    for i in range(rows):
        x += sizeBtwn
        y += sizeBtwn

    pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
    pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global sn
    surface.fill((0, 0, 0))
    sn.draw(surface)  
    snack.draw(surface)
    drawGrid(500, 20, surface)
    pygame.display.update()

def drawSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

global sn
sn = Snake((255, 0, 0), (10, 10))
global snack
snack = Cube(drawSnack(20, sn), color = (0, 255, 0))

def main():
    global snack
    win = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    
    flag = True
    while flag:
        pygame.time.delay(80)
        clock.tick(9)
        sn.move()
        if sn.body[0].pos == snack.pos:
            sn.addCube()
            snack = Cube(drawSnack(20, sn), color = (0, 255, 0))
        
        for x in range(len(sn.body)):
            if sn.body[x].pos in list(map(lambda z:z.pos, sn.body[x + 1:])):
                print('Score: ', len(sn.body))
                message_box('You died!', 'Play again')
                sn.reset((10, 10))
                break
        
        redrawWindow(win)


main()
