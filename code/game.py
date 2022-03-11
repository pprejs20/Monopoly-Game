import pygame
from pygame.locals import *

from cards import load_all_cards
from player import Player
from tile import Tile
import random

class Game:
    def __init__(self, no_of_players=3):
        self.no_of_players = no_of_players
        self.tiles = Tile.load_tiles_from_xlsx()
        self.pot_cards, self.opp_cards = Game.get_cards()
        self.players = Game.set_up_players(no_of_players)

    @classmethod
    def set_up_players(cls, no_of_players):
        players = []
        for i in range(no_of_players):
            players.append(Player())
        players = PlayerQueue(players)
        players.shuffle()
        return players

    @classmethod
    def get_cards(cls):
        pot_cards, opp_cards = load_all_cards()
        random.shuffle(pot_cards)
        random.shuffle(opp_cards)
        return pot_cards, opp_cards


class PlayerQueue:
    def __init__(self, players):
        self.players = players

    def shuffle(self):
        random.shuffle(self.players)

    def next_player(self):
        player = self.players.pop(0)
        self.players.append(player)
        return player

    def get(self, i):
        return self.players[i]

    def __str__(self):
        string = "----------- Player Queue -----------\n"
        i = 1
        for player in self.players:
            string += "-- " + str(i) + " --\n"
            string += "" + str(player)
            i += 1
        string += "-----------------------------------\n"
        return string

game = Game()
