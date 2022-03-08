import random

class Player:
    # TODO: Double check if the start money is correct
    def __init__(self, pos=0, money=1500, propList=[], laps=0):
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




    def move_player(self, amount):
        self.pos += amount

    def roll_dice(self):
        dOne = random.randint(1, 7)
        dTwo = random.randint(1, 7)
        return (dOne, dTwo)


