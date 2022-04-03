import pygame
from pygame.locals import *

from cards import load_all_cards
from player import Player
from tile import Tile
import random


class Game:
    def __init__(self, players):
        self.players = PlayerQueue(players)
        self.players.shuffle()
        self.tiles = Tile.load_tiles_from_xlsx()
        self.pot_cards, self.opp_cards = Game.get_cards()
        self.pot_cards = Queue(self.pot_cards)
        self.opp_cards = Queue(self.opp_cards)
        self.free_parking_money = 0
        self.doubles_counter = 0
        self.current_d1 = None
        self.current_d2 = None

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
            player = self.players.next_object()

        if player.is_jailed():
            self.jailed_player(player)
            return
        d1, d2, doubles = player.roll_dice()
        self.current_d1 = d1
        self.current_d2 = d2
        dice_sum = d1 + d2
        player.move_player_forward(dice_sum)
        self.check_player_position(player)
        print("[{}] rolled: {}".format(player.name, dice_sum))

        if doubles:
            print("[{}] Player rolled a double".format(player.name))
            self.doubles_counter += 1
            self.next_step(player)

        self.doubles_counter = 0
        # TODO: doubles_count has to be reset at the end, after recursive call

    def jailed_player(self, player):
        assert player.is_jailed()
        response = input("[{}] Do you want to pay $50 to leave jail?".format(player.name))
        if response == 'y':
            player.deduct_money(50)
            self.free_parking_money += 50
            player.unjail()
        else:
            d1, d2, doubles = player.roll_dice()
            if doubles:
                player.unjail()
                print("[{}] You have rolled a double, you are now free!".format(player.name))
                return
            else:
                player.add_jail_term()
                return

    def find_jail_position(self):
        for t in self.tiles:
            if t.group == "Go to jail":
                return t.pos-1

    def check_property(self, player):
        tile = self.tiles[player.pos]
        if tile.owner is None:
            if player.laps > 0:
                if input("[{}] buy property y/n: ".format(player.name)) == "y":
                    player.deduct_money(tile.cost)
                    tile.owner = player.name
                    player.add_prop(tile)
        elif tile.owner is not None:
            if tile.group == "Utilities":
                self.check_utilities(player, tile.owner)

    def check_utilities(self, player, owner_name):
        owner = self.players.get_by_name(owner_name)
        count = self.count_utilities(owner)
        if count == 1:
            money_owed = (self.current_d1 + self.current_d2) * 4
        elif count == 2:
            money_owed = (self.current_d1 + self.current_d2) * 4
        else:
            raise Exception("Invalid number of utilities")

        player.deduct_money(money_owed)
        owner.add_money(money_owed)

    def count_utilities(self, player):
        count = 0
        for prop in player.propList:
            if prop.group == "Utilities":
                count += 1
        return count

    def check_player_position(self, player):
        # TODO: A lot more checks for things such as free parking, properties, etc
        tile = self.tiles[player.pos]
        if tile.group == "Go to jail":
            player.jail()
        if tile.buyable:
            self.check_property(player)
        if tile.space == "Pot Luck":
            pot = self.pot_cards.next_object()


class Queue:
    def __init__(self, objects):
        self.objects = objects

    def shuffle(self):
        random.shuffle(self.objects)

    def next_object(self):
        object = self.objects.pop(0)
        self.objects.append(object)
        return object

    def get(self, i):
        return self.objects[i]

    def remove(self):
        return self.objects.pop(-1)

    def __str__(self):
        string = "--------------- Queue --------------\n"
        i = 1
        for obj in self.objects:
            string += "-- " + str(i) + " --\n"
            string += "" + str(obj)
            i += 1
        string += "-----------------------------------\n"
        return string


class PlayerQueue(Queue):
    def __init__(self, players):
        super().__init__(players)

    def get_by_name(self, name):
        for obj in self.objects:
            if obj.name == name:
                return obj

        raise Exception("No player with that name!")


players = [Player("Player1"), Player("Player2"), Player("Player3"), Player("Player4")]
game = Game(players)

for i in range(250):
    game.next_step()
