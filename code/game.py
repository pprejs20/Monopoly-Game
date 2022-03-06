import pygame
from pygame.locals import *

from cards import load_all_cards
from player import Player
from tile import Tile

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

def start_game(no_of_players = 2):
    tiles = Tile.load_tiles_from_xlsx()
    cards = load_all_cards()
    players = []
    for i in range(no_of_players):
        players.append(Player())
    

