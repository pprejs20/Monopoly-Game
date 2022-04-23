import random


class Player:
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

    def add_prop(self, tile):
        self.propList.append(tile)

    def move_player_forward(self, amount):
        for i in range(amount):
            if self.pos == 39:
                self.pos = 1
                self.add_money(200)
                print("[{}] Collected $200 for passing go".format(self.name))
                self.laps += 1
            else:
                self.pos += 1

    def move_player_backward(self, amount):
        for i in range(amount):
            if self.pos == 0:
                self.pos = 39
            else:
                self.pos -= 1

    def set_pos(self, pos):
        self.pos = pos

    def move_player(self, amount):
        self.pos += amount

    def is_jailed(self):
        return self.jailed

    def jail(self):
        self.jailed = True
        self.set_pos(11)

    def unjail(self):
        self.jailed = False
        self.jail_term = 0

    def add_jail_term(self):
        self.jail_term += 1
        if self.jail_term == 2:
            self.unjail()
            print("[{}] You served your time, you are now free!".format(self.name))

    def deduct_money(self, amount):
        self.money -= amount

    def add_money(self, amount):
        self.money += amount

    def roll_dice(self):
        dOne = random.randint(1, 6)
        dTwo = random.randint(1, 6)
        doubles = dOne == dTwo
        return (dOne, dTwo, doubles)

    def buy_property(self, tile, cost=None):
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
        return True if len(self.monopolies) > 0 else False

    def get_monopolies(self):
        return self.monopolies

    def count_color(self, color):
        count = 0
        for prop in self.propList:
            if prop.group == color:
                count += 1
        return count

    def get_props_of_color(self, color):
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
    player_count = 1

    def __init__(self, pos=1, money=1500, propList=None, laps=0, token=None):
        if propList is None:
            propList = []
        else:
            pass
        self.propList = [] if propList is None else propList
        name = "AI Player " + str(AIPlayer.player_count)
        AIPlayer.player_count += 1
        super().__init__(name, pos, money, propList, laps, token)


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
