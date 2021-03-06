import openpyxl


class Tile:
    """
    A class for all necessary functionality involving tiles and properties on the board 
    """

    def __init__(self, pos, space, group, action, buyable, cost,
                 base_rent, one_house_rent, two_house_rent, three_house_rent, four_house_rent,
                 hotel_rent, no_of_houses=0):
        self.no_of_houses = no_of_houses
        self.pos = pos
        self.space = space
        self.group = group
        self.action = action
        self.buyable = buyable
        self.cost = cost
        self.base_rent = base_rent
        self.one_house_rent = one_house_rent
        self.two_house_rent = two_house_rent
        self.three_house_rent = three_house_rent
        self.four_house_rent = four_house_rent
        self.hotel_rent = hotel_rent
        self.owner = None

    @classmethod
    def parse_bool(cls, data):
        """
        Turns string "yes" and "no" values to True or false boolean datatypes 
        :param data: the string that the boolean will be derived from
        :return: True if input is "yes", False if input is "no" 
        """

        if data == 'Yes':
            return True
        elif data == 'No':
            return False
        else:
            # Code should not end up here, this will throw an error
            assert False

    @classmethod
    def load_tiles_from_xlsx(cls, path="ExcelData/PropertyTycoonBoardData.xlsx"):
        """
        Loads all the cards from the xlsx data 
        :param path: the path to the xlsx data
        :return: a list of Tile objects derived from the xlsx data
        """

        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        tiles = []

        # range function is exclusive of the bound
        # range(5, 45) will give numbers 5 to 44
        for row in range(5, 45):
            row_data = []
            for col in range(1, 16):

                # If you look in the excel sheet these columns are not used
                # (Columns C, G, j)
                if col in [3, 7, 10]:
                    continue
                cell = get_cell_ref(row, col)

                # Change 'Yes' and 'No' to True or False for code
                if col == 6:
                    row_data.append(Tile.parse_bool(sheet[cell].value))
                else:
                    row_data.append(sheet[cell].value)
            # print(row_data)
            tiles.append(Tile(row_data[0], row_data[1], row_data[2], row_data[3],
                              row_data[4], row_data[5], row_data[6], row_data[7],
                              row_data[8], row_data[9], row_data[10], row_data[11]))

        return tiles

    def add_house(self):
        """
        Adds a house to the property
        """

        assert self.no_of_houses != 5
        self.no_of_houses += 1

    def remove_house(self):
        """
        Removed a house from the property 
        """

        assert self.no_of_houses > 0
        self.no_of_houses -= 1

    def __str__(self):
        string = "----------- Tile -----------\n"
        string += "Owner: {}\n".format(self.owner)
        string += "Pos: {}\n".format(self.pos)
        string += "Space: {}\n".format(self.space)
        string += "Group: {}\n".format(self.group)
        string += "Action: {}\n".format(self.action)
        string += "Buyable: {}\n".format(self.buyable)
        string += "Cost: {}\n".format(self.cost)
        string += "Base Rent: {}\n".format(self.base_rent)
        string += "  1 House: {}\n".format(self.one_house_rent)
        string += "  2 House: {}\n".format(self.two_house_rent)
        string += "  3 House: {}\n".format(self.three_house_rent)
        string += "  4 House: {}\n".format(self.four_house_rent)
        string += "  Hotel Rent: {}\n".format(self.hotel_rent)
        string += "----------------------------"
        return string


def get_cell_ref(row, col):
    """
    Gets xlsx cell reference given the row and column 
    :param row: row number 
    :param col: column number 
    :return: A string designating a cell in excel 
    """

    # chr(65) is A in ASCII
    return "" + chr(64 + col) + str(row)


# tiles = Tile.load_tiles_from_xlsx()
# for t in tiles:
#     print(t)
