
class Tile:
    def __init__(self, pos, space, group, action, buyable, cost,
                baseRent, oneHouseRent, twoHouseRent, threeHouseRent, fourHouseRent,
                hotelRent):
        self.pos = pos
        self.space = space
        self.group = group
        self.action = action
        self.buyable = buyable
        self.cost = cost
        self.baseRent = baseRent
        self.oneHouseRent = oneHouseRent
        self.twoHouseRent = twoHouseRent
        self.threeHouseRent = threeHouseRent
        self.fourHouseRent = fourHouseRent
        self.hotelRent = hotelRent