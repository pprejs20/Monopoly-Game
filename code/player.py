import random

class Player:
    def __init__(self, pos, money, propList, laps):
        self.pos = pos
        self.money = money
        self.propList = propList
        self.laps = laps

    def move_player_forward(self, amount):
        for i in range(amount):
            if self.pos == 39:
                self.pos = 0
            else:
                self.pos += 1

    def move_player_backward(self,amount):
        for i in range(amount):
            if self.pos == 0:
                self.pos = 39
            else:
                self.pos -= 1




    def move_Player(self, amount):
        self.pos += amount

    def player_RollDice(self):
        dOne = random.randint(1, 7)
        dTwo = random.randint(1, 7)
        return (dOne, dTwo)


