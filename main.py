import pygame as pg
import sys as s
import poke as p
import io
from urllib.request import urlopen


pg.init()

screen = pg.display.set_mode((600, 800))
pg.display.set_caption("Pokedex")

img = p.get_poke_image("sandshrew")

image_str = urlopen(img).read()

image_file = io.BytesIO(image_str)




py_img = pg.image.load(image_file)

pg.display.set_icon(pg.image.load("icon.png"))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            s.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            pg.display.set_icon(pg.image.load("blue_01.png"))



    screen.blit(py_img, py_img.get_rect())

    pg.display.flip()
