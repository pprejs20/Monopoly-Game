import random

class Player:
    # TODO: Double check if the start money is correct
    def __init__(self, pos=0, money=1500, propList=[], laps=0):
        self.pos = pos
        self.money = money
        self.propList = propList
        self.laps = laps
        self.doubles_count = 0
        self.jailed = False

    def move_player_forward(self, amount):
        for i in range(amount):
            if self.pos == 39:
                self.pos = 0
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

    def next_step(self):
        doubles = False
        dice_rolls = self.roll_dice()

        if dice_rolls[0] == dice_rolls[1]:
            doubles = True
            self.doubles_count += 1

            if self.doubles_count == 3:
                self.set_pos(10)
                self.jailed = True
                return

        dice_sum = dice_rolls[0] + dice_rolls[1]
        self.move_player(dice_sum)

    def roll_dice(self):
        dOne = random.randint(1, 6)
        dTwo = random.randint(1, 6)
        return (dOne, dTwo)

    def __str__(self):
        string = "----------- Player -----------\n"
        string += "Pos: {}\n".format(self.pos)
        string += "Money: {}\n".format(self.money)
        string += "Owned Properties: {}\n".format(len(self.propList))
        string += "Laps: {}\n".format(self.laps)
        string += "------------------------------\n"
        return string




