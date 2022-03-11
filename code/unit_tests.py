import unittest
import openpyxl
from tile import Tile
from cards import *
from player import *
from game import *


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

    def test_load_cards(self):
        potluck, opportunity = load_all_cards()

        pot_card = potluck[0]
        opportunity = opportunity[0]

        self.assertEqual(pot_card.payer, "bank")
        self.assertEqual(pot_card.reciever, "player")
        self.assertEqual(pot_card.amount, 200)
        self.assertEqual(pot_card.description, '"You inherit £200"')

        self.assertEqual(opportunity.payer, "bank")
        self.assertEqual(opportunity.reciever, "player")
        self.assertEqual(opportunity.amount, 50)
        self.assertEqual(opportunity.description, '"Bank pays you divided of £50"')

class TestPlayer(unittest.TestCase):

    def test_player_move(self):
        player = Player(pos=39)
        self.assertEqual(player.pos, 39)
        player.move_player_forward(1)
        self.assertEqual(player.pos, 0)
        player.move_player_backward(1)
        self.assertEqual(player.pos, 39)

    def test_roll_dice(self):
        player = Player()
        d1, d2 = player.roll_dice()
        possible = [1, 2, 3, 4, 5, 6]
        self.assertTrue(d1 in possible)
        self.assertTrue(d2 in possible)

class TestGame(unittest.TestCase):
    def test_player_queue_rotate(self):
        p1 = Player(money=1)
        p2 = Player(money=2)
        p3 = Player(money=3)
        queue = PlayerQueue([p1, p2, p3])

        self.assertEqual(queue.get(0), p1)
        queue.next_player()

        self.assertEqual(queue.get(0), p2)
        queue.next_player()

        self.assertEqual(queue.get(0), p3)
        queue.next_player()
        
        self.assertEqual(queue.players, [p1, p2, p3])






