import pyxel
from collections import deque
from random import randint

pyxel.init(20,20, title="snake")

def lance_game():
    global pomme, score, serpent, suprime, last_snake_part, head_pos, dx, dy, snake_speed, time_pomme_spawn, decalage, snake_head_color, snake_body_color

    pyxel.cls(7)

    pomme = None
    score = 0

    serpent = deque([(2,2),(1,2)])

    suprime = None
    last_snake_part = None

    head_pos = (2,2)

    dx = 1
    dy = 0

    snake_speed = 4

    time_pomme_spawn = 40
    decalage = 0

    color = {"blue":(5,1),"green":(11,3)}

    snake_body_color = color["blue"][0]
    snake_head_color = color["blue"][1]

lance_game()


def get_apple_pos() -> tuple:

    pomme = (randint(0,pyxel.width-1),randint(0,pyxel.height-1))

    if pomme in serpent:

        return get_apple_pos()
    
    else:
        return pomme

def apple_spawn():

    global time_pomme_spawn,decalage, pomme, serpent

    if pomme == None:
        
        if (pyxel.frame_count + decalage) % time_pomme_spawn == 0:

            pomme = get_apple_pos()

def avance():

    global dx, dy, serpent, suprime, head_pos, last_snake_part, pomme, score, decalage

    if pyxel.frame_count % snake_speed == 0:

        last_snake_part = head_pos

        head_pos = ((head_pos[0] + dx)%pyxel.width, (head_pos[1] + dy)%pyxel.height)

        if head_pos in serpent or head_pos[0] < 0 or head_pos[1] < 0:
            lance_game()

        if pomme != None and head_pos == pomme:
            score += 1
            pomme = None
            decalage = -(pyxel.frame_count % time_pomme_spawn -1)
        else:
            suprime = serpent.pop()

        serpent.appendleft(head_pos)

def input_direction():
    global dx, dy

    if pyxel.btnp(pyxel.KEY_RIGHT):

        if dx != -1:
            dx = 1
            dy = 0

    if pyxel.btnp(pyxel.KEY_LEFT):

        if dx != 1:
            dx = -1
            dy = 0

    if pyxel.btnp(pyxel.KEY_UP):

        if dy != 1:
            dy = -1
            dx = 0

    if pyxel.btnp(pyxel.KEY_DOWN):

        if dy != -1:
            dy = 1
            dx = 0

def update():

    global snake_speed

    input_direction()

    avance()

    apple_spawn()

def draw():

    global suprime, last_snake_part, head_pos, snake_body_color, snake_head_color

    if suprime != None:
        pyxel.rect(suprime[0], suprime[1], 1, 1, 7)
    
    if last_snake_part != None:
        pyxel.rect(last_snake_part[0], last_snake_part[1], 1, 1, snake_body_color)

    if head_pos != None:
        pyxel.rect(head_pos[0], head_pos[1], 1, 1, snake_head_color)

    if pomme != None:
        pyxel.rect(pomme[0], pomme[1], 1, 1, 8)


pyxel.run(update,draw)