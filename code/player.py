import random


class Player:
    # TODO: Double check if the start money is correct
    def __init__(self, name, pos=0, money=1500, propList=[], laps=0, token=None):
        self.pos = pos
        self.money = money
        self.propList = propList
        self.laps = laps
        self.name = name
        self.token = token
        self.doubles_count = 0
        self.jailed = False
        self.jail_term = 0

    def add_prop(self, tile):
        self.propList.append(tile)

    def move_player_forward(self, amount):
        for i in range(amount):
            if self.pos == 39:
                self.pos = 0
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
        self.set_pos(10)

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
