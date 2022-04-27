import random


class Player:
    """
    A class which encapsulates all functionality required for a player in the game
    """

    # TODO: Double check if the start money is correct
    def __init__(self, name, pos=1, money=1500, propList=None, laps=0, token=None, number=None, jailCard=0):
        self.jailCard = jailCard
        self.pos = pos
        self.money = money

        if propList is None:
            self.propList = []
        else:
            self.propList = propList

        self.laps = laps
        self.name = name
        self.token = token
        self.doubles_count = 0
        self.jailed = False
        self.jail_term = 0
        self.number = number
        self.monopolies = []
        self.net_worth = self.money
        self.bankrupt = False

    def add_prop(self, tile):
        """
        Adds a property to the players property list
        :param tile: the property to be added
        """

        self.propList.append(tile)

    def move_player_forward(self, amount):
        """
        Moves the player forward by an x amount
        :param amount: the number of spaces the player should be moved
        """

        for i in range(amount):
            if self.pos == 40:
                self.pos = 1
                self.add_money(200)
                print("[{}] Collected $200 for passing go".format(self.name))
                self.laps += 1
            else:
                self.pos += 1

    def move_player_backward(self, amount):
        """
        Moves the player backwards by an x amount
        :param amount: the number of spaces the player should be moved
        """

        for i in range(amount):
            if self.pos == 1:
                self.pos = 40
            else:
                self.pos -= 1

    def set_pos(self, pos):
        """
        Sets the players position
        :param pos: the position number
        """

        self.pos = pos

    def move_player(self, amount):
        """
        Moves the player by a specified a
        :param amount:
        :return:
        """

        self.pos += amount

    def is_jailed(self):
        """
        Checks if a player is jailed
        :return: True if the player is jailed, otherwise False
        """

        return self.jailed

    def jail(self):
        """
        Procedure for jailing the player
        """

        self.jailed = True
        self.set_pos(11)

    def unjail(self):
        """
        Unjails the player
        """

        self.jailed = False
        self.jail_term = 0

    def add_jail_term(self):
        """
        Adds a term once a player has missed a go because of being in jail
        """

        self.jail_term += 1
        if self.jail_term == 2:
            self.unjail()
            print("[{}] You served your time, you are now free!".format(self.name))

    def sell_property(self, game, amount):
        while self.money < amount:
            for i, prop in enumerate(self.propList):
                print(i, prop, prop.cost)
            ans = input("Enter prop index to sell")
            self.propList[ans].buyable = True
            self.propList[ans].owner = None
            game.gui.return_prop(self.propList[ans])
            no = self.propList[ans].no_of_house
            if no > 0:
                amount = house_costs[self.propList[ans].group] * no
                amount += self.propList[ans].cost
            else:
                amount = self.propList[ans].cost
            self.propList.pop(ans)
            self.add_money(amount)



    def deduct_money(self, amount, game, net_worth_deduction=False):
        """
        Takes money away from the player
        :param amount: the amount of money that will be deducted
        """

        if self.net_worth < amount:
            game.players.remove_by_name(self.name)
            for prop in self.propList:
                prop.buyable = True
                prop.owner = None
                game.gui.return_prop(prop)
            return

        if self.money < amount:
            self.sell_property(game, amount)

        self.money -= amount
        if net_worth_deduction:
            self.net_worth -= amount



    def add_money(self, amount, net_worth_increase=True):
        """
        Gives the player money
        :param amount: the amount of money to be added
        """

        self.money += amount
        if net_worth_increase:
            self.net_worth += amount

    def roll_dice(self):
        """
        Rolls dice for the player
        :return: 2 integers representing the numbers rolled on 2 separate die and a boolean value indicating if
        its a double
        """

        dOne = random.randint(1, 6)
        dTwo = random.randint(1, 6)
        doubles = dOne == dTwo
        return (dOne, dTwo, doubles)

    def buy_property(self, tile, cost=None):
        """
        Purchases a property for the player
        :param tile: the property which is to be purchased
        :param cost: optional cost value if the price is not the original price of the property
        """

        if cost is None:
            cost = tile.cost

        self.deduct_money(cost)
        tile.owner = self.name
        self.add_prop(tile)

        if tile.group in tiles_of_color.keys():
            num = self.count_color(tile.group)

            if num == tiles_of_color[tile.group]:
                self.monopolies.append(tile.group)

    def has_monopoly(self):
        """
        Checks if the player has a monopoly
        :return: True if the player has a monopoly, Fasle otherwise
        """

        return True if len(self.monopolies) > 0 else False

    def get_monopolies(self):
        """
        Gets a list of monopolies owned by the player
        :return: List of monopolies
        """

        return self.monopolies

    def count_color(self, color):
        """
        Counts how many properties of a color the player owns
        :param color: the color of the properties
        :return: the number of properties owned of the specified color
        """

        count = 0
        for prop in self.propList:
            if prop.group == color:
                count += 1
        return count

    def get_props_of_color(self, color):
        """
        Gets the properties of the same color owned by the player
        :param color: the desired color of the properties
        :return: a list of the properties of the color owned by the player
        """

        props = []
        for prop in self.propList:
            if prop.group == color:
                props.append(prop)
        return props


    def __str__(self):
        string = "----------- Player -----------\n"
        string += "Name: {}\n".format(self.name)
        string += "Token: {}\n".format(self.token)
        string += "Pos: {}\n".format(self.pos)
        string += "Money: {}\n".format(self.money)
        string += "Owned Properties: {}\n".format(len(self.propList))
        string += "Laps: {}\n".format(self.laps)
        string += "------------------------------\n"
        return string


class AIPlayer(Player):
    """
    An extension of the Player class which can work autonomously without a human player
    """

    player_count = 1

    def __init__(self, pos=1, money=1500, propList=None, laps=0, token=None, number=None, jailCard=0):
        if propList is None:
            propList = []
        else:
            pass
        self.propList = [] if propList is None else propList
        name = "AI Player " + str(AIPlayer.player_count)
        AIPlayer.player_count += 1
        super().__init__(name, pos, money, propList, laps, token, number, jailCard)


tiles_of_color = {
    "Brown": 2,
    "Blue": 3,
    "Purple": 3,
    "Orange": 3,
    "Red": 3,
    "Yellow": 3,
    "Green": 3,
    "Deep blue": 2
}

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
