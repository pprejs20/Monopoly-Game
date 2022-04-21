
from cards import load_all_cards
from player import Player, AIPlayer, tiles_of_color
from tile import Tile
from inter import Intermediary
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
        self.gui = Intermediary(self)

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
        self.gui.gui_roll_dice(player, d1, d2)
        self.check_player_position(player)
        print("[{}] rolled: {}".format(player.name, dice_sum))

        if doubles:
            print("[{}] Player rolled a double".format(player.name))
            self.doubles_counter += 1
            self.next_step(player)

        self.doubles_counter = 0
        if player.has_monopoly() and not doubles:
            self.check_monopoly(player)

    def check_monopoly(self, player):
        # TODO: Finish this
        inpt = None
        while input != 1:
            available_props = self.get_house_available_props(player)
            string = "1. Leave\n"
            string += self.consturct_prop_strings(available_props)
            string += "\nSelect an option: "
            inpt = int(input(string))

            if inpt == 1:
                return
            elif inpt > 1:
                self.buy_house(available_props[inpt - 2], player)

    def buy_house(self, prop, player):
        player.deduct_money(house_costs[prop.group])
        prop.add_house()


    def consturct_prop_strings(self, props):
        string = ""
        counter = 2
        for prop in props:
            string += "{}. {}, {}, £{} per house\n".format(counter, prop.space, prop.group, house_costs[prop.group])
            counter += 1
        return string

    def get_house_available_props(self, player):
        monopolies = player.get_monopolies()
        available_props = []
        for mon in monopolies:
            props = player.get_props_of_color(mon)
            house_nos = self.get_prop_houses(props)
            min_houses = min(house_nos)
            max_houses = max(house_nos)
            assert not max_houses - min_houses > 1
            for prop in props:
                if prop.no_of_houses == min_houses:
                    available_props.append(prop)
        return available_props

    def get_prop_houses(self, props):
        house_nos = []
        for prop in props:
            house_nos.append(prop.no_of_houses)
        return house_nos

    def jailed_player(self, player):
        assert player.is_jailed()
        if player.money >= 50:
            # if isinstance(player, AIPlayer):
            #     response = random.choice(["y", "n"])
            # else:
            response = self.gui.gui_jailed_player(player)
        else:
            response = "n"
            print("[{}] Doesn't have enough money to leave jail (£{})".format(player.name, player.money))

        if response == 'y':
            player.deduct_money(50)
            self.free_parking_money += 50
            player.unjail()
            self.gui.gui_reblit_all()
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
        self.gui.gui_auction_prop(tile)
        while not (temp_queue.get_length() == 0):
            curr_player = temp_queue.next_object()
            # Only one player left and has already raised, they win
            if temp_queue.get_length() == 1 and money_placed:
                break
            # if isinstance(player, AIPlayer):
            #     curr_price, passed = self.auction_menu_ai(curr_player, tile, curr_price)
            # else:
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
        self.gui.gui_buy_prop(curr_player, tile)
        self.gui.gui_reblit_board()
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

        inpt = self.gui.gui_auction_menu(player, curr_price)

        if inpt == "1":
            return curr_price, True
        elif inpt == "2":
            return curr_price + 50, False
        elif inpt == "3":
            return curr_price + 100, False
        elif inpt == "4":
            return curr_price + 500, False

    # def auction_menu_ai(self, player, tile, curr_price):
        # inpt = self.gui.gui_auction_menu(player, curr_price)
        # if player.money >= curr_price + 500:
        #     inpt = random.choice(["1", "2", "3", "4"])
        # elif player.money >= curr_price + 100:
        #     inpt = random.choice(["1", "2", "3"])
        # elif player.money >= curr_price + 50:
        #     inpt = random.choice(["1", "2"])
        # else:
        #     inpt = "1"
        #
        # if inpt == "1":
        #     return curr_price, True
        # elif inpt == "2":
        #     return curr_price + 50, False
        # elif inpt == "3":
        #     return curr_price + 100, False
        # elif inpt == "4":
        #     return curr_price + 500, False

    def check_property(self, player):
        tile = self.tiles[player.pos-1]
        if tile.owner is None:
            if player.laps > 0:
                if player.money >= tile.cost:
                    inpt = self.gui.gui_offer_prop(player)
                    # if isinstance(player, AIPlayer):
                    #     inpt = random.choice(["y", "n"])
                    # else:
                    #     inpt = response
                    if inpt == "y":
                        player.buy_property(tile)
                        self.gui.gui_buy_prop(player)
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
        tile = self.tiles[player.pos-1]
        self.gui.gui_check_player_location(player)
        if tile.group == "Go to jail":
            player.jail()
            self.gui.gui_go_jail(player)
        elif tile.pos == 1:
            self.gui.gui_go(player)
        elif tile.buyable:
            self.check_property(player)
        elif tile.space == "Pot Luck":
            pot = self.pot_cards.next_object()
            self.gui.gui_pot_luck(pot)
            # pot.execute(player, self.players, self)
        elif tile.space == "Opportunity Knocks":
            opp = self.opp_cards.next_object()
            self.gui.gui_opp_knocks(opp)
            # opp.execute(player, self.players, self)
        elif tile.space == "Free Parking":
            player.add_money(self.free_parking_money)
            self.gui.gui_free_parking(player)
            print("[{}] Collected ${} from free parking money".format(player.name, self.free_parking_money))
            self.free_parking_money = 0
        elif tile.space == "Income Tax":
            player.deduct_money(200)
            self.gui.gui_income_tax(player)
            print("[{}] Paid $200 for income tax".format(player.name))
        elif tile.space == "Super Tax":
            self.gui.gui_super_tax(player)
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

house_costs = {
    "Brown": 50,
    "Blue": 50,
    "Purple": 100,
    "Orange": 100,
    "Red": 150,
    "Yellow": 150,
    "Green": 200,
    "Deep Blue": 200
}


# players = [Player("Player1"), Player("Player2"), Player("Player3"), Player("Player4")]
# # players = [AIPlayer(), AIPlayer(), AIPlayer(), AIPlayer()]
# game = Game(players)
#
# game.players.objects[0].buy_property(game.tiles[1])
# game.players.objects[0].buy_property(game.tiles[3])
# game.next_step()
# for i in range(250):
#     game.next_step()

# TODO: Check if player has enough money during auctioning
# TODO: Make player sell properties if they run out of money
        # Leaving jail
        # Tax tiles
        # Auctioning
        # Landing on someones tile
# TODO: Allow players to buy houses on properties if they have all the colors
# TODO: Collect money from free parking

# TODO: Finish Check monopoly
