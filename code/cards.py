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
    def load_transaction_card_from_xlsx(cls, path="ExcelData/PropertyTycoonCardDataRefactored.xlsx"):
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        pot_cards = []
        opp_cards = []

        for row in range(4, 17):
            row_data = []
            for col in range(1, 5):

                cell = get_cell_ref(row, col)

                row_data.append(sheet[cell].value)
            pot_cards.append(TransactionCard(row_data[0], row_data[1], row_data[2], row_data[3]))

        for row in range(29, 35):
            row_data = []
            for col in range(1, 5):

                cell = get_cell_ref(row, col)

                row_data.append(sheet[cell].value)
            opp_cards.append(TransactionCard(row_data[0], row_data[1], row_data[2], row_data[3]))

        return pot_cards, opp_cards

    def __str__(self):
        string  = "----------- Transaction Card -----------\n"
        string += "Payer: {}\n".format(self.payer)
        string += "Reciever: {}\n".format(self.reciever)
        string += "Amount: {}\n".format(self.amount)
        string += "Description: {}\n".format(self.description)
        string += "----------------------------"
        return string

class MovementCard(Card):
    def __init__(self, relative_pos, tile, pass_go, description):
        self.relative_pos = relative_pos
        self.tile = tile
        self.pass_go = pass_go
        super().__init__(description)

    @classmethod
    def load_movement_card_from_xlsx(cls, path="ExcelData/PropertyTycoonCardDataRefactored.xlsx"):
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        pot_cards = []
        opp_cards = []

        for row in range(19, 22):
            row_data = []
            for col in range(1, 5):
                cell = get_cell_ref(row, col)

                row_data.append(sheet[cell].value)
            pot_cards.append(MovementCard(row_data[0], row_data[1], row_data[2], row_data[3]))

        for row in range(41, 48):
            row_data = []
            for col in range(1, 5):
                cell = get_cell_ref(row, col)

                row_data.append(sheet[cell].value)
            opp_cards.append(MovementCard(row_data[0], row_data[1], row_data[2], row_data[3]))

        return pot_cards, opp_cards

    def __str__(self):
        string = "----------- Movement Card -----------\n"
        string += "Relative position: {}\n".format(self.relative_pos)
        string += "Tile: {}\n".format(self.tile)
        string += "Pass go: {}\n".format(self.pass_go)
        string += "Description: {}\n".format(self.description)
        string += "----------------------------"
        return string

class HouseHotelCard(Card):
    def __init__(self, payer, reciever, house_amount, hotel_amount, description):
        self.payer = payer
        self.reciever = reciever
        self.house_amount = house_amount
        self.hotel_amount = hotel_amount
        super().__init__(description)

    @classmethod
    def load_hh_card_from_xlsx(cls, path="ExcelData/PropertyTycoonCardDataRefactored.xlsx"):
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        cards = []

        for row in range(37, 39):
            row_data = []
            for col in range(1, 6):
                cell = get_cell_ref(row, col)

                row_data.append(sheet[cell].value)
            cards.append(HouseHotelCard(row_data[0], row_data[1], row_data[2], row_data[3], row_data[4]))

        return cards

    def __str__(self):
        string = "----------- HH Card -----------\n"
        string += "Payer: {}\n".format(self.payer)
        string += "Reciever: {}\n".format(self.reciever)
        string += "House amount: {}\n".format(self.house_amount)
        string += "Hotel amount: {}\n".format(self.hotel_amount)
        string += "Description: {}\n".format(self.description)
        string += "----------------------------"
        return string

class JailfreeCard(Card):
    def __init__(self, description):
        super().__init__(description)

    @classmethod
    def load_jail_card_from_xlsx(cls, path="ExcelData/PropertyTycoonCardDataRefactored.xlsx"):
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        cards = []

        for row in range(24, 25):
            row_data = []
            for col in range(1, 2):
                cell = get_cell_ref(row, col)

                row_data.append(sheet[cell].value)
            cards.append(JailfreeCard(row_data[0]))

        return cards

    def __str__(self):
        string = "----------- Jail Free Card -----------\n"
        string += "Description: {}\n".format(self.description)
        string += "----------------------------"
        return string


#card = JailfreeCard("jailfree")
#print(isinstance(card, Card))

# cards1, cards2 = TransactionCard.load_transaction_card_from_xlsx()
# for c in cards1:
#     print(c)
# for c1 in cards2:
#     print(c1)

cards1, cards2 = MovementCard.load_movement_card_from_xlsx()
for c in cards1:
    print(c)
for c1 in cards2:
    print(c1)



#cards3 = JailfreeCard.load_jail_card_from_xlsx()
#for c in cards3:
#   print(c)

# cards4 = HouseHotelCard.load_hh_card_from_xlsx()
# for c in cards4:
#     print(c)





