import random

class Player:
    def __init__(self, pos, money, propList, laps):
        self.pos = pos
        self.money = money
        self.propList = propList
        self.laps = laps

    def playerRollDice(self):
        dOne = random.randint(1, 7)
        dTwo = random.randint(1, 7)
        return (dOne, dTwo)
