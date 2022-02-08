import pygame
from pygame.locals import *

pygame.init()

screen_width = 1000
screen_hight = 1000

screen = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption("Monopoly")

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
