
from cards import load_all_cards
from player import Player, AIPlayer, tiles_of_color
from tile import Tile
from inter import Intermediary
import random


class Game:
    """
    Main game engine class
    """

    def __init__(self, players):

        assert len(players) <= 6 and len(players) >= 2

        self.players = PlayerQueue(players)
        self.players.shuffle()
        self.tiles = Tile.load_tiles_from_xlsx()
        self.pot_cards, self.opp_cards = Game.get_cards()
        self.free_parking_money = 0
        self.doubles_counter = 0
        self.current_d1 = None
        self.current_d2 = None
        self.gui = Intermediary(self)

    @classmethod
    def get_cards(cls):
        """
        Gets the cards from the excel data, shuffles, and returns them in the correct format
        :return: A tuple of two card queues, for pot luck and opportunity knocks cards respectively
        """

        pot_cards, opp_cards = load_all_cards()
        pot_cards = Queue(pot_cards)
        opp_cards = Queue(opp_cards)
        pot_cards.shuffle()
        opp_cards.shuffle()
        return pot_cards, opp_cards

    def next_step(self, player=None):
        """
        The main game loop function, it drives the game forward
        :param player: optional parameter if a deviation from standard player queue order is required
        """

        if self.doubles_counter == 3:
            player.jail()
            self.gui.doubles_jail(player)
        else:

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
            self.gui.roll_dice(player, d1, d2)
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
        """
        This function is used to allow players to buy houses and hotels if they have a monopoly
        :param player: the player that this procedure will be executed for
        """

        inpt = None
        first_time = True
        while input != 1:
            available_props = self.get_house_available_props(player, first_time)
            # first_time = False
            # string = "1. Leave\n"
            # string += self.consturct_prop_strings(available_props)
            # string += "\nSelect an option: "
            inpt = int(self.gui.buy_buildings(self, player, first_time))

            if inpt == 1:
                return
            elif inpt > 1:
                self.buy_house(available_props[inpt - 2], player)

    def buy_house(self, prop, player):
        """
        This function buys a house at a property
        :param prop: the property for which the house will be purchased
        :param player: the player which will purchase the property
        """
        
        player.deduct_money(house_costs[prop.group])
        prop.add_house()


    def consturct_prop_strings(self, props):
        """
        Constructs the strings for the buying houses command line menu
        :param props: a list of properties for which the s
        :return: String of numbered property options
        """

        string = ""
        counter = 2
        for prop in props:
            string += "{}. {}, {}, Current Houses: {}, ${} per house\n".format(counter, prop.space, prop.group, prop.no_of_houses, house_costs[prop.group])
            counter += 1
        return string

    def get_house_available_props(self, player, first_time):
        """
        Gets the properties that a player is able to purchase houses on
        :param player: the player for which the properties will be checked
        :param first_time: this parameter prevents players from being able to buy hotels before buying 4 houses
        :return: A list of properties for which houses can be purchased
        """

        monopolies = player.get_monopolies()
        available_props = []
        for mon in monopolies:
            props = player.get_props_of_color(mon)
            house_nos = self.get_prop_houses(props)
            min_houses = min(house_nos)
            max_houses = max(house_nos)
            assert not max_houses - min_houses > 1
            for prop in props:
                if prop.no_of_houses == 5:
                    continue
                if prop.no_of_houses == min_houses:
                    if prop.no_of_houses == 4 and not first_time:
                        continue
                    available_props.append(prop)
        return available_props

    def get_prop_houses(self, props):
        """
        Makes a list of the number of houses in the corresponding properties provided by the parameter
        :param props: A list of properties
        :return: A list of integers corresponding to the number of houses in each property
        """

        house_nos = []
        for prop in props:
            house_nos.append(prop.no_of_houses)
        return house_nos

    def jailed_player(self, player):
        """
        Procedure that takes place when a player is in jail on their turn
        :param player: the jailed player
        """

        assert player.is_jailed()

        if player.jailCard > 0:
            input = self.gui.gjf_card(player)
            if input == "y":
                player.jailCard -= 1
                player.unjail()
                self.gui.reblit_all()
                return
            else:
                pass

        if player.money >= 50:
            # if isinstance(player, AIPlayer):
            #     response = random.choice(["y", "n"])
            # else:
            response = self.gui.jailed_player(player)
        else:
            response = "n"
            print("[{}] Doesn't have enough money to leave jail (£{})".format(player.name, player.money))

        if response == 'y':
            self.gui.pay_to_leave(player)
            player.deduct_money(50, True)
            self.free_parking_money += 50
            player.unjail()
            self.gui.reblit_all()
        else:
            d1, d2, doubles = player.roll_dice()
            self.gui.roll_to_leave(player)
            self.gui.roll_dice(player, d1, d2)
            if doubles:
                player.unjail()
                self.gui.leave(player)
                print("[{}] You have rolled a double, you are now free!".format(player.name))
                return
            else:
                player.add_jail_term()
                return

    def find_jail_position(self):
        """
        Finds where the jail is in the list of tiles
        :return: position of the jail tile
        """

        for t in self.tiles:
            if t.group == "Go to jail":
                return t.pos-1

    def auction_property(self, tile, player):
        """
        Initiates auction procedure for when a player doesn't want to purchase a property they landed on
        :param tile: the property to be auctioned
        :param player: the player who didn't purchase the property
        """

        assert tile.buyable
        temp_queue = PlayerQueue(self.players.objects.copy())
        temp_queue.remove_by_name(player.name)
        curr_price = tile.cost - 50 # - 50 because the first raise will be the original price of the property (min raise 50)
        money_placed = False
        self.gui.auction_prop(tile)
        while not (temp_queue.get_length() == 0):
            curr_player = temp_queue.next_object()
            # check to make sure player is eligible: not in jail and at least 1 lap
            if curr_player.jailed or curr_player.laps < 1:
                temp_queue.remove_by_name(curr_player.name)
            else:
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
            self.gui.noone_bought()
            print("No one bought the property")
            return
        curr_player = temp_queue.get(0)
        curr_player.buy_property(tile, cost=curr_price)
        self.gui.buy_prop(curr_player, tile)
        print("({}) Bought property: {}, for ${}".format(curr_player.name, tile.space, curr_price))

    def display_auction_menu(self, player, tile, curr_price):
        """
        Shows the menu for auctioning properties
        :param player: the player who is currently bidding
        :param tile: the tile to be purchased
        :param curr_price: the current price for the auction
        :return: the new price and a boolean indicating whether player has passed
        """

        # TODO: Check if player has enough money!
        string =  "-------- ({}) Tile Auction --------\n".format(player.name)
        string += "Property: {}\n".format(tile.space)
        string += "Current Price: {}\n\n".format(curr_price)
        string += "1. Pass\n"
        string += "2. Raise $50\n"
        string += "3. Raise $100\n"
        string += "4. Raise $500\n"
        string += "Choose an option: "

        inpt = self.gui.auction_menu(player, curr_price)

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
        """
        Procedure which takes place when a player lands on a property
        :param player: the player whose turn it is
        """

        tile = self.tiles[player.pos-1]
        if tile.owner is None:
            if player.laps > 0:
                if player.money >= tile.cost:
                    inpt = self.gui.offer_prop(player)
                    # if isinstance(player, AIPlayer):
                    #     inpt = random.choice(["y", "n"])
                    # else:
                    #     inpt = response
                    if inpt == "y":
                        player.buy_property(tile)
                        self.gui.buy_prop(player)
                        print("[{}] Bought {} for {}".format(player.name, tile.space, tile.cost))
                    elif inpt == "n":
                        self.auction_property(tile, player)
                else:
                    print("[{}] Not enough money to buy!".format(player.name))
        elif tile.owner is not None and player.name != tile.owner:
            self.gui.owned_tile(player, tile)
            rent = tile.base_rent
            if tile.no_of_houses > 4:
                rent = tile.hotel_rent
            if tile.no_of_houses == 1:
                rent = tile.one_house_rent
            if tile.no_of_houses == 2:
                rent = tile.two_house_rent
            if tile.no_of_houses == 3:
                rent = tile.three_house_rent
            if tile.no_of_houses == 4:
                rent = tile.four_house_rent
            if tile.group in player.get_monopolies():
                if rent == tile.base_rent:
                    rent = rent*2
            # else:
            #     rent = rent
            if tile.group == "Utilities":
                rent = self.check_utilities(player, tile.owner)
            elif tile.group == "Station":
                rent = self.check_stations(tile.owner)

            # # check if player can afford rent
            # if rent > player.net_worth:
            #     # return any player properties to the bank
            #     for prop in player.propList:
            #         self.gui.return_prop(prop)
            #     self.gui.reblit_right()
            #     # remove player from player list
            #     self.players.remove_by_name(player.name)
            #     # reblit lhs
            #     self.gui.reblit_left()
            # # check if player needs to mortgage any properties
            # elif rent > player.money:
            #     pass

            owner = self.players.get_by_name(tile.owner)

            player.deduct_money(rent, True)
            owner.add_money(rent, True)
            self.gui.pay_rent(rent, player, owner)
            self.gui.reblit_left()

    def check_utilities(self, player, owner_name):
        """
        Procedure which takes place if a player lands on a owned utility
        :param player: the player whose turn it currently is
        :param owner_name: the name of the owner of the property
        """

        owner = self.players.get_by_name(owner_name)
        count = self.count_utilities(owner)
        if count == 1:
            rent = (self.current_d1 + self.current_d2) * 4
        elif count == 2:
            rent = (self.current_d1 + self.current_d2) * 4
        else:
            raise Exception("Invalid number of utilities")

        return rent

    def count_utilities(self, player):
        """
        Counts how many utilities a player owns
        :param player: the player in question
        :return: the number of utilities owned by the player
        """

        count = 0
        for prop in player.propList:
            if prop.group == "Utilities":
                count += 1
        return count

    def check_stations(self, owner_name):

        owner = self.players.get_by_name(owner_name)
        count = self.count_stations(owner)

        if count == 1:
            rent = 25
        elif count == 2:
            rent = 50
        elif count == 3:
            rent = 100
        elif count == 4:
            rent = 200
        else:
            raise Exception("Invalid number of stations")

        return rent

    def count_stations(self, player):
        count = 0
        for prop in player.propList:
            if prop.group == "Station":
                count += 1
        return count

    def check_player_position(self, player):
        """
        Procedure which takes place when a player rolls dice and lands on a new tile
        :param player: the player in question
        """

        # TODO: A lot more checks for things such as free parking, properties, etc
        tile = self.tiles[player.pos-1]
        self.gui.check_player_location(player)
        if tile.group == "Go to jail":
            player.jail()
            self.gui.go_jail(player)
        elif tile.pos == 1:
            self.gui.go()
        elif tile.buyable:
            self.check_property(player)
        elif tile.space == "Pot Luck":
            pot = self.pot_cards.next_object()
            pot.execute(player, self.players, self)
            self.gui.pot_luck(pot)
            self.gui.reblit_all()
        elif tile.space == "Opportunity Knocks":
            opp = self.opp_cards.next_object()
            opp.execute(player, self.players, self)
            self.gui.opp_knocks(opp)
            self.gui.reblit_all()
        elif tile.space == "Free Parking":
            player.add_money(self.free_parking_money)
            self.gui.free_parking(player)
            print("[{}] Collected ${} from free parking money".format(player.name, self.free_parking_money))
            self.free_parking_money = 0
        elif tile.space == "Income Tax":
            player.deduct_money(200, True)
            self.gui.income_tax(player)
            print("[{}] Paid $200 for income tax".format(player.name))
        elif tile.space == "Super Tax":
            player.deduct_money(100, True)
            self.gui.super_tax(player)
            print("[{}] Paid $100 for super tax".format(player.name))

    def end_game(self):
        # get net worth of all players and determine who wins
        # temporarily getting player at top of queue
        winner = self.players.get(0)
        self.gui.end_game(winner)



class Queue:
    """
    A Queue data structure implementation
    """

    def __init__(self, objects):
        self.objects = objects

    def shuffle(self):
        """
        shuffles the order of the objects
        """

        random.shuffle(self.objects)

    def next_object(self):
        """
        Gives the next element in the queue and rotates the queue accordingly
        :return: the next object in the queue
        """

        object = self.objects.pop(0)
        self.objects.append(object)
        return object

    def get(self, i):
        """
        Gets a spceific element in the queue
        :param i: The index of the element
        :return: the element at the given index
        """

        return self.objects[i]

    def remove(self):
        """
        Removes an object out of the queue without rotating the queue
        :return: the next object in the queue
        """

        return self.objects.pop(-1)

    def get_length(self):
        """
        Gives the length of the queue
        :return: the length of the queue
        """

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
    """
    Extension of the Queue class with additional functionality for player objects
    """

    def __init__(self, players):
        super().__init__(players)

    def get_by_name(self, name):
        """
        Gets a player with the name provided from the queue
        :param name: the name of the player
        :return: the player with that name
        """

        for obj in self.objects:
            if obj.name == name:
                return obj
        raise Exception("No player with that name! (getting)")

    def remove_by_name(self, name):
        """
        Removes a player from the queue with a specific name
        :param name: the name of the player
        """

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
# players = [AIPlayer(), AIPlayer(), AIPlayer(), AIPlayer()]
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
