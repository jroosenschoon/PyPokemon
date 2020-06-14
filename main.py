import pygame as pg
import sys as s
import poke as p
import io
from urllib.request import urlopen

type_colors = {
    "normal"   : "#B5B5A7",
    "poison"   : "#A65B9E",
    "psychic"  : "#F863B3",
    "grass"    : "#8CD751",
    "ground"   : "#EDCA57",
    "ice"      : "#96F1FF",
    "fire"     : "#FA5643",
    "rock"     : "#CBBB70",
    "dragon"   : "#8975FF",
    "water"    : "#56ADFF",
    "bug"      : "#C3D21F",
    "dark"     : "#8C6955",
    "fighting" : "#A85545",
    "ghost"    : "#736FCD",
    "steel"    : "#C4C2DB",
    "flying"   : "#79A4FF",
    "electric" : "#FDE339",
    "fairy"    : "#F8ACFF"
}


pg.init()

screen = pg.display.set_mode((600, 800))
pg.display.set_caption("Pokedex")

pg.display.set_icon(pg.image.load("icon.png"))

screen_rect = screen.get_rect()

w = 160
h = 32
search_box = pg.Rect(screen_rect.centerx - w/2, screen_rect.centery-h/2, w, h)
again_box  = pg.Rect(screen_rect.right-w-10, screen_rect.top+10, w, h)
again_txt  = "Search again"

input_poke = ""

font       = pg.font.Font("Satisfy-Regular.ttf", 32)
small_font = pg.font.Font("Satisfy-Regular.ttf", 26)

found_pokemon = False
has_error = False

left_padding = 10

bg = pg.image.load("oldpaper.jpg")

ability_rect = pg.Rect(left_padding, 200, screen_rect.width/2 - left_padding*2, 150)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            s.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            # Search again
            if again_box.collidepoint(pg.mouse.get_pos()):
                found_pokemon = False
                input_poke = ""

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
                    py_img = pg.transform.scale(py_img, (250, 250))
                    found_pokemon = True
                    err_msg = ""
                    has_error = False
                    info_text = []
                    # info_text.append(input_poke.title())
                    # info_text.append("Pokedex Number: " + str(info['id']))
                    # info_text.append("Height : {:.2f} feet".format(info['height']/10*3.28084))
                    # info_text.append("Weight : {:.2f} pounds".format(info['weight']*100/454))
                    # info_text.append("HP     : " + str(info['hp']))
                    # info_text.append("Attack : " + str(info['attack']))
                    # info_text.append("Defense: " + str(info['defense']))
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

    # screen.fill((151, 151, 151))
    screen.blit(bg, (0, 0))

    if has_error:
        err_surf = font.render(err_msg, True, (200, 0, 0))
        screen.blit(err_surf, (search_box.x, search_box.y - 60))

    if not found_pokemon:
        pg.draw.rect(screen, (51, 51, 51), search_box)
        user_surf = font.render(input_poke, True, (200, 200, 200))
        screen.blit(user_surf, search_box)

    if found_pokemon:
        pg.display.set_icon(pg.transform.scale(py_img, (32, 32)))
        pg.draw.rect(screen, (194, 255, 251), again_box)
        again_surf = small_font.render(again_txt, True, (77, 77, 77))
        screen.blit(again_surf, again_box)
        py_img_rect = py_img.get_rect()
        py_img_rect.x = screen_rect.left + left_padding
        py_img_rect.y = screen_rect.bottom - py_img.get_rect().height+10
        screen.blit(py_img, py_img_rect)

        # Name
        name_surf = font.render("Name: " + input_poke.title() + " (" + str(info['id']) + ")", True, (255, 255, 255))
        screen.blit(name_surf, (left_padding, left_padding))

        # Type(s)
        if len(info['types']) > 1:
            type_txt = "Types: "
        else:
            type_txt = "Type: "
        t_surf = font.render(type_txt + " ", True, pg.Color('#FFFFFF'))
        screen.blit(t_surf, (left_padding, left_padding * 2 + 32))
        t_rect = None
        for t in info['types']:
            type_surf = font.render(t + " ", True, pg.Color(type_colors[t]))
            if t_rect is not None:
                x = t_rect.right + 10
                y = left_padding * 2 + 32
                t_rect = type_surf.get_rect()
                t_rect.x = x
                t_rect.y = y
                screen.blit(type_surf, t_rect)
            else:
                t_rect = type_surf.get_rect()
                t_rect.x = left_padding+t_surf.get_rect().width
                t_rect.y = left_padding * 2 + 32
                screen.blit(type_surf, t_rect)

        type_txt = type_txt[:-2]

        # Weight/Height
        # print(info['weight'], info['height'])
        weight_surf = font.render("Weight : {:.2f} pounds".format(info['weight']*100/454), True, (255, 255, 255))
        screen.blit(weight_surf, (left_padding+py_img_rect.width-4, py_img_rect.top+60))
        height_surf = font.render("Height : {:.2f} feet".format(info['height']/10*3.28084), True, (255, 255, 255))
        screen.blit(height_surf, (left_padding+py_img_rect.width-4, py_img_rect.top+95))

        # Abilities
        # 154
        # print(info['abilities'])
        pg.draw.rect(screen, (207, 252, 255), ability_rect)
        y = 200
        for ability in info['abilities']:

            size = font.size(ability)  # (width, height)
            init_x = left_padding + 10

            mouse_pos = pg.mouse.get_pos()

            if mouse_pos[0] > init_x and mouse_pos[0] < init_x + size[0] and mouse_pos[1] > y and mouse_pos[1] < y+size[1]:
                a_surf = font.render(ability, True, (255, 103, 34))
                # Convert sentence to list of words
                # Make top_surf the first half of the words
                # Make bottom_suf the last half of the words
                words_list = ability.split()
                top_txt = ""
                for i in range(round(len(words_list)/2)):
                    top_txt += words_list[i] + " "

                a_info_surf = small_font.render(top_txt, True, (0, 0, 0))
                screen.blit(a_info_surf, (init_x, y+75))
            else:
                a_surf = font.render(ability, True, (0, 0, 0))

            screen.blit(a_surf, (init_x, y))


            y += 50


    pg.display.flip()
