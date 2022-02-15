class Card:
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description

class TransactionCard(Card):
    def __init__(self, payer, reciever, amount, description):
        self.payer = payer
        self.reciever = reciever
        self.amount = amount
        super().__init__(description)

class MovementCard(Card):
    def __init__(self, relative_pos, tile, pass_go, description): #make sure to change excel to tile to numbers
        self.relative_pos = relative_pos
        self.tile = tile
        self.pass_go = pass_go
        super().__init__(description)

class HouseHotelCard(Card):
    pass

class JailfreeCard(Card):
    pass


card = JailfreeCard("jailfree")
print(isinstance(card, Card))



