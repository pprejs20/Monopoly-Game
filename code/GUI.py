import datetime
import time

import pygame
from game import Game
from player import Player, AIPlayer
from tile import Tile

pygame.init()
# ef978b

start_screen_size = (800, 800)
game_size = (1650, 975)
screen = pygame.display.set_mode(start_screen_size)
pygame.display.set_caption('Property Tycoon')
pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(740, 740, 60, 60))
# define board height and width
board_height = board_width = game_size[1]
# define tile width
tile_width = 82.5
# define tile height
tile_height = 116.25
board = pygame.image.load("Images/Board2.png")
board_right = pygame.image.load("Images/BoardRightSide.png")
play_original = pygame.image.load("Images/PlayOriginal.png")
play_abridged = pygame.image.load("Images/PlayAbridged.png")
logo = pygame.image.load("Images/Logo.png")
one_player = pygame.image.load("Images/1Player.png")
# 100x100
two_player = pygame.image.load("Images/2Player.png")
three_player = pygame.image.load("Images/3Player.png")
four_player = pygame.image.load("Images/4Player.png")
five_player = pygame.image.load("Images/5Player.png")
six_player = pygame.image.load("Images/6Player.png")
zero_player = pygame.image.load("Images/0player.png")
no_of_human_players = pygame.image.load("Images/NoHumanPlayers.png")
# 620x200
no_of_ai_players = pygame.image.load("Images/NoAIPlayers.png")
# 620x200
game_mode = pygame.image.load("Images/GameMode.png")
# 300x100
human_players = pygame.image.load("Images/HumanPlayers.png")
# 300x100
ai_players = pygame.image.load("Images/AIPlayers.png")
start_game = pygame.image.load("Images/StartGame.png")
# 200x100
back = pygame.image.load("Images/Back.png")
name = pygame.image.load("Images/Name.png")
choose_icon = pygame.image.load("Images/ChooseIcon.png")
smartphone = pygame.image.load("Images/smartphone.png")
cat = pygame.image.load("Images/cat.png")
boot = pygame.image.load("Images/boot.png")
iron = pygame.image.load("Images/iron.png")
ship = pygame.image.load("Images/ship.png")
hatstand = pygame.image.load("Images/hatstand.png")
next_button = pygame.image.load("Images/Next.png")
# resized icons to go on board (width limit = 31, height limit = 22)
smartphone_token = pygame.transform.scale(smartphone, (11, 22))
cat_token = pygame.transform.scale(cat, (31, 23))
boot_token = pygame.transform.scale(boot, (29, 26))
iron_token = pygame.transform.scale(iron, (31, 25))
ship_token = pygame.transform.scale(ship, (13, 22))
hatstand_token = pygame.transform.scale(hatstand, (6, 22))
# get the tile data from excel
tiles = Tile.load_tiles_from_xlsx("ExcelData/PropertyTycoonBoardData.xlsx")
# load images of the property indicators (one for each property group, station, and the two utilities) and append
# them to a list
brown1 = pygame.image.load("Images/Brown.png")
brown2 = pygame.image.load("Images/Brown.png")
lblue1 = pygame.image.load("Images/LightBlue.png")
lblue2 = pygame.image.load("Images/LightBlue.png")
lblue3 = pygame.image.load("Images/LightBlue.png")
pink1 = pygame.image.load("Images/Pink.png")
pink2 = pygame.image.load("Images/Pink.png")
pink3 = pygame.image.load("Images/Pink.png")
orange1 = pygame.image.load("Images/Orange.png")
orange2 = pygame.image.load("Images/Orange.png")
orange3 = pygame.image.load("Images/Orange.png")
red1 = pygame.image.load("Images/Red.png")
red2 = pygame.image.load("Images/Red.png")
red3 = pygame.image.load("Images/Red.png")
yellow1 = pygame.image.load("Images/Yellow.png")
yellow2 = pygame.image.load("Images/Yellow.png")
yellow3 = pygame.image.load("Images/Yellow.png")
green1 = pygame.image.load("Images/Green.png")
green2 = pygame.image.load("Images/Green.png")
green3 = pygame.image.load("Images/Green.png")
dblue1 = pygame.image.load("Images/DarkBlue.png")
dblue2 = pygame.image.load("Images/DarkBlue.png")
station1 = pygame.image.load("Images/Station.png")
station2 = pygame.image.load("Images/Station.png")
station3 = pygame.image.load("Images/Station.png")
station4 = pygame.image.load("Images/Station.png")
elec = pygame.image.load("Images/Electric.png")
water = pygame.image.load("Images/Water.png")
prop_indicators = [brown1, brown2, lblue1, lblue2, lblue3, pink1, pink2, pink3, orange1, orange2, orange3, red1, red2,
                   red3, yellow1, yellow2, yellow3, green1, green2, green3, dblue1, dblue2, station1, station2,
                   station3, station4, elec, water]
# get out of jail free indicator
gjf = pygame.image.load("Images/GJF.png")
# load player template image for left hand side of board
playerTemplate = pygame.image.load("Images/PlayerTemplate.png")
# load pot luck and opportunity knocks templates
pot_luck = pygame.image.load("Images/PotLuck.png")
opp_knocks = pygame.image.load("Images/OppKnocks.png")
# load hat for indicating current player
hat = pygame.image.load("Images/Hat.png")
# load dice images
dice1 = pygame.image.load("Images/dice1.png")
dice2 = pygame.image.load("Images/dice2.png")
dice3 = pygame.image.load("Images/dice3.png")
dice4 = pygame.image.load("Images/dice4.png")
dice5 = pygame.image.load("Images/dice5.png")
dice6 = pygame.image.load("Images/dice6.png")
dices = [dice1, dice2, dice3, dice4, dice5, dice6]
# create font to be used
font = pygame.font.SysFont('franklingothicmediumcond', 15)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# create dictionary for the bank property indicators
bank_prop_list = {}
for i in [2, 4, 7, 9, 10, 12, 14, 15, 17, 19, 20, 22, 24, 25, 27, 28, 30, 32, 33, 35, 38, 40, 6, 16, 26, 36, 13, 29]:
    # create entry that has key of the current property being looked at and value is corresponding indicator
    bank_prop_list[tiles[i - 1].space] = prop_indicators.pop(0)

# create dictionary for the player property indicators (x and y coordinates of each indicator are relative to player 1)
player_prop_ind = {}
# variable for which indicator is being looked at to know when to drop a line
i = 1
# x value of first indicator
x = 2
# y value of first indicator
y = 76
# for each indicator
for key in bank_prop_list:
    # if at the end of the line drop a new line
    if i == 15:
        x = 2
        y += 50
    # rescale the indicator to fit on right side
    ind = bank_prop_list[key]
    ind = pygame.transform.scale(ind, (29, 43))
    # store the indicator its coordinates in the dictionary
    player_prop_ind[key] = (ind, (x, y))
    # increment x value to move along the line
    x += 32
    i += 1

# create dictionary for dice images
dice_images = {}
for i in range(1, 7):
    dice_images[i] = dices.pop(0)


def blit_bank_prop():
    """
    Function to blit the property indicators on the right side of the board (i.e. not yet purchased)
    :return:
    """
    screen.blit(board_right, (1425, 0))
    ctr = 1
    # coordinates of first tile
    x = 1435 - (44 + 10)
    y = 60
    for prop in bank_prop_list.values():
        # tile that are on the start of line (drop new line)
        if ctr in [3, 6, 9, 12, 15, 18, 21, 23, 27]:
            # back to far left
            x = 1435
            # increase by height and gap between lines
            y += (65 + 20)
        else:
            # otherwise, increment by width of tile plus space in between
            x += (44 + 10)
        ctr += 1
        screen.blit(prop, (x, y))


def blit_player_indicators(player_no, player):
    """
    Function to blit the player name, money, and indicators of a player
    :param player_no: the player number (i.e.: player 1, 2, 3, etc.)
    :param player: the player whose information is being displayed
    :return:
    """
    # variable to determine how high/low to display the information (dependent on player_no)
    y_inc = (player_no - 1) * 155
    # blit the template at the correct height
    screen.blit(playerTemplate, (0, (22.5 + y_inc)))
    # blit the player name and money
    font1 = pygame.font.SysFont('franklingothicmediumcond', 30)
    name = font1.render(player.name, True, WHITE)
    money = font1.render("£" + str(player.money), True, WHITE)
    screen.blit(name, (10, (30 + y_inc)))
    screen.blit(money, (287, (30 + y_inc)))
    # blit the indicators for the properties the player owns
    for prop in player.propList:
        indicator = player_prop_ind[prop.space][0]
        x = player_prop_ind[prop.space][1][0]
        y = player_prop_ind[prop.space][1][1] + y_inc
        screen.blit(indicator, (x, y))
    # blit the Get out of Jail card if the player owns one
    if player.jailCard > 0:
        card = pygame.transform.scale(gjf, (29, 43))
        screen.blit(card, (227, 28.5))
    # blit the net_worth toggle button
    toggle_button = pygame.Rect(325, 955.5, 100, 16.5)
    pygame.draw.rect(screen, WHITE, toggle_button)
    toggle_txt = font.render("Net Worth", True, BLACK)
    toggle_rect = toggle_txt.get_rect()
    toggle_rect.center = toggle_button.center
    screen.blit(toggle_txt, toggle_rect)
    # blit end game button
    end_button = pygame.Rect(25, 955.5, 100, 16.5)
    pygame.draw.rect(screen, WHITE, end_button)
    end_txt = font.render("End Game", True, BLACK)
    end_rect = end_txt.get_rect()
    end_rect.center = end_button.center
    screen.blit(end_txt, end_rect)
    pygame.display.update()


# function to get the coordinates of each tile on board
def get_coordinates():
    """
    Function to populate a list with the coordinates of the top left corner of each tile (takes into consideration
     orientation of the tiles).
    :return: the list of coordinates
    """
    # create list to store the coordinates of each tile
    coord_list = []
    # iterator to go through the 40 tiles
    i = 1

    # first get screen width without board because there is space on either side of board (2/3 on left and 1/3 on
    # right)
    screen_width_excl_board = game_size[0] - board_width

    # BOTTOM ROW:
    # x starts where board ends minus the height of a tile (because first tile, GO, is in bottom right)
    x = (game_size[0] - screen_width_excl_board * (1 / 3)) - tile_height
    # y is the screen height minus height of a tile (because there is no space below board)
    y = game_size[1] - tile_height
    for i in range(1, 11):
        # for first row (bottom) y stays the same and x decreases by width of a tile each iteration
        coord_list.append((x, y))
        x -= tile_width

    # LEFT ROW:
    # x is where the board starts plus the height of a tile
    x = (screen_width_excl_board * (2 / 3)) + tile_height
    # y starts at screen height - height of a tile
    y = game_size[1] - tile_height
    for i in range(11, 21):
        # for second row (left) x stays the same and y decreases by width of a tile each iteration
        coord_list.append((x, y))
        y -= tile_width

    # TOP ROW:
    # x starts at the where the board starts plus height of a tile
    x = (screen_width_excl_board * (2 / 3)) + tile_height
    # y is the height of a tile (because there is no space above the board)
    y = tile_height
    for i in range(21, 31):
        # for third row (top) y stays the same and x increases by width of tile each iteration
        coord_list.append((x, y))
        x += tile_width

    # RIGHT ROW:
    # x is where the board ends minus the height of a tile
    x = (game_size[0] - screen_width_excl_board * (1 / 3)) - tile_height
    # y starts at the height of a tile
    y = tile_height
    for i in range(31, 41):
        coord_list.append((x, y))
        y += tile_width

    return coord_list


def wrap_text(text, width):
    """
    Function to wrap text within a given width
    :param text: string to be wrapped
    :param width: width which is the limit
    :return:
    """
    # create list to store rendered text images
    imgs = []
    # render image of string
    string_img = font.render(text, True, BLACK)
    # check width to see if it fits in tile (with gap of 7.5 px on either side)
    if string_img.get_rect().width > width:
        # split given string into words
        words = text.split()

        # get ready to loop through all the words
        while len(words) > 0:
            # create list to store words in a line
            line = []
            # add word until they no longer fit the width
            while len(words) > 0:
                line.append(words.pop(0))
                width1, height1 = font.size(' '.join(line + words[:1]))
                if width1 > width:
                    break

            # append the words that did fit in the line
            ln = ' '.join(line)
            imgs.append(ln)
    else:
        # append the inputted string if it did not need to be
        imgs.append(text)
    return imgs


# function to get the text for each tile
def get_text(tiles_set):
    """
    Function to display the text corresponding to each tile on the board
    :return:
    """
    # get tile coordinates
    tiles_coord = get_coordinates()
    # write the text for each tile
    for t in tiles_set:
        # get current tile's position
        curr_pos = t.pos
        # skip non-customisable tiles (corners, pot lucks, opportunity knocks, and taxes)
        if curr_pos in [1, 3, 5, 8, 11, 18, 21, 23, 31, 34, 37, 39]:
            continue
        else:
            # get text for name and pass to wrap text function
            text = t.space
            name = wrap_text(text, 64.5)
            # get text for price
            price = str(t.cost)
            # get text for house/hotel
            txt = ""
            if t.no_of_houses > 0:
                count = str(t.no_of_houses)
                if t.no_of_houses == 5:
                    txt = "Hotel"
                else:
                    txt = "Houses: {}".format(count)

            # for the bottom row
            if curr_pos < 11:
                # set a margin for the text y coordinate (check if its train station)
                if curr_pos == 6:
                    buffer = 2
                else:
                    # takes into account the property rectangle
                    buffer = 32
                # print name
                for names in name:
                    name_img = font.render(names, True, BLACK)
                    name_img_rect = name_img.get_rect()
                    name_img_rect.centerx = (tiles_coord[curr_pos - 1][0] + (tile_width / 2))
                    name_img_rect.y = tiles_coord[curr_pos - 1][1] + buffer
                    screen.blit(name_img, name_img_rect)
                    buffer += name_img_rect.height
                # print price
                price_img = font.render('£' + price, True, BLACK)
                price_img_rect = price_img.get_rect()
                price_img_rect.centerx = (tiles_coord[curr_pos - 1][0] + (tile_width / 2))
                price_img_rect.y = (tiles_coord[curr_pos - 1][1] + tile_height) - (2 + price_img_rect.height)
                screen.blit(price_img, price_img_rect)
                # print number of houses
                houses_img = font.render(txt, True, BLACK)
                houses_rect = houses_img.get_rect()
                houses_rect.centerx = (tiles_coord[curr_pos - 1][0] + (tile_width / 2))
                houses_rect.y = tiles_coord[curr_pos - 1][1] + 2
                screen.blit(houses_img, houses_rect)

            # for the left row
            elif curr_pos < 21:
                # set a margin for the text y coordinate (check if its utility or train station)
                if curr_pos in [13, 16]:
                    buffer = 2
                else:
                    # takes into account the property rectangle
                    buffer = 32
                # print name
                for names in name:
                    name_img = font.render(names, True, BLACK)
                    name_img = pygame.transform.rotate(name_img, -90)
                    name_img_rect = name_img.get_rect()
                    name_img_rect.centery = (tiles_coord[curr_pos - 1][1] + (tile_width / 2))
                    buffer += name_img_rect.width
                    name_img_rect.x = tiles_coord[curr_pos - 1][0] - buffer
                    screen.blit(name_img, name_img_rect)
                # print price
                price_img = font.render('£' + price, True, BLACK)
                price_img = pygame.transform.rotate(price_img, -90)
                price_img_rect = price_img.get_rect()
                price_img_rect.centery = (tiles_coord[curr_pos - 1][1] + (tile_width / 2))
                price_img_rect.x = (tiles_coord[curr_pos - 1][0] - tile_height) + 2
                screen.blit(price_img, price_img_rect)
                # print number of houses
                houses_img = font.render(txt, True, BLACK)
                houses_rect = houses_img.get_rect()
                houses_rect.centery = (tiles_coord[curr_pos - 1][1] + (tile_width / 2))
                houses_rect.x = tiles_coord[curr_pos - 1][0] - 2
                screen.blit(houses_img, houses_rect)

            # for the top row
            elif curr_pos < 31:
                # set a margin for the text y coordinate (check if its train station)
                if curr_pos in [26, 29]:
                    buffer = 2
                else:
                    # takes into account the property rectangle
                    buffer = 32
                # print name
                for names in name:
                    name_img = font.render(names, True, BLACK)
                    name_img = pygame.transform.rotate(name_img, 180)
                    name_img_rect = name_img.get_rect()
                    name_img_rect.centerx = (tiles_coord[curr_pos - 1][0] - (tile_width / 2))
                    buffer += name_img_rect.height
                    name_img_rect.y = tiles_coord[curr_pos - 1][1] - buffer
                    screen.blit(name_img, name_img_rect)
                # print price
                price_img = font.render('£' + price, True, BLACK)
                price_img = pygame.transform.rotate(price_img, 180)
                price_img_rect = price_img.get_rect()
                price_img_rect.centerx = (tiles_coord[curr_pos - 1][0] - (tile_width / 2))
                price_img_rect.y = 2
                screen.blit(price_img, price_img_rect)
                # print number of houses
                houses_img = font.render(txt, True, BLACK)
                houses_rect = houses_img.get_rect()
                houses_rect.centerx = (tiles_coord[curr_pos - 1][0] + (tile_width / 2))
                houses_rect.y = tiles_coord[curr_pos - 1][1] - 2
                screen.blit(houses_img, houses_rect)

            # for the right row
            else:
                # set a margin for the text y coordinate (check if its utility or train station)
                if curr_pos == 36:
                    buffer = 2
                else:
                    # takes into account the property rectangle
                    buffer = 32
                # print name
                for names in name:
                    name_img = font.render(names, True, BLACK)
                    name_img = pygame.transform.rotate(name_img, 90)
                    name_img_rect = name_img.get_rect()
                    name_img_rect.centery = (tiles_coord[curr_pos - 1][1] - (tile_width / 2))
                    name_img_rect.x = tiles_coord[curr_pos - 1][0] + buffer
                    screen.blit(name_img, name_img_rect)
                    buffer += name_img_rect.width
                # print price
                price_img = font.render('£' + price, True, BLACK)
                price_img = pygame.transform.rotate(price_img, 90)
                price_img_rect = price_img.get_rect()
                price_img_rect.centery = (tiles_coord[curr_pos - 1][1] - (tile_width / 2))
                price_img_rect.x = (tiles_coord[curr_pos - 1][0] + tile_height) - (2 + price_img_rect.width)
                screen.blit(price_img, price_img_rect)
                # print number of houses
                houses_img = font.render(txt, True, BLACK)
                houses_img = pygame.transform.rotate(houses_img, 90)
                houses_rect = houses_img.get_rect()
                houses_rect.centery = (tiles_coord[curr_pos - 1][1] + (tile_width / 2))
                houses_rect.x = tiles_coord[curr_pos - 1][0] + 2
                screen.blit(houses_img, houses_rect)
    pygame.display.update()


# function to blit a players token  on the board
def token_blit(number, tile_pos, token):
    """
    Function to blit each player's token on the board
    :param number: whether it is player 1, 2, 3, etc.
    :param tile_pos: the number of the tile to blit onto
    :param token: the token to blit
    :return:
    """
    # get the coordinates of all the tiles
    coordinates = get_coordinates()
    # get the top left corner of the current tile token is being blitted on to
    x, y = coordinates[tile_pos - 1]
    # BOTTOM ROW
    if tile_pos < 11:
        # player 1 token goes in top left
        if number == 1:
            x += 22 - token.get_rect().width / 2
            y += 47.5 - token.get_rect().height / 2
        # player 2 token goes top right
        elif number == 2:
            x += 63 - token.get_rect().width / 2
            y += 47.5 - token.get_rect().height / 2
        # player 3 token goes middle left
        elif number == 3:
            x += 22 - token.get_rect().width / 2
            y += 74.5 - token.get_rect().height / 2
        # player 4 token goes middle right
        elif number == 4:
            x += 63 - token.get_rect().width / 2
            y += 74.5 - token.get_rect().height / 2
        # player 5 token goes bottom left
        elif number == 5:
            x += 22 - token.get_rect().width / 2
            y += 101.5 - token.get_rect().height / 2
        # player 6 token goes bottom right
        elif number == 6:
            x += 63 - token.get_rect().width / 2
            y += 101.5 - token.get_rect().height / 2
    # LEFT ROW
    elif tile_pos < 21:
        token = pygame.transform.rotate(token, -90)
        if number == 1:
            x -= 47.5 + token.get_rect().width / 2
            y += 22 - token.get_rect().height / 2
        elif number == 2:
            x -= 47.5 + token.get_rect().width / 2
            y += 63 - token.get_rect().height / 2
        elif number == 3:
            x -= 74.5 + token.get_rect().width / 2
            y += 22 - token.get_rect().height / 2
        elif number == 4:
            x -= 74.5 + token.get_rect().width / 2
            y += 63 - token.get_rect().height / 2
        elif number == 5:
            x -= 101.5 + token.get_rect().width / 2
            y += 22 - token.get_rect().height / 2
        elif number == 6:
            x -= 101.5 + token.get_rect().width / 2
            y += 63 - token.get_rect().height / 2
    # TOP ROW
    elif tile_pos < 31:
        token = pygame.transform.rotate(token, 180)
        if number == 1:
            x -= 22 + token.get_rect().width / 2
            y -= 47.5 + token.get_rect().height / 2
        elif number == 2:
            x -= 63 + token.get_rect().width / 2
            y -= 47.5 + token.get_rect().height / 2
        elif number == 3:
            x -= 22 + token.get_rect().width / 2
            y -= 74.5 + token.get_rect().height / 2
        elif number == 4:
            x -= 63 + token.get_rect().width / 2
            y -= 74.5 + token.get_rect().height / 2
        elif number == 5:
            x -= 22 + token.get_rect().width / 2
            y -= 101.5 + token.get_rect().height / 2
        elif number == 6:
            x -= 63 + token.get_rect().width / 2
            y -= 101.5 + token.get_rect().height / 2
    # RIGHT ROW
    elif tile_pos < 41:
        token = pygame.transform.rotate(token, 90)
        if number == 1:
            x += 47.5 - token.get_rect().width / 2
            y -= 22 + token.get_rect().height / 2
        elif number == 2:
            x += 47.5 - token.get_rect().width / 2
            y -= 63 + token.get_rect().height / 2
        elif number == 3:
            x += 74.5 - token.get_rect().width / 2
            y -= 22 + token.get_rect().height / 2
        elif number == 4:
            x += 74.5 - token.get_rect().width / 2
            y -= 63 + token.get_rect().height / 2
        elif number == 5:
            x += 101.5 - token.get_rect().width / 2
            y -= 22 - token.get_rect().height / 2
        elif number == 6:
            x += 101.5 - token.get_rect().width / 2
            y -= 63 + token.get_rect().height / 2
    # blit the token onto the screen at the correct coordinates
    screen.blit(token, (x, y))
    # update display
    pygame.display.update()


class ScreenTracker:

    def __init__(self):
        self.start_menu1 = True
        self.start_menu2 = False
        self.start_menu3 = False
        self.start_menu4 = False
        self.getting_names = False
        self.choosing_token = False
        self.playing_game = False
        self.normal_mode = True
        self.no_of_players = 0
        self.no_of_ai = 0
        self.players_setup = 0
        self.name_chosen = ""
        self.token_chosen = None
        self.tokens = [smartphone, cat, iron, hatstand, ship, boot]
        self.names_and_tokens = []
        self.tiles = tiles
        self.game = None
        self.pot_luck = None
        self.opp_knocks = None
        self.timer = None
        self.getting_timer = None
        self.time_limit = None
        self.net_worth = False

    def start_screen1(self):
        while self.start_menu1:
            pygame.display.set_mode(start_screen_size)
            screen.fill((30, 145, 150))
            screen.blit(logo, (150, -50))
            screen.blit(play_original, (150, 400))
            screen.blit(play_abridged, (450, 400))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start_menu1 = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 150 <= mouse_pos[0] <= 350 and 400 <= mouse_pos[1] <= 600:
                        self.normal_mode = True
                        self.start_menu1 = False
                        self.start_menu2 = True
                        self.start_screen2()

                    if 450 <= mouse_pos[0] <= 650 and 400 <= mouse_pos[1] <= 600:
                        self.normal_mode = False
                        self.start_menu1 = False
                        self.start_menu2 = True
                        self.start_screen2()

    def start_screen2(self):
        while self.start_menu2:
            pygame.display.set_mode(start_screen_size)
            screen.blit(no_of_human_players, (90, 50))
            screen.blit(back, (0, 700))
            screen.blit(one_player, (90, 250))
            screen.blit(two_player, (220, 250))
            screen.blit(three_player, (350, 250))
            screen.blit(four_player, (480, 250))
            screen.blit(five_player, (610, 250))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start_menu2 = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 0 <= mouse_pos[0] <= 200 and 700 <= mouse_pos[1] <= 800:
                        self.start_menu2 = False
                        self.start_menu1 = True
                        self.start_screen1()

                    if 90 <= mouse_pos[0] <= 190 and 250 <= mouse_pos[1] <= 350:
                        self.no_of_players = 1
                        self.start_menu2 = False
                        self.start_menu3 = True
                        self.start_screen3()

                    if 220 <= mouse_pos[0] <= 320 and 250 <= mouse_pos[1] <= 350:
                        self.no_of_players = 2
                        self.start_menu2 = False
                        self.start_menu3 = True
                        self.start_screen3()

                    if 350 <= mouse_pos[0] <= 450 and 250 <= mouse_pos[1] <= 350:
                        self.no_of_players = 3
                        self.start_menu2 = False
                        self.start_menu3 = True
                        self.start_screen3()

                    if 480 <= mouse_pos[0] <= 580 and 250 <= mouse_pos[1] <= 350:
                        self.no_of_players = 4
                        self.start_menu2 = False
                        self.start_menu3 = True
                        self.start_screen3()

                    if 610 <= mouse_pos[0] <= 710 and 250 <= mouse_pos[1] <= 350:
                        self.no_of_players = 5
                        self.start_menu2 = False
                        self.start_menu3 = True
                        self.start_screen3()

    def start_screen3(self):
        while self.start_menu3:
            pygame.display.set_mode(start_screen_size)
            screen.blit(no_of_human_players, (90, 20))
            screen.blit(no_of_ai_players, (90, 340))
            screen.blit(back, (0, 700))
            if self.no_of_players == 1:
                screen.blit(one_player, (350, 220))
                screen.blit(one_player, (90, 540))
                screen.blit(two_player, (220, 540))
                screen.blit(three_player, (350, 540))
                screen.blit(four_player, (480, 540))
                screen.blit(five_player, (610, 540))

            if self.no_of_players == 2:
                screen.blit(two_player, (350, 220))
                screen.blit(one_player, (155, 540))
                screen.blit(two_player, (285, 540))
                screen.blit(three_player, (415, 540))
                screen.blit(four_player, (545, 540))

            if self.no_of_players == 3:
                screen.blit(three_player, (350, 220))
                screen.blit(one_player, (220, 540))
                screen.blit(two_player, (350, 540))
                screen.blit(three_player, (480, 540))

            if self.no_of_players == 4:
                screen.blit(four_player, (350, 220))
                screen.blit(one_player, (285, 540))
                screen.blit(two_player, (415, 540))

            if self.no_of_players == 5:
                screen.blit(five_player, (350, 220))
                screen.blit(one_player, (350, 540))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start_menu3 = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if 0 <= mouse_pos[0] <= 200 and 700 <= mouse_pos[1] <= 800:
                        self.start_menu2 = True
                        self.start_menu3 = False
                        self.start_screen2()

                    if self.no_of_players == 1 or self.no_of_players == 3 or self.no_of_players == 5:

                        if 90 <= mouse_pos[0] <= 190 and 540 <= mouse_pos[1] <= 640:
                            if self.no_of_players == 1:
                                self.no_of_ai = 1
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                        if 220 <= mouse_pos[0] <= 320 and 540 <= mouse_pos[1] <= 640:
                            if self.no_of_players == 1:
                                self.no_of_ai = 2
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                            if self.no_of_players == 3:
                                self.no_of_ai = 1
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                        if 350 <= mouse_pos[0] <= 450 and 540 <= mouse_pos[1] <= 640:
                            if self.no_of_players == 1:
                                self.no_of_ai = 3
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                            if self.no_of_players == 3:
                                self.no_of_ai = 2
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                            if self.no_of_players == 5:
                                self.no_of_ai = 1
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                        if 480 <= mouse_pos[0] <= 580 and 540 <= mouse_pos[1] <= 640:
                            if self.no_of_players == 1:
                                self.no_of_ai = 4
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                            if self.no_of_players == 3:
                                self.no_of_ai = 3
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                        if 610 <= mouse_pos[0] <= 710 and 540 <= mouse_pos[1] <= 640:
                            if self.no_of_players == 1:
                                self.no_of_ai = 5
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                    if self.no_of_players == 2 or self.no_of_players == 4:

                        if 155 <= mouse_pos[0] <= 255 and 540 <= mouse_pos[1] <= 640:
                            if self.no_of_players == 2:
                                self.no_of_ai = 1
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                        if 285 <= mouse_pos[0] <= 385 and 540 <= mouse_pos[1] <= 640:
                            if self.no_of_players == 2:
                                self.no_of_ai = 2
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                            if self.no_of_players == 4:
                                self.no_of_ai = 1
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                        if 415 <= mouse_pos[0] <= 515 and 540 <= mouse_pos[1] <= 640:
                            if self.no_of_players == 2:
                                self.no_of_ai = 3
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                            if self.no_of_players == 4:
                                self.no_of_ai = 2
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

                        if 545 <= mouse_pos[0] <= 656 and 540 <= mouse_pos[1] <= 640:
                            if self.no_of_players == 2:
                                self.no_of_ai = 4
                                self.start_menu4 = True
                                self.start_menu3 = False
                                self.start_screen4()

    def start_screen4(self):
        while self.start_menu4:
            pygame.display.set_mode(start_screen_size)
            screen.blit(game_mode, (250, 20))
            screen.blit(human_players, (75, 400))
            screen.blit(ai_players, (425, 400))
            screen.blit(start_game, (600, 700))
            screen.blit(back, (0, 700))

            if self.normal_mode:
                screen.blit(play_original, (300, 120))
            elif not self.normal_mode:
                screen.blit(play_abridged, (300, 120))

            if self.no_of_players == 1:
                screen.blit(one_player, (175, 530))
            if self.no_of_players == 2:
                screen.blit(two_player, (175, 530))
            if self.no_of_players == 3:
                screen.blit(three_player, (175, 530))
            if self.no_of_players == 4:
                screen.blit(four_player, (175, 530))
            if self.no_of_players == 5:
                screen.blit(five_player, (175, 530))

            if self.no_of_ai == 1:
                screen.blit(one_player, (525, 530))
            if self.no_of_ai == 2:
                screen.blit(two_player, (525, 530))
            if self.no_of_ai == 3:
                screen.blit(three_player, (525, 530))
            if self.no_of_ai == 4:
                screen.blit(four_player, (525, 530))
            if self.no_of_ai == 5:
                screen.blit(five_player, (525, 530))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start_menu4 = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 0 <= mouse_pos[0] <= 200 and 700 <= mouse_pos[1] <= 800:
                        self.start_menu3 = True
                        self.start_menu4 = False
                        self.start_screen3()

                    if 600 <= mouse_pos[0] <= 800 and 700 <= mouse_pos[1] <= 800:
                        self.getting_names = True
                        self.start_menu4 = False
                        self.input_names()

    def input_names(self):
        input_active = False
        self.name_chosen = ""
        font = pygame.font.SysFont('timesnewroman', 40)
        pygame.display.set_mode(start_screen_size)
        screen.blit(name, (50, 50))
        screen.blit(next_button, (600, 700))
        pygame.display.update()
        while self.getting_names:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.getting_names = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    input_active = True
                    if 600 <= mouse_pos[0] <= 800 and 700 <= mouse_pos[1] <= 800 and len(self.name_chosen) > 0:
                        self.choosing_token = True
                        self.getting_names = False
                        self.choose_token()

                if event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.name_chosen = self.name_chosen[:-1]
                    elif event.key == pygame.K_RETURN and len(self.name_chosen) > 0:
                        input_active = False
                    elif len(self.name_chosen) < 13:
                        self.name_chosen += event.unicode

                pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(126, 130, 525, 50))
                show_name = font.render(self.name_chosen, True, (255, 255, 255))
                screen.blit(show_name, (150, 132))
                pygame.display.update()

    def choose_token(self):
        """

        :return:
        """
        self.token_chosen = None
        pygame.display.set_mode(start_screen_size)
        screen.fill((0, 200, 210))
        screen.blit(name, (50, 50))
        screen.blit(back, (0, 700))
        screen.blit(next_button, (600, 700))
        font = pygame.font.SysFont('timesnewroman', 40)
        show_name = font.render(self.name_chosen, True, (255, 255, 255))
        screen.blit(show_name, (150, 132))
        if smartphone in self.tokens:
            screen.blit(smartphone, (100, 250))
        if cat in self.tokens:
            screen.blit(cat, (350, 275))
        if ship in self.tokens:
            screen.blit(ship, (600, 250))
        if iron in self.tokens:
            screen.blit(iron, (100, 520))
        if hatstand in self.tokens:
            screen.blit(hatstand, (395, 500))
        if boot in self.tokens:
            screen.blit(boot, (600, 500))
        pygame.display.update()
        while self.choosing_token:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.choosing_token = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 0 <= mouse_pos[0] <= 200 and 700 <= mouse_pos[1] <= 800:
                        self.getting_names = True
                        self.choosing_token = False
                        self.input_names()

                    if self.token_chosen is not None and 600 <= mouse_pos[0] <= 800 and 700 <= mouse_pos[1] <= 800:
                        self.names_and_tokens.append((self.name_chosen, self.token_chosen))
                        self.tokens.remove(self.token_chosen)
                        self.players_setup = self.players_setup + 1
                        if self.players_setup == self.no_of_players:
                            self.playing_game = True
                            self.choosing_token = False
                            if not self.normal_mode:
                                self.getting_timer = True
                                self.get_timer()
                            self.game_screen()
                        else:
                            self.getting_names = True
                            self.choosing_token = False
                            self.input_names()

                    if smartphone in self.tokens and 100 <= mouse_pos[0] <= 200 and 250 <= mouse_pos[1] <= 450:
                        self.token_chosen = smartphone
                        pygame.draw.circle(screen, (0, 200, 210), (425, 331), 90, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (650, 338), 103, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (150, 563), 70, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (425, 600), 115, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (650, 544), 70, 3)

                        pygame.draw.circle(screen, (255, 0, 0), (150, 350), 115, 3)

                    if cat in self.tokens and 350 <= mouse_pos[0] <= 500 and 275 <= mouse_pos[1] <= 387:
                        self.token_chosen = cat
                        pygame.draw.circle(screen, (0, 200, 210), (650, 338), 103, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (150, 563), 70, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (425, 600), 115, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (650, 544), 70, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (150, 350), 115, 3)

                        pygame.draw.circle(screen, (255, 0, 0), (425, 331), 90, 3)

                    if ship in self.tokens and 600 <= mouse_pos[0] <= 700 and 250 <= mouse_pos[1] <= 426:
                        self.token_chosen = ship
                        pygame.draw.circle(screen, (0, 200, 210), (150, 563), 70, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (425, 600), 115, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (650, 544), 70, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (150, 350), 115, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (425, 331), 90, 3)

                        pygame.draw.circle(screen, (255, 0, 0), (650, 338), 103, 3)

                    if iron in self.tokens and 100 <= mouse_pos[0] <= 200 and 520 <= mouse_pos[1] <= 602:
                        self.token_chosen = iron
                        pygame.draw.circle(screen, (0, 200, 210), (425, 600), 115, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (650, 544), 70, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (150, 350), 115, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (425, 331), 90, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (650, 338), 103, 3)

                        pygame.draw.circle(screen, (255, 0, 0), (150, 563), 70, 3)

                    if hatstand in self.tokens and 395 <= mouse_pos[0] <= 455 and 500 <= mouse_pos[1] <= 700:
                        self.token_chosen = hatstand
                        pygame.draw.circle(screen, (0, 200, 210), (150, 563), 70, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (650, 544), 70, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (150, 350), 115, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (425, 331), 90, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (650, 338), 103, 3)

                        pygame.draw.circle(screen, (255, 0, 0), (425, 600), 115, 3)

                    if boot in self.tokens and 600 <= mouse_pos[0] <= 700 and 500 <= mouse_pos[1] <= 588:
                        self.token_chosen = boot
                        pygame.draw.circle(screen, (0, 200, 210), (150, 350), 115, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (425, 331), 90, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (425, 600), 115, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (150, 563), 70, 3)
                        pygame.draw.circle(screen, (0, 200, 210), (650, 338), 103, 3)

                        pygame.draw.circle(screen, (255, 0, 0), (650, 544), 70, 3)

                    pygame.display.update()

    def get_timer(self):
        """
        Function to create the start screen which will receive the timer if the game is the abridged version
        :return:
        """
        input_active = False
        self.timer = ""
        font1 = pygame.font.SysFont('algerian', 40)
        font = pygame.font.SysFont('timesnewroman', 40)
        timer_txt = font1.render("Insert timer in minutes:", True, WHITE)
        pygame.display.set_mode(start_screen_size)
        screen.blit(timer_txt, (50, 50))
        screen.blit(next_button, (600, 700))
        pygame.display.update()
        while self.getting_timer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.getting_timer = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    input_active = True
                    if 600 <= mouse_pos[0] <= 800 and 700 <= mouse_pos[1] <= 800 and len(self.timer) > 0:
                        self.getting_timer = False
                        self.time_limit = int(self.timer)*60
                        self.game_screen()

                if event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.timer = self.timer[:-1]
                    elif event.key == pygame.K_RETURN and len(self.timer) > 0:
                        input_active = False
                    elif len(self.timer) < 13:
                        self.timer += event.unicode

                pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(126, 130, 525, 50))
                show_timer = font.render(self.timer, True, (255, 255, 255))
                screen.blit(show_timer, (150, 132))
                pygame.display.update()

    def toggle_net_worth(self, game):
        """
        Function for the button which displays all player's net worth on the board
        :param game: the game object
        :return:
        """
        self.net_worth = True
        pygame.draw.rect(screen, WHITE, pygame.Rect(586.25, 136.25, 702.25, 475))
        pygame.display.update()
        font1 = pygame.font.SysFont('franklingothicmediumcond', 30)
        header = font1.render("Player net worth:", True, BLACK)
        header_rect = header.get_rect()
        header_rect.centerx = 937.5
        header_rect.y = 156.25
        x = 606.25
        y = header_rect.bottom + 30
        for i in range(game.players.get_length()):
            player = game.players.get(i)
            # blit the player name
            name = font1.render(player.name, True, BLACK)
            name_rect = name.get_rect()
            name_rect.x = x
            name_rect.y = y
            screen.blit(name, name_rect)
            # blit player net worth
            money = font1.render("Net worth: £" + str(player.net_worth), True, BLACK)
            money_rect = money.get_rect()
            money_rect.x = 937.5
            money_rect.y = y
            screen.blit(money, money_rect)
            y = name_rect.bottom + 15
        # blit the confirm toggle button
        toggle_button = pygame.Rect(887.5, 581.25, 100, 20)
        pygame.draw.rect(screen, BLACK, toggle_button)
        toggle_txt = font.render("Confrim", True, WHITE)
        toggle_rect = toggle_txt.get_rect()
        toggle_rect.center = toggle_button.center
        screen.blit(toggle_txt, toggle_rect)
        pygame.display.update()

    def game_screen(self):
        """
        Function to create the game object (from information inputted in start screens) and display initial game screen
        :return:
        """
        # while self.playing_game:
        pygame.display.set_mode(game_size)
        screen.blit(board, (450, 0))
        screen.blit(board_right, (1425, 0))
        get_text(self.tiles)
        # get the inputted names and chosen tokens for each player
        player_list = self.names_and_tokens
        # create a list for the players
        players = []
        # assign the player objects in the game object the correct names and tokens
        for i in range(0, len(player_list)):
            # create a player with name from the player_list
            player = Player(name=player_list[i][0], propList=[])
            # get the token chosen to convert it to a size that fits the board
            pl_token = player_list[i][1]
            if pl_token == smartphone:
                pl_token = smartphone_token
            elif pl_token == cat:
                pl_token = cat_token
            elif pl_token == boot:
                pl_token = boot_token
            elif pl_token == iron:
                pl_token = iron_token
            elif pl_token == ship:
                pl_token = ship_token
            else:
                pl_token = hatstand_token
            # assign the resized token to the player
            player.token = pl_token
            # assign players number
            player.number = i + 1
            # append player to the player list
            players.append(player)
        # create AI players
        for i in range(0, self.no_of_ai):
            token = self.tokens.pop(0)
            if token == smartphone:
                token = smartphone_token
            elif token == cat:
                token = cat_token
            elif token == boot:
                token = boot_token
            elif token == iron:
                token = iron_token
            elif token == ship:
                token = ship_token
            else:
                token = hatstand_token
            ai = AIPlayer(token=token, propList=[])
            ai.number = i + 1 + self.no_of_players
            players.append(ai)
        # create game object using the player list
        game = Game(players)
        self.game = game
        # get the cards
        self.pot_luck = game.pot_cards
        self.opp_knocks = game.opp_cards
        # set tiles
        self.tiles = game.tiles
        # blit the board, text, and free parking
        font3 = pygame.font.SysFont('franklingothicmediumcond', 40)
        fp_txt = font3.render("£{}".format(self.game.free_parking_money), True, BLACK)
        fp_rect = fp_txt.get_rect()
        fp_rect.centerx = 937.5
        fp_rect.centery = 487.5
        screen.blit(fp_txt, fp_rect)
        blit_bank_prop()
        pygame.display.update()
        # blit the players tokens
        for player in players:
            token_blit(player.number, player.pos, player.token)
            blit_player_indicators(player.number, player)
            print(player.name + ", " + str(player.number))
        current_player = game.players.get(0)
        screen.blit(hat, (450 - 10 - 40, 30 + ((current_player.number - 1) * 155)))
        pygame.display.update()
        start_time = time.time()
        self.game_loop(game, start_time)

    def game_loop(self, game, start_time):
        """
        Function for the game loop. Handles starting and ending a players turn, and if it is the abridged version,
        ending the game once the timer is over.
        :param game: the current game's game object
        :param start_time: the time the game was started
        :return:
        """
        dice_rolled = False
        turn_ended = True
        last_turns = False
        checked = False
        ctr = None
        player1 = self.game.players.get(0)
        while self.playing_game:
            if self.game.players.get_length() == 1:
                self.game.end_game()
            if not self.normal_mode:
                if ctr == self.game.players.get_length():
                    self.game.end_game()
                    self.playing_game = False
                elapsed_time = time.time() - start_time
                if elapsed_time > self.time_limit and not checked and game.players.get(0) == player1:
                    # create base to display text on
                    base = pygame.Rect((450 + tile_height + 150), (tile_height + 50), 675 - 2 * tile_height, 40)
                    pygame.draw.rect(screen, WHITE, base)
                    font2 = pygame.font.SysFont('franklingothicmediumcond', 20)
                    # create line 2
                    line1 = font2.render("The game is almost over! Take your last turns!", True, BLACK)
                    line1_rect = line1.get_rect()
                    line1_rect.centerx = 937.5
                    line1_rect.y = tile_height + 60
                    screen.blit(line1, line1_rect)
                    ctr = 1
                    last_turns = True
                    checked = True
            pygame.display.update()
            # if turn_ended:
            #     if isinstance(game.players.get(0), AIPlayer):
            #         pygame.time.wait(2000)
            #         self.game.next_step()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing_game = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if 25 <= mouse_pos[0] <= 125 and 955.5 <= mouse_pos[1] <= 972:
                        self.game.end_game()
                    if 325 <= mouse_pos[0] <= 425 and 955.5 <= mouse_pos[1] <= 972 and not self.net_worth:
                        self.toggle_net_worth(game)
                    if 887.5 <= mouse_pos[0] <= 987.5 and 581.25 <= mouse_pos[1] <= 601.25 and self.net_worth:
                        self.net_worth = False
                        screen.blit(board, (450, 0))
                        get_text(self.game.tiles)
                        for i in range(game.players.get_length()):
                            player = game.players.get(i)
                            token_blit(player.number, player.pos, player.token)
                        font3 = pygame.font.SysFont('franklingothicmediumcond', 40)
                        fp_txt = font3.render("£{}".format(self.game.free_parking_money), True, BLACK)
                        fp_rect = fp_txt.get_rect()
                        fp_rect.centerx = 937.5
                        fp_rect.centery = 487.5
                        screen.blit(fp_txt, fp_rect)
                    if 1460 <= mouse_pos[0] <= 1545 and 910 <= mouse_pos[1] <= 965 and turn_ended:
                        dice_rolled = True
                        turn_ended = False
                        self.game.next_step()
                    if 1555 <= mouse_pos[0] <= 1640 and 910 <= mouse_pos[1] <= 965 and dice_rolled:
                        if last_turns:
                            ctr += 1
                        dice_rolled = False
                        turn_ended = True
                        screen.blit(board, (450, 0))
                        get_text(self.game.tiles)
                        font3 = pygame.font.SysFont('franklingothicmediumcond', 40)
                        fp_txt = font3.render("£{}".format(self.game.free_parking_money), True, BLACK)
                        fp_rect = fp_txt.get_rect()
                        fp_rect.centerx = 937.5
                        fp_rect.centery = 487.5
                        screen.blit(fp_txt, fp_rect)
                        for i in range(game.players.get_length()):
                            player = game.players.get(i)
                            token_blit(player.number, player.pos, player.token)
                            blit_player_indicators(player.number, player)
                        screen.blit(hat, (450 - 10 - 40, 30 + ((game.players.get(0).number - 1) * 155)))
                        pygame.display.update()


screen_tracker = ScreenTracker()
screen_tracker.start_screen1()

pygame.quit()
