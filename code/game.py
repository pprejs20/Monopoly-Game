import pygame
from pygame.locals import *

from cards import load_all_cards
from player import Player
from tile import Tile
import random

class Game:
    def __init__(self, no_of_players):
        self.no_of_players = no_of_players
        self.tiles = Tile.load_tiles_from_xlsx()
        self.pot_cards, self.opp_cards = Game.get_cards()
        self.players = []

    def set_up_game(self, no_of_players=2):
        players = []
        for i in range(no_of_players):
            players.append(Player())
        random.shuffle(players)

    @classmethod
    def get_cards(cls):
        pot_cards, opp_cards = load_all_cards()
        random.shuffle(pot_cards)
        random.shuffle(opp_cards)
        return pot_cards, opp_cards






