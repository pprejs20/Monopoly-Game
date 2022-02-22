import random

class Player:
    def __init__(self, pos, money, propList, laps):
        self.pos = pos
        self.money = money
        self.propList = propList
        self.laps = laps

    def move_player(self, amount):
        for i in range(amount):
            if self.pos == 39:
                self.pos = 0
            else:
                self.pos += 1


    def playerRollDice(self):
        dOne = random.randint(1, 7)
        dTwo = random.randint(1, 7)
        return (dOne, dTwo)


