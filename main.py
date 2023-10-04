import pyxel
from collections import deque
from random import randint
"""jeu snake basique
- utiliser les fleches directionelles pour vous diriger
- manger des pomme rouge pour grandir 
- vous avez 1 chance sur 4 de gagner de la vitesse
- si vous manger une pomme violette vous pouvez ralentir
- cliquer sur espace lorsque vous mourrez pour rejouez"""

pyxel.init(200,200, title="snake")

COLOR = {"blue":(5,1),"green":(11,3)} # prefab de couleur pour corps et tete du snake 

def lance_game():
    """defini toute les variable pour un debut de game et ansi lance de nouveau la game"""
    global pomme, score, serpent, suprime, last_snake_part, head_pos, dx, dy, dead, time_special_pomme_spawn
    global snake_speed, time_pomme_spawn, decalage, snake_head_color, snake_body_color, pixel_taille
    global special_pomme_duration, special_pomme, special_pomme_start, suprime_special_pomme, max_speed, min_speed

    pyxel.cls(7)

    # general

    pixel_taille = 20

    dead = False

    score = 0

    # snake

    serpent = deque([(20,20),(10,20)])

    suprime = None
    last_snake_part = None

    head_pos = (20,20)

    snake_body_color = COLOR["green"][0]
    snake_head_color = COLOR["green"][1]

    # movement

    dx = 1
    dy = 0

    snake_speed = 5

    max_speed = 2
    min_speed = 5

    # pomme normal

    pomme = None

    time_pomme_spawn = 40
    decalage = 0

    # special pomme

    special_pomme = None
    suprime_special_pomme = None
    
    special_pomme_duration = 100
    time_special_pomme_spawn  = 40
    special_pomme_start = 0

lance_game()


def get_apple_pos() -> tuple:
    """recupere les cordonée dans laquelle une pomme peut spawn"""
    global pomme, special_pomme

    new_pomme = (randint(0,pyxel.width/pixel_taille-1)*pixel_taille,randint(0,pyxel.height/pixel_taille-1)*pixel_taille) # genere une cordoner aleatoire

    # regarde si cette cordonée et valide en regardant si il y a rien dessus et sinon relance la fonction jusqu'a trouver une bonne position
    if new_pomme in serpent or new_pomme == pomme or new_pomme == special_pomme: 

        return get_apple_pos()
    
    else:
        return new_pomme

def apple_spawn():
    """gere le spawn de la pomme qui permet de gagner en taille"""

    global time_pomme_spawn,decalage, pomme, serpent

    # si elle existe pas nous la creont si le temps entre le moment ou a elle a etait manger et l'actuelle et egal a notre temp de spawn
    # si oui on genere la pomme

    if pomme == None:
        
        if (pyxel.frame_count + decalage) % time_pomme_spawn == 0: 

            pomme = get_apple_pos()

def test_special_pomme():
    """gere le spawn et le despawn de la pomme qui permet reduire la vitesse"""
    global special_pomme, time_special_pomme_spawn, special_pomme_duration, special_pomme_start, suprime_special_pomme

    # toute les 40 frame nous teston avec de l'aleatoire si on spwan la pomme ou pas 

    if special_pomme == None:
        
        if pyxel.frame_count % time_special_pomme_spawn == 0:

            if randint(0,10) == 1:

                special_pomme = get_apple_pos()
                special_pomme_start = pyxel.frame_count

    # mais si deja spawn alors si ça duré de vie et atteinte on la despawn
    
    else:
        
        if (pyxel.frame_count - special_pomme_start) >= special_pomme_duration:
            suprime_special_pomme = special_pomme # met dans la variable l'endroit ou faire un carre blanc pour efacer la pomme
            special_pomme = None

def avance():
    """avance en fonction de la direction"""

    global dx, dy, serpent, suprime, head_pos, last_snake_part, pomme, score, decalage, pixel_taille, dead, snake_speed, suprime_special_pomme, special_pomme
    global max_speed, min_speed

    # si on peut avancer sur cette frame par rapport a la vitesse defini alors on avance
    if pyxel.frame_count % snake_speed == 0:

        # on creer une nouvelle tete
        last_snake_part = head_pos

        head_pos = ((head_pos[0] + (dx*pixel_taille))%pyxel.width, (head_pos[1] + (dy*pixel_taille))%pyxel.height)

        # regarde si la nouvelle tete touche le serpent si oui alors game over
        if head_pos in serpent: 
            dead = True

        # regarde si la pomme existe et si la nouvelle tete touche la pomme sinon on suprime la derniere partie du serpent
        if pomme != None and head_pos == pomme:

            # si oui on gagne en score et en vitesse de façon aleatoire  
            score += 1

            if randint(0,3) == 0:
                if (snake_speed -1) >= max_speed:
                    snake_speed -= 1

            # puis suprime la pomme       
            pomme = None

            # et set le decalage pour que la pomme mette le bon temps pour spawn
            decalage = -(pyxel.frame_count % time_pomme_spawn -1)

        else:
            suprime = serpent.pop()

        # regarde si la special pomme existe et si la nouvelle tete touche la pomme
        if special_pomme != None and head_pos == special_pomme:

            # si oui on descend la vitesse
            if (snake_speed +1) <= min_speed:
                snake_speed += 1
            
            # et on suprime la pomme
            suprime_special_pomme = special_pomme
            special_pomme = None

        # puis on rajoute la pomme dans le serpent apres avoir fait tout les tests
        serpent.appendleft(head_pos)

def input_direction():
    """teste toute les fleche directionelle et change la direction en fonction"""
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

def test_restart():
    """relance le jeux si la touche espace presser"""

    if pyxel.btnp(pyxel.KEY_SPACE):

        lance_game()

def update():

    global dead

    if not dead:

        # si nous somme pas mort 
        # nous testons les touche de clavier presse et change la directon en fonction

        input_direction()

        # avec la direction defini nous avançont

        avance()

        # gere le spawn des pommes

        apple_spawn()
        test_special_pomme()

    else:

        test_restart() #test si clique sur space si game over et relance si jamais

def draw():

    global suprime, last_snake_part, head_pos, snake_body_color, snake_head_color, score, dead, special_pomme, suprime_special_pomme, snake_speed, min_speed

    if not dead:

        # pour chaque elemnt regarde si il a une cordonée et si oui alors on le dessine

        # case blanche pour suprime les ancien texte de score et speed si le serpent n'est pas sur c'est case
        if not (0,0) in serpent: 
            pyxel.rect(0,0,20,20,7)
        if not (180,0) in serpent: 
            pyxel.rect(180,0,20,20,7)

        # dessin de case blanche pour suprime ce qu'il faut
        if suprime != None:
            pyxel.rect(suprime[0], suprime[1], pixel_taille, pixel_taille, 7)

        if suprime_special_pomme != None and not suprime_special_pomme in serpent:
            pyxel.rect(suprime_special_pomme[0], suprime_special_pomme[1], pixel_taille, pixel_taille, 7)
        
        # dessin du snake
        if last_snake_part != None:
            pyxel.rect(last_snake_part[0], last_snake_part[1], pixel_taille, pixel_taille, snake_body_color)

        if head_pos != None:
            pyxel.rect(head_pos[0], head_pos[1], pixel_taille, pixel_taille, snake_head_color)

        # dessin des pommes
        if pomme != None:
            pyxel.rect(pomme[0], pomme[1], pixel_taille, pixel_taille, 8)

        if special_pomme != None:
            pyxel.rect(special_pomme[0], special_pomme[1], pixel_taille, pixel_taille, 2)

        # texte de score et de speed

        pyxel.text(4,4,str(score),10)
        pyxel.text(pyxel.width-40,4,f"speed : {min_speed-snake_speed}",15)

    else:
        # ecran de game over

        pyxel.cls(0)
        pyxel.text(4,4,"GAME OVER", 8)
        pyxel.text(10,14,"Press --space-- to play", 14)

        # dessin de tete de mort

        pyxel.rect(40,40,20,20,7)
        pyxel.rect(43,42,6,7,0)
        pyxel.rect(53,42,6,7,0)
        pyxel.rect(45,51,10,8,0)


pyxel.run(update,draw)