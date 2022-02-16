import openpyxl
from tile import get_cell_ref

potluck = []
opportunity = []

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

    @classmethod
    def load_tiles_from_xlsx(cls, path="ExcelData/PropertyTycoonCardDataRefactored.xlsx"):
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        cards = []

        for row in range(4, 17):
            row_data = []
            for col in range(1, 5):

                cell = get_cell_ref(row, col)

                row_data.append(sheet[cell].value)
            cards.append(TransactionCard(row_data[0], row_data[1], row_data[2], row_data[3]))

        return cards

    def __str__(self):
        string  = "----------- Transaction Card -----------\n"
        string += "Payer: {}\n".format(self.payer)
        string += "Reciever: {}\n".format(self.reciever)
        string += "Amount: {}\n".format(self.amount)
        string += "Description: {}\n".format(self.description)
        string += "----------------------------"
        return string

class MovementCard(Card):
    def __init__(self, relative_pos, tile, pass_go, description): #make sure to change excel to tile to numbers
        self.relative_pos = relative_pos
        self.tile = tile
        self.pass_go = pass_go
        super().__init__(description)

class HouseHotelCard(Card):
    def __init__(self, payer, reciever, house_amount, hotel_amount, description):
        self.payer = payer
        self.reciever = reciever
        self.house_amount = house_amount
        self.hotel_amount = hotel_amount
        super().__init__(description)

class JailfreeCard(Card):
    pass


card = JailfreeCard("jailfree")
print(isinstance(card, Card))

cards1 = TransactionCard.load_tiles_from_xlsx()
for c in cards1:
    print(c)


