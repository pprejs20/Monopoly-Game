import pygame
from pygame.locals import *

from cards import load_all_cards
from player import Player, AIPlayer
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
        if player.money >= 50:
            if isinstance(player, AIPlayer):
                response = random.choice(["y", "n"])
            else:
                response = input("[{}] Do you want to pay $50 to leave jail?".format(player.name))
        else:
            response = "n"
            print("[{}] Has not enough money to leave jail (${})".format(player.name, player.money))

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

    def auction_property(self, tile, player):
        assert tile.buyable
        temp_queue = PlayerQueue(self.players.objects.copy())
        temp_queue.remove_by_name(player.name)
        curr_price = tile.cost - 50 # - 50 because the first raise will be the original price of the property (min raise 50)
        money_placed = False
        while not (temp_queue.get_length() == 0):
            curr_player = temp_queue.next_object()
            # Only one player left and has already raised, they win
            if temp_queue.get_length() == 1 and money_placed:
                break
            if isinstance(player, AIPlayer):
                curr_price, passed = self.auction_menu_ai(curr_player, tile, curr_price)
            else:
                curr_price, passed = self.display_auction_menu(curr_player, tile, curr_price)
            if passed:
                temp_queue.remove_by_name(curr_player.name)
            else:
                money_placed = True

        if temp_queue.get_length() == 0:
            print("No one bought the property")
            return
        curr_player = temp_queue.get(0)
        curr_player.buy_property(tile, cost=curr_price)
        print("({}) Bought property: {}, for ${}".format(curr_player.name, tile.space, curr_price))

    def display_auction_menu(self, player, tile, curr_price):
        # TODO: Check if player has enough money!
        string =  "-------- ({}) Tile Auction --------\n".format(player.name)
        string += "Property: {}\n".format(tile.space)
        string += "Current Price: {}\n\n".format(curr_price)
        string += "1. Pass\n"
        string += "2. Raise $50\n"
        string += "3. Raise $100\n"
        string += "4. Raise $500\n"
        string += "Choose an option: "
        inpt = input(string)

        if inpt == "1":
            return curr_price, True
        elif inpt == "2":
            return curr_price + 50, False
        elif inpt == "3":
            return curr_price + 100, False
        elif inpt == "4":
            return curr_price + 500, False

    def auction_menu_ai(self, player, tile, curr_price):
        if player.money >= curr_price + 500:
            inpt = random.choice(["1", "2", "3", "4"])
        elif player.money >= curr_price + 100:
            inpt = random.choice(["1", "2", "3"])
        elif player.money >= curr_price + 50:
            inpt = random.choice(["1", "2"])
        else:
            inpt = "1"

        if inpt == "1":
            return curr_price, True
        elif inpt == "2":
            return curr_price + 50, False
        elif inpt == "3":
            return curr_price + 100, False
        elif inpt == "4":
            return curr_price + 500, False

    def check_property(self, player):
        tile = self.tiles[player.pos]
        if tile.owner is None:
            if player.laps > 0:
                if player.money >= tile.cost:
                    if isinstance(player, AIPlayer):
                        inpt = random.choice(["y", "n"])
                    else:
                        inpt = input("[{}] buy property y/n: ".format(player.name))
                    if inpt == "y":
                        player.buy_property(tile)
                        print("[{}] Bought {} for {}".format(player.name, tile.space, tile.cost))
                    elif inpt == "n":
                        self.auction_property(tile, player)
                else:
                    print("[{}] Not enough money to buy!".format(player.name))
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
        elif tile.buyable:
            self.check_property(player)
        elif tile.space == "Pot Luck":
            pot = self.pot_cards.next_object()
        elif tile.space == "Free Parking":
            player.add_money(self.free_parking_money)
            print("[{}] Collected ${} from free parking money".format(player.name, self.free_parking_money))
            self.free_parking_money = 0
        elif tile.space == "Income Tax":
            player.deduct_money(200)
            print("[{}] Paid $200 for income tax".format(player.name))
        elif tile.space == "Super Tax":
            player.deduct_money(100)
            print("[{}] Paid $100 for super tax".format(player.name))



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

    def get_length(self):
        return len(self.objects)

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
        raise Exception("No player with that name! (getting)")

    def remove_by_name(self, name):
        for obj in self.objects:
            if obj.name == name:
                self.objects.remove(obj)
                return
        raise Exception("No player with that name! (removing)")


# players = [Player("Player1"), Player("Player2"), Player("Player3"), Player("Player4")]
players = [AIPlayer(), AIPlayer(), AIPlayer(), AIPlayer()]
game = Game(players)

for i in range(250):
    game.next_step()

# TODO: Check if player has enough money during auctioning
# TODO: Make player sell properties if they run out of money
        # Leaving jail
        # Tax tiles
        # Auctioning
        # Landing on someones tile
# TODO: Allow players to buy houses on properties if they have all the colors
# TODO: Collect money from free parking
