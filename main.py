import pyxel
from collections import deque
from random import randint

pyxel.init(200,200, title="snake")

def lance_game():
    global pomme, score, serpent, suprime, last_snake_part, head_pos, dx, dy, dead
    global snake_speed, time_pomme_spawn, decalage, snake_head_color, snake_body_color, pixel_taille

    pyxel.cls(7)

    pomme = None
    score = 0

    serpent = deque([(20,20),(10,20)])

    suprime = None
    last_snake_part = None

    head_pos = (20,20)

    dx = 1
    dy = 0

    snake_speed = 5

    time_pomme_spawn = 40
    decalage = 0

    color = {"blue":(5,1),"green":(11,3)}

    snake_body_color = color["blue"][0]
    snake_head_color = color["blue"][1]

    pixel_taille = 20

    dead = False

    special_pomme = None
    special_pomme_duration = 20

lance_game()


def get_apple_pos() -> tuple:

    pomme = (randint(0,pyxel.width/pixel_taille-1)*pixel_taille,randint(0,pyxel.height/pixel_taille-1)*pixel_taille)

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

    global dx, dy, serpent, suprime, head_pos, last_snake_part, pomme, score, decalage, pixel_taille, dead, snake_speed

    if pyxel.frame_count % snake_speed == 0:

        last_snake_part = head_pos

        head_pos = ((head_pos[0] + (dx*pixel_taille))%pyxel.width, (head_pos[1] + (dy*pixel_taille))%pyxel.height)

        if head_pos in serpent or head_pos[0] < 0 or head_pos[1] < 0:
            dead = True

        if pomme != None and head_pos == pomme:
            score += 1
            if randint(1,5) == 0:
                if (snake_speed -1) >= 2:
                    snake_speed -= 1
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

def test_replay():

    if pyxel.btn(pyxel.KEY_SPACE):

        lance_game()

def special_pomme_spawn():
    global special_pomme

    if randint(0,40):

        special_pomme = get_apple_pos()

def update():

    global snake_speed, dead

    if not dead:

        input_direction()

        avance()

        apple_spawn()

    else:

        test_replay()

def draw():

    global suprime, last_snake_part, head_pos, snake_body_color, snake_head_color, score, dead

    if not dead:
        pyxel.rect(0,0,20,20,7)

        if suprime != None:
            pyxel.rect(suprime[0], suprime[1], pixel_taille, pixel_taille, 7)
        
        if last_snake_part != None:
            pyxel.rect(last_snake_part[0], last_snake_part[1], pixel_taille, pixel_taille, snake_body_color)

        if head_pos != None:
            pyxel.rect(head_pos[0], head_pos[1], pixel_taille, pixel_taille, snake_head_color)

        if pomme != None:
            pyxel.rect(pomme[0], pomme[1], pixel_taille, pixel_taille, 8)

        pyxel.text(4,4,str(score),10)
    else:
        pyxel.cls(0)
        pyxel.text(4,4,"GAME OVER", 8)
        pyxel.text(10,14,"Press --space-- to play", 14)

        pyxel.rect(40,40,20,20,7)
        pyxel.rect(44,42,3,9,0)
        pyxel.rect(55,42,3,9,0)
        pyxel.rect(45,55,10,2,0)


pyxel.run(update,draw)