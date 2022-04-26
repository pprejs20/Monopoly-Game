import unittest
import openpyxl
from tile import Tile
from cards import *
from player import *
from game import *
from inter import *


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
        player = Player("test1", pos=39)
        self.assertEqual(player.pos, 39)
        player.move_player_forward(1)
        self.assertEqual(player.pos, 0)
        player.move_player_backward(1)
        self.assertEqual(player.pos, 39)

    def test_roll_dice(self):
        player = Player("test")
        d1, d2, double = player.roll_dice()
        possible = [1, 2, 3, 4, 5, 6]
        self.assertTrue(d1 in possible)
        self.assertTrue(d2 in possible)

class TestGame(unittest.TestCase):
    def setUp(self):
        self.p1 = Player("p1", money=1)
        self.p2 = Player("p2", money=2)
        self.p3 = Player("p3", money=3)
        self.queue = Queue([self.p1, self.p2, self.p3])

    def test_player_queue_rotate(self):


        self.assertEqual(self.queue.get(0), self.p1)
        self.queue.next_object()

        self.assertEqual(self.queue.get(0), self.p2)
        self.queue.next_object()

        self.assertEqual(self.queue.get(0), self.p3)
        self.queue.next_object()

        self.assertEqual(self.queue.objects, [self.p1, self.p2, self.p3])

    def test_player_queue_shuffle(self):
        player = self.queue.get(0)
        for i in range(10):
            self.queue.shuffle()
            if player != self.queue.get(0):
                self.assertTrue(True)
                return
        self.assertTrue(False)


class TestUserRequirements(unittest.TestCase):

    def setUp(self):
        players1 = [AIPlayer(token=cat_token, number=1), AIPlayer(token=iron_token, number=2), AIPlayer(token=smartphone_token, number=3)]
        players2 = [Player("Player 1", token=cat_token, number=1), Player("Player 2", token=iron_token, number=2),
                    Player("Player 3", token=smartphone_token, number=3), AIPlayer(token=hatstand_token, number=1)]
        self.game1 = Game(players1)
        self.game2 = Game(players2)

    def test_ai_players(self):
        for i in range(250):
            self.game1.next_step()

        self.assertTrue(True)

    def test_player_numbers(self):
        players = [AIPlayer()]
        try:
            game = Game(players)
        except AssertionError:
            self.assertTrue(True)
            return
        self.assertTrue(False)

    def test_players_start_money(self):
        self.assertEqual(1500, self.game1.players.get(0).money)
        self.assertEqual(1500, self.game1.players.get(1).money)
        self.assertEqual(1500, self.game1.players.get(2).money)

    def test_player_moves_around_board(self):
        player = self.game1.players.get(0)
        initial_pos = player.pos
        self.game1.next_step()
        self.assertTrue(initial_pos != player.pos)
        dice_sum = self.game1.current_d1 + self.game1.current_d2
        self.assertTrue(player.pos == initial_pos + dice_sum)

    def test_card_shuffle(self):
        pot_cards, opp_cards = load_all_cards()
        pot_cards = Queue(pot_cards)
        card1 = pot_cards.get(0)
        card2 = pot_cards.get(1)
        card3 = pot_cards.get(4)
        pot_cards.shuffle()
        self.assertTrue(card1 != pot_cards.get(0) or card2 != pot_cards.get(1) or card3 != pot_cards.get(4))


if __name__ == '__main__':
    unittest.main()







