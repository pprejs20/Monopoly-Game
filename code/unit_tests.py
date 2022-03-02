import unittest
import openpyxl
from tile import Tile

class TestTile(unittest.TestCase):

    def test_load_tiles_from_xlsx(self):
        tile = Tile.load_tiles_from_xlsx()[0]

        self.assertEqual(tile.pos, 1)
        self.assertEqual(tile.space, "Go")
        self.assertEqual(tile.group, None)
        self.assertEqual(tile.action, "Collect £200")
        self.assertEqual(tile.buyable, False)
        self.assertEqual(tile.cost, None)
        self.assertEqual(tile.base_rent, None)
        self.assertEqual(tile.one_house_rent, None)
        self.assertEqual(tile.two_house_rent, None)
        self.assertEqual(tile.three_house_rent, None)
        self.assertEqual(tile.four_house_rent, None)
        self.assertEqual(tile.hotel_rent, None)

    def test_xlsx_change(self):
        row = 5
        original_tile = Tile.load_tiles_from_xlsx("ExcelData\TestingPropertyTycoonBoardData.xlsx")[0]
        workbook = openpyxl.load_workbook("ExcelData\TestingPropertyTycoonBoardData.xlsx")
        sheet = workbook.active

        sheet["A5"].value = 55
        sheet["B5"].value = "Testing1"
        sheet["D5"].value = "Testing2"
        sheet["F5"].value = "Yes"
        workbook.save("ExcelData\TestingPropertyTycoonBoardData.xlsx")

        changed_tile = Tile.load_tiles_from_xlsx("ExcelData\TestingPropertyTycoonBoardData.xlsx")[0]
        self.assertEqual(changed_tile.pos, 55)
        self.assertEqual(changed_tile.space, "Testing1")
        self.assertEqual(changed_tile.group, "Testing2")
        self.assertTrue(changed_tile.buyable)

        sheet["A5"].value = 1
        sheet["B5"].value = "Go"
        sheet["D5"].value = None
        sheet["F5"].value = "No"
        workbook.save("ExcelData\TestingPropertyTycoonBoardData.xlsx")

class TestCard(unittest.TestCase):


