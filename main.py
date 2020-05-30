import pygame as pg
import sys as s
import poke as p
import io
from urllib.request import urlopen


pg.init()

screen = pg.display.set_mode((600, 800))
pg.display.set_caption("Pokedex")

pg.display.set_icon(pg.image.load("icon.png"))

screen_rect = screen.get_rect()

w = 160
h = 32
search_box = pg.Rect(screen_rect.centerx - w/2, screen_rect.centery-h/2, w, h)

input_poke = ""

font = pg.font.Font(None, 32)
found_pokemon = False
has_error = False
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            s.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            pg.display.set_icon(pg.image.load("blue_01.png"))
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                input_poke = input_poke[:-1]
            elif event.key == pg.K_RETURN:
                # API calls!
                url = p.get_poke_image(input_poke)
                info = p.get_poke_info(input_poke)
                if url != -1:
                    image_str = urlopen(url).read()
                    image_file = io.BytesIO(image_str)
                    py_img = pg.image.load(image_file)
                    found_pokemon = True
                    err_msg = ""
                    has_error = False
                    info_text = []
                    info_text.append(input_poke.title())
                    info_text.append("Pokedex Number: " + str(info['id']))
                    info_text.append("Height : {:.2f} feet".format(info['height']/10*3.28084))
                    info_text.append("Weight : {:.2f} pounds".format(info['weight']*100/454))
                    info_text.append("HP     : " + str(info['hp']))
                    info_text.append("Attack : " + str(info['attack']))
                    info_text.append("Defense: " + str(info['defense']))
                    if len(info['types']) > 1:
                        info_text.append("Types: ")
                    else:
                        info_text.append("Type: ")
                    for t in info['types']:
                        info_text[-1] += t.title() + ", "
                    info_text[-1] = info_text[-1][:-2]
                else:
                    err_msg = "Error. \"" + input_poke + "\" does not exist."
                    input_poke = ""
                    has_error = True
            else:
                input_poke += event.unicode

    screen.fill((151, 151, 151))

    pg.draw.rect(screen, (51, 51, 51), search_box)

    user_surf = font.render(input_poke, True, (200, 200, 200))

    if has_error:
        err_surf = font.render(err_msg, True, (200, 0, 0))
        screen.blit(err_surf, (search_box.x, search_box.y - 60))



    screen.blit(user_surf, search_box)

    if found_pokemon:
        screen.blit(py_img, (screen_rect.centerx-py_img.get_rect().width/2, 0))
        for i in range(len(info_text)):
            info_surf = font.render(info_text[i], True, (255, 255, 255))
            screen.blit(info_surf, (screen_rect.centerx-py_img.get_rect().width/2, 100+i*32))

    pg.display.flip()
