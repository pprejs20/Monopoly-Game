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

def set_up_game(no_of_players = 2):
    tiles = Tile.load_tiles_from_xlsx()
    cards = load_all_cards()
    players = []
    for i in range(no_of_players):
        players.append(Player())


def set_up_player_order(players):
    player_dice_rolls = []
    for player in players:
        player_dice_rolls.append((player.roll_dice(), player))
    for i in range(0, len(player_dice_rolls) - 1):
        if player_dice_rolls[i][0] > player_dice_rolls[i + 1][0]:
            temp = player_dice_rolls[i]
            player_dice_rolls[i] = player_dice_rolls[i + 1]
            player_dice_rolls[i + 1] = temp
    # TODO: Finish






