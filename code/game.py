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
        self.free_parking_money = 0
        self.doubles_counter = 0

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

    def next_step(self, player=None):
        if self.doubles_counter == 3:
            player.jail()

        if player is None:
            player = self.players.next_player()

        if player.is_jailed():
            self.jailed_player(player)
            return
        d1, d2, doubles = player.roll_dice()
        dice_sum = d1 + d2
        player.move_player_forward(dice_sum)
        print("Player rolled: {}".format(dice_sum))

        if doubles:
            print("Player rolled a double")
            self.doubles_counter += 1
            self.next_step(player)

        self.doubles_counter = 0
        #TODO: doubles_count has to be reset at the end, after recursive call

    def jailed_player(self, player):
        assert player.is_jailed()
        response = input("Do you want to pay $50 to leave jail?")
        if response == 'y':
            player.deduct_money(50)
            self.free_parking_money += 50
            player.unjail()
        else:
            d1, d2, doubles = player.roll_dice()
            if doubles:
                player.unjail()
                print("You have rolled a double, you are now free!")
                return
            else:
                player.add_jail_term()
                return

    def check_player_position(self, player):
        # TODO: A lot more checks for things such as free parking, properties, etc

        if player.pos == 30:
            player.jail()




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
#game.players.get(0).jail()

for i in range(250):
    game.next_step()