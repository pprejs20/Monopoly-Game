import random
import pygame

from player import AIPlayer
from tile import Tile

pygame.init()

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

logo = pygame.image.load("Images/Logo.png")

smartphone = pygame.image.load("Images/smartphone.png")
cat = pygame.image.load("Images/cat.png")
boot = pygame.image.load("Images/boot.png")
iron = pygame.image.load("Images/iron.png")
ship = pygame.image.load("Images/ship.png")
hatstand = pygame.image.load("Images/hatstand.png")

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
# jail messages
msgs = ["You were caught trying to trade properties!", "You're the prime suspect in an embezzlement case!",
        "Another player accuses you of theft!", "You've been avoiding your taxes!",
        "You tried to take the free-parking money!", "You tried to take your £200 before passing GO!"]
# create font to be used for board
font = pygame.font.SysFont('franklingothicmediumcond', 15)
# font for tiles landed on
font2 = pygame.font.SysFont('franklingothicmediumcond', 20)
# colours
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
def get_text(tile_set):
    """
    Function to display the text corresponding to each tile on the board
    :return:
    """
    # get tile coordinates
    tiles_coord = get_coordinates()
    # write the text for each tile
    for t in tile_set:
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
                if t.no_of_houses > 0:
                    count = str(t.no_of_houses)
                    if t.no_of_houses == 5:
                        txt = "Hotel"
                    else:
                        txt = "Houses: {}".format(count)
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
                if t.no_of_houses > 0:
                    count = str(t.no_of_houses)
                    if t.no_of_houses == 5:
                        txt = "Hotel"
                    else:
                        txt = "Houses: {}".format(count)
                    houses_img = font.render(txt, True, BLACK)
                    houses_rect = houses_img.get_rect()
                    houses_rect.centerx = (tiles_coord[curr_pos - 1][0] + (tile_width / 2))
                    houses_rect.y = tiles_coord[curr_pos - 1][1] + 2
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
                if t.no_of_houses > 0:
                    count = str(t.no_of_houses)
                    if t.no_of_houses == 5:
                        txt = "Hotel"
                    else:
                        txt = "Houses: {}".format(count)
                    houses_img = font.render(txt, True, BLACK)
                    houses_rect = houses_img.get_rect()
                    houses_rect.centerx = (tiles_coord[curr_pos - 1][0] + (tile_width / 2))
                    houses_rect.y = tiles_coord[curr_pos - 1][1] + 2
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
                if t.no_of_houses > 0:
                    count = str(t.no_of_houses)
                    if t.no_of_houses == 5:
                        txt = "Hotel"
                    else:
                        txt = "Houses: {}".format(count)
                    houses_img = font.render(txt, True, BLACK)
                    houses_rect = houses_img.get_rect()
                    houses_rect.centerx = (tiles_coord[curr_pos - 1][0] + (tile_width / 2))
                    houses_rect.y = tiles_coord[curr_pos - 1][1] + 2
                    screen.blit(houses_img, houses_rect)


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


# class containing integration functions to be called from the back end
class Intermediary:
    """
    Class which functions are called from the game class to update the GUI
    """

    # initialise with an instance of the game class
    def __init__(self, game):
        self.game = game
        self.choice = ""

    def reblit_left(self):
        """
        Function to reblit the player information on the left side of screen
        :return:
        """
        # create base to cover current player templates (in case someone is removed from the game)
        base = pygame.Rect(0, 0, 450, 975)
        pygame.draw.rect(screen, BLACK, base)
        # re-blit the player templates on left side
        for i in range(self.game.players.get_length()):
            player = self.game.players.get(i)
            blit_player_indicators(player.number, player)

    def reblit_board(self):
        """
        Function to re-blit the board image, the text, and the houses/hotels (if any)
        :return:
        """
        # re-blit the board and text
        screen.blit(board, (450, 0))
        get_text(self.game.tiles)
        # re-blit the player tokens
        for i in range(self.game.players.get_length()):
            player = self.game.players.get(i)
            token_blit(player.number, player.pos, player.token)
        # display free-parking money
        font3 = pygame.font.SysFont('franklingothicmediumcond', 40)
        fp_txt = font3.render("£{}".format(self.game.free_parking_money), True, BLACK)
        fp_rect = fp_txt.get_rect()
        fp_rect.centerx = 937.5
        fp_rect.centery = 487.5
        screen.blit(fp_txt, fp_rect)
        pygame.display.update()

    def reblit_right(self):
        """
        Function to re-blit the bank indicators on the right side of the screen
        :return:
        """
        # re-blit the bank property indicators on the right side
        blit_bank_prop()

    def reblit_all(self):
        """
        Function to re-blit each part of the screen
        :return:
        """
        self.reblit_left()
        self.reblit_board()
        self.reblit_right()

    def gjf_card(self, player, test=None):
        """
        Function to give player the option to use their Get out of Jail Free card, and get their decision
        :param player: Player who is in jail
        :param test: Variable to allow for passing a manual response (for testing)
        :return: Whether the player will use their Get out of Jail Free card
        """
        # create base to display text on
        base = pygame.Rect((450 + tile_height + 150), (tile_height + 100), 675 - 2 * tile_height, 675 - 2 * tile_height)
        pygame.draw.rect(screen, WHITE, base)
        # create line 1
        line1 = font2.render("{}, you're in jail!,".format(player.name), True, BLACK)
        line1_rect = line1.get_rect()
        line1_rect.centerx = 937.5
        line1_rect.y = tile_height + 120
        screen.blit(line1, line1_rect)
        # create line 2
        line2 = font2.render("Do you want to use your Get Out of Jail Free card?", True, BLACK)
        line2_rect = line2.get_rect()
        line2_rect.centerx = 937.5
        line2_rect.y = line1_rect.bottom + 30
        screen.blit(line2, line2_rect)
        # make yes button
        yes_button = pygame.Rect(base.x + 40, base.bottom - 90, 70, 50)
        pygame.draw.rect(screen, (40, 220, 50), yes_button)
        yes = font2.render("Yes", True, BLACK)
        yes_rect = yes.get_rect()
        yes_rect.center = yes_button.center
        screen.blit(yes, yes_rect)
        # make no button
        no_button = pygame.Rect(base.right - 110, base.bottom - 90, 70, 50)
        pygame.draw.rect(screen, (220, 50, 40), no_button)
        no = font2.render("No", True, BLACK)
        no_rect = no.get_rect()
        no_rect.center = no_button.center
        screen.blit(no, no_rect)
        pygame.display.update()
        # if player is AI, automatically generate response
        if isinstance(player, AIPlayer):
            pygame.time.wait(2000)
            response = random.choice(["y", "n"])
        # if player is human, get response through button clicks
        else:
            response = None
            use = True
            while use:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        use = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if yes_button.left <= mouse_pos[0] <= yes_button.right and yes_button.top <= mouse_pos[
                            1] <= yes_button.bottom:
                            use = False
                            response = "y"
                        elif no_button.left <= mouse_pos[0] <= no_button.right and no_button.top <= mouse_pos[
                            1] <= no_button.bottom:
                            use = False
                            response = "n"
        # return manually inputted response if there is one
        if test is not None:
            return test
        # otherwise, return player response
        return response

    def doubles_jail(self, player):
        """
        Function to blit a message when the player rolls three doubles in a row and is sent to jail
        :param player: Player who has rolled the doubles
        :return:
        """
        # create base to display text on
        base = pygame.Rect((450 + tile_height + 150), (tile_height + 100), 675 - 2 * tile_height, 675 - 2 * tile_height)
        pygame.draw.rect(screen, WHITE, base)
        # create line 1
        line1 = font2.render("{}, you're getting too lucky!,".format(player.name), True, BLACK)
        line1_rect = line1.get_rect()
        line1_rect.centerx = 937.5
        line1_rect.y = tile_height + 120
        screen.blit(line1, line1_rect)
        # create line 2
        line2 = font2.render("After rolling three doubles in a row you're sent to jail", True, BLACK)
        line2_rect = line2.get_rect()
        line2_rect.centerx = 937.5
        line2_rect.y = line1_rect.bottom + 60
        screen.blit(line2, line2_rect)
        pygame.display.update()
        # wait to give time to read message
        pygame.time.wait(2500)
        # move the player to jail
        self.reblit_board()

    def jailed_player(self, player, test=None):
        """
        Function for when a player is in jail at the beginning of their turn. Gives option to pay £50 to leave or to try
         and roll for a double
        :param player: Player who is in jail
        :param test: Variable to allow for passing a manual response (for testing)
        :return: Whether the player will pay to leave jail or not
        """
        # create base to display text on
        base = pygame.Rect((450 + tile_height + 150), (tile_height + 100), 675 - 2 * tile_height, 675 - 2 * tile_height)
        pygame.draw.rect(screen, WHITE, base)
        # create line 2
        line1 = font2.render("{}, you're in jail!,".format(player.name), True, BLACK)
        line1_rect = line1.get_rect()
        line1_rect.centerx = 937.5
        line1_rect.y = tile_height + 120
        screen.blit(line1, line1_rect)
        # create line 2
        line2 = font2.render("Do you want to pay £50 to leave jail?", True, BLACK)
        line2_rect = line2.get_rect()
        line2_rect.centerx = 937.5
        line2_rect.y = line1_rect.bottom + 30
        screen.blit(line2, line2_rect)
        # make yes button
        yes_button = pygame.Rect(base.x + 40, base.bottom - 90, 70, 50)
        pygame.draw.rect(screen, (40, 220, 50), yes_button)
        yes = font2.render("Yes", True, BLACK)
        yes_rect = yes.get_rect()
        yes_rect.center = yes_button.center
        screen.blit(yes, yes_rect)
        # make no button
        no_button = pygame.Rect(base.right - 110, base.bottom - 90, 70, 50)
        pygame.draw.rect(screen, (220, 50, 40), no_button)
        no = font2.render("No", True, BLACK)
        no_rect = no.get_rect()
        no_rect.center = no_button.center
        screen.blit(no, no_rect)
        pygame.display.update()
        # if player is AI, automatically generate response
        if isinstance(player, AIPlayer):
            pygame.time.wait(2000)
            response = random.choice(["y", "n"])
        # if player is humnan, get their response through button clicks
        else:
            response = None
            pay = True
            while pay:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pay = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if yes_button.left <= mouse_pos[0] <= yes_button.right and yes_button.top <= mouse_pos[
                            1] <= yes_button.bottom:
                            pay = False
                            response = "y"
                        elif no_button.left <= mouse_pos[0] <= no_button.right and no_button.top <= mouse_pos[
                            1] <= no_button.bottom:
                            pay = False
                            response = "n"
        # return manually inputted response if there is one
        if test is not None:
            return test
        # otherwise, return player decision
        return response

    def pay_to_leave(self, player):
        """
        Function for when the player pays to leave jail
        :param player: PLayer who is leaving jail
        :return:
        """
        # create a smaller base to display text on (covers previous text apart from header)
        base = pygame.Rect((450 + tile_height + 150), 290, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create line 2
        line2 = font2.render("You pay £50 to leave jail!", True, BLACK)
        line2_rect = line2.get_rect()
        line2_rect.centerx = 937.5
        line2_rect.y = 350
        screen.blit(line2, line2_rect)
        pygame.display.update()
        pygame.time.wait(1000)

    def roll_to_leave(self):
        """
        Function for when a player is trying to roll a double to leave jail
        :return:
        """
        # create a smaller base to display text on (covers previous text apart from header)
        base = pygame.Rect((450 + tile_height + 150), 290, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create line 2
        line2 = font2.render("Rolling for a double to leave jail!", True, BLACK)
        line2_rect = line2.get_rect()
        line2_rect.centerx = 937.5
        line2_rect.y = 350
        screen.blit(line2, line2_rect)
        pygame.display.update()

    def leave(self, player):
        """
        Function for when a player successfully rolls a double to leave jail
        :param player: Player who is leaving jail
        :return:
        """
        # create a smaller base to display text on (covers previous text apart from header)
        base = pygame.Rect((450 + tile_height + 150), 290, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create line 2
        line2 = font2.render("{}, you've rolled a double and are now free!".format(player.name), True, BLACK)
        line2_rect = line2.get_rect()
        line2_rect.centerx = 937.5
        line2_rect.y = 350
        screen.blit(line2, line2_rect)
        pygame.display.update()

    def failed_double(self, player):
        """
        Function for when a player fails to roll a double to get out of jail
        :param player: Player who was rolling dice
        :return:
        """
        # create a smaller base to display text on (covers previous text apart from header)
        base = pygame.Rect((450 + tile_height + 150), 290, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create line 2
        line2 = font2.render("{}, you didn't roll a double :(".format(player.name), True, BLACK)
        line2_rect = line2.get_rect()
        line2_rect.centerx = 937.5
        line2_rect.y = 350
        screen.blit(line2, line2_rect)
        # create line 3
        line3 = font2.render("Better luck next time!", True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = line2_rect.bottom + 20
        screen.blit(line3, line3_rect)
        pygame.display.update()

    def go(self):
        """
        Function for when a player lands on GO!
        :return:
        """
        # create a smaller base to display text on (covers previous text apart from where player landed)
        base = pygame.Rect((450 + tile_height + 150), 280, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # cretae line 3
        line3 = font2.render("Collect £200 as you pass GO!", True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = 350
        screen.blit(line3, line3_rect)
        # re-blit left side to show updated player money
        self.reblit_left()
        pygame.display.update()

    def roll_dice(self, roll1, roll2):
        """
        Function to roll the dice
        :param roll1: number rolled on dice 1
        :param roll2: number rolled on dice 2
        :return:
        """
        # randomly show different dice faces to simulate the rolling of dice
        for i in range(4):
            screen.blit(dice_images[random.choice([1, 2, 3, 4, 5, 6])], (858.75, (975 - tile_height - 70)))
            screen.blit(dice_images[random.choice([1, 2, 3, 4, 5, 6])], (966.25, (975 - tile_height - 70)))
            pygame.display.update()
            pygame.time.wait(300)
        # re-blit the board and text (to cover the old tokens)
        screen.blit(board, (450, 0))
        get_text(self.game.tiles)
        # display the actual numbers that were rolled
        screen.blit(dice_images[roll1], (858.75, (975 - tile_height - 70)))
        screen.blit(dice_images[roll2], (966.25, (975 - tile_height - 70)))
        # re-blit all the player tokens (having moved currently player forward)
        for i in range(self.game.players.get_length()):
            player = self.game.players.get(i)
            token_blit(player.number, player.pos, player.token)
        pygame.display.update()

    def roll_again(self, player):
        """
        Function for a player to roll the dice again after there turn if they rolled a double
        :param player: player who rolled a double
        :return:
        """
        # reblit the board to cover any previous base
        self.reblit_board()
        # create base to display text on
        base = pygame.Rect((450 + tile_height + 150), (tile_height + 110), 675 - 2 * tile_height, 300)
        pygame.draw.rect(screen, WHITE, base)
        # create line 2
        line1 = font2.render("{}, you've rolled a double!,".format(player.name), True, BLACK)
        line1_rect = line1.get_rect()
        line1_rect.centerx = 937.5
        line1_rect.y = tile_height + 120
        screen.blit(line1, line1_rect)
        # make roll again button
        roll_button = pygame.Rect(base.centerx - 50, base.bottom - 60, 100, 40)
        pygame.draw.rect(screen, (220, 215, 200), roll_button)
        roll_txt = font2.render("Roll again!", True, BLACK)
        roll_rect = roll_txt.get_rect()
        roll_rect.center = roll_button.center
        screen.blit(roll_txt, roll_rect)
        pygame.display.update()
        # if AI player automatically click button
        if isinstance(player, AIPlayer):
            pygame.time.wait(2000)
        # if human player get mouse click
        else:
            clicked = False
            while not clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        clicked = True
                        break

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos

                        # if player clicks roll again button exit loop
                        if roll_button.left <= pos[0] <= roll_button.right and roll_button.top <= pos[
                            1] <= roll_button.bottom:
                            clicked = True

    def buy_buildings(self, game, player, first_time, test=None):
        """
        Function to give a player the option to buy houses/hotels on properties they have a monopoly of
        :param game: game object which is in use
        :param player: player who is buying house/hotel
        :param first_time: whether it is the first time the player is given this choice (can only buy hotel on first
         time)
        :param test: Variable to allow for passing a manual response (for testing)
        :return:
        """
        # create base to display the text on (for buying buildings)
        base = pygame.Rect((450 + tile_height + 130), (tile_height + 100), 675 - 2 * tile_height + 40,
                           675 - 2 * tile_height)
        pygame.draw.rect(screen, WHITE, base)
        # line 1
        line1 = font2.render("{}, you can buy a house/hotel on:".format(player.name), True, BLACK)
        line1_rect = line1.get_rect()
        line1_rect.centerx = 937.5
        line1_rect.y = (tile_height + 150)
        screen.blit(line1, line1_rect)
        pygame.display.update()
        # create option 1: Pass
        pass_txt = font2.render("1. Pass", True, BLACK)
        pass_rect = pass_txt.get_rect()
        pass_rect.centerx = 937.5
        pass_rect.y = line1_rect.bottom + 20
        screen.blit(pass_txt, pass_rect)
        # get possible properties
        available_props = game.get_house_available_props(player, first_time)
        x = pass_rect.x
        y = pass_rect.bottom
        ctr = 2
        # display possible properties
        for prop in available_props:
            cost = house_costs[prop.group]
            # if the player cannot afford a house for that group do not display it
            if player.money < cost:
                break
            else:
                txt = font2.render("{}. {}, {}, Current Houses: {}, ${} per house".format(ctr, prop.space, prop.group,
                                                                                          prop.no_of_houses, cost),
                                   True, BLACK)
                ctr += 1
                txt_rect = txt.get_rect()
                txt_rect.centerx = 937.5
                txt_rect.y = y + 15
                y = txt_rect.bottom
                screen.blit(txt, txt_rect)
        # create input space
        input_rect = pygame.Rect(937.5 - 40, base.bottom - 40, 80, 30)
        pygame.draw.rect(screen, (220, 215, 200), input_rect)
        pygame.display.update()
        # if AI player, generate random response
        if isinstance(player, AIPlayer):
            pygame.time.wait(1500)
            options = []
            for i in range(1, len(available_props) + 1):
                options.append(str(i))
            self.choice = random.choice(options)
        # if human player, get the option they chose
        else:
            input_active = False
            self.choice = ""
            decision = False
            while not decision:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        decision = True
                        break

                    # if the player clicks on the input rectangle enable input
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if input_rect.left <= mouse_pos[0] <= input_rect.right and input_rect.top <= mouse_pos[
                            1] <= input_rect.bottom:
                            input_active = True

                    # if player presses backspace delete one
                    if event.type == pygame.KEYDOWN and input_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.choice = self.choice[:-1]
                        # if they press return and the input is valid exit
                        elif event.key == pygame.K_RETURN and int(self.choice) <= len(available_props) + 1:
                            input_active = False
                            decision = True
                            break
                        # receive input
                        elif len(self.choice) < 2 and event.unicode.isdigit():
                            self.choice += event.unicode

                    pygame.draw.rect(screen, (220, 215, 200), input_rect)
                    show_choice = font.render(self.choice, True, BLACK)
                    choice_rect = show_choice.get_rect()
                    choice_rect.center = input_rect.center
                    screen.blit(show_choice, choice_rect)
                    pygame.display.update()

        # return manually inputted value if there is one
        if test is not None:
            return test
        # otherwise, return the player's response
        return self.choice

    def sell_properties(self, player, test=None):
        # create base to display the text on (for buying buildings)
        base = pygame.Rect((450 + tile_height + 130), (tile_height + 100), 675 - 2 * tile_height + 40,
                           675 - 2 * tile_height)
        pygame.draw.rect(screen, WHITE, base)
        # line 1
        line1 = font2.render("{}, you can sell the following properties:".format(player.name), True, BLACK)
        line1_rect = line1.get_rect()
        line1_rect.centerx = 937.5
        line1_rect.y = (tile_height + 150)
        screen.blit(line1, line1_rect)
        pygame.display.update()
        # get possible properties
        y = line1_rect.bottom + 20
        ctr = 1
        # display possible properties
        for prop in player.propList:
            if prop.group in house_costs.keys():
                no = house_costs[prop.group]
                no_houses = prop.no_of_houses
                txt = font2.render("{}. {}, Houses: {}, Value: {}".format(ctr, prop.space, no_houses,
                                                                      prop.cost + (no * no_houses)), True, BLACK)
            else:
                txt = font2.render("{}. {}, Value: {}".format(ctr, prop.space, prop.cost), True, BLACK)
            ctr += 1
            txt_rect = txt.get_rect()
            txt_rect.centerx = 937.5
            txt_rect.y = y + 15
            y = txt_rect.bottom
            screen.blit(txt, txt_rect)
        # create input space
        input_rect = pygame.Rect(937.5 - 40, base.bottom - 40, 80, 30)
        pygame.draw.rect(screen, (220, 215, 200), input_rect)
        pygame.display.update()
        # if AI player, generate random response
        if isinstance(player, AIPlayer):
            pygame.time.wait(1500)
            options = []
            for i in range(1, len(player.propList) + 1):
                options.append(str(i))
            self.choice = random.choice(options)
        # if human player, get the option they chose
        else:
            input_active = False
            self.choice = ""
            decision = False
            while not decision:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        decision = True
                        break

                    # if the player clicks on the input rectangle enable input
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if input_rect.left <= mouse_pos[0] <= input_rect.right and input_rect.top <= mouse_pos[
                            1] <= input_rect.bottom:
                            input_active = True

                    # if player presses backspace delete one
                    if event.type == pygame.KEYDOWN and input_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.choice = self.choice[:-1]
                        # if they press return and the input is valid exit
                        elif event.key == pygame.K_RETURN and int(self.choice) <= len(player.propList) + 1:
                            input_active = False
                            decision = True
                        # receive input
                        elif len(self.choice) < 3 and event.unicode.isdigit():
                            self.choice += event.unicode

                    pygame.draw.rect(screen, (220, 215, 200), input_rect)
                    show_choice = font.render(self.choice, True, BLACK)
                    choice_rect = show_choice.get_rect()
                    choice_rect.center = input_rect.center
                    screen.blit(show_choice, choice_rect)
                    pygame.display.update()

        # return manually inputted value if there is one
        if test is not None:
            return test
        # otherwise, return the player's response
        return self.choice

    def check_player_location(self, player):
        """
        Function to blit the name of the tile a player has landed on. Creates the base on which the appropriate messages
         for that tile will be blitted
        :param player: player who landed on the tile
        :return:
        """
        # create a base to put the text for where the player landed
        current_tile = tiles[player.pos - 1]
        base = pygame.Rect((450 + tile_height + 150), (tile_height + 100), 675 - 2 * tile_height, 675 - 2 * tile_height)
        pygame.draw.rect(screen, WHITE, base)
        # create line 1
        line1 = font2.render(player.name + ", you have landed on:", True, BLACK)
        line1_rect = line1.get_rect()
        line1_rect.centerx = 937.5
        line1_rect.y = (tile_height + 100) + 20
        screen.blit(line1, line1_rect)
        # create line 2
        line2 = font2.render(str(current_tile.space), True, BLACK)
        line2_rect = line2.get_rect()
        line2_rect.y = line1_rect.bottom + 20
        line2_rect.centerx = 937.5
        screen.blit(line2, line2_rect)
        pygame.display.update()

    def go_jail(self, player):
        """
        Function for when a player lands on the Go to Jail tile
        :param player: player who is sent to jail
        :return:
        """
        # create smaller base to put text on (covers previous text apart from where they landed)
        base = pygame.Rect((450 + tile_height + 150), 300, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create line 3
        line3 = font2.render("Uh oh! {}".format(random.choice(msgs)), True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = 350
        screen.blit(line3, line3_rect)
        # create line 4
        line4 = font2.render("{} is escorted to jail.".format(player.name), True, BLACK)
        line4_rect = line4.get_rect()
        line4_rect.centerx = 937.5
        line4_rect.y = line3_rect.bottom + 30
        screen.blit(line4, line4_rect)
        pygame.display.update()

    def offer_prop(self, curr_player, test=None):
        """
        Function to give a player the opportunity to buy the property they have landed on. Generates automatic response
         for AI players
        :param curr_player: player who is buying a property
        :param test: Variable to allow for manually passing a response (for testing)
        :return:
        """
        # get the tile to be offered
        tile = tiles[curr_player.pos - 1]
        # create smaller base to put text on (covers previous text apart from where they landed)
        base = pygame.Rect((450 + tile_height + 150), 300, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        # if the tile is a station create following lines of text:
        if tile.pos in [6, 16, 26, 36]:
            line3_txt = "1 Station: £25            2 Stations: £50"
            line4_txt = "3 Stations: £100            4 Stations: £200"
            line5_txt = ""
        # if tile is a utility create following lines of text:
        elif tile.pos in [13, 29]:
            line3_txt = "1 Utility: rent is 4 times value shown on dice"
            line4_txt = "2 Utilities: rent is 10 times value shown on dice"
            line5_txt = ""
        # otherwise, tile will be a normal property
        else:
            line3_txt = "Base rent: £{}".format(tile.base_rent) + "            1 House: £{}".format(
                tile.one_house_rent)
            line4_txt = "2 House: £{}".format(tile.two_house_rent) + "            3 House: £{}".format(
                tile.three_house_rent)
            line5_txt = "4 House: £{}".format(tile.four_house_rent) + "            Hotel: £{}".format(
                tile.hotel_rent)
        # display line 3
        line3 = font2.render(line3_txt, True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = 350
        screen.blit(line3, line3_rect)
        # display line 4
        line4 = font2.render(line4_txt, True, BLACK)
        line4_rect = line4.get_rect()
        line4_rect.centerx = 937.5
        line4_rect.y = line3_rect.bottom + 15
        screen.blit(line4, line4_rect)
        # display line 5
        line5 = font2.render(line5_txt, True, BLACK)
        line5_rect = line5.get_rect()
        line5_rect.centerx = 937.5
        line5_rect.y = line4_rect.bottom + 15
        screen.blit(line5, line5_rect)
        # display line 6
        line6 = font2.render("Cost: £{}".format(tile.cost), True, BLACK)
        line6_rect = line6.get_rect()
        line6_rect.centerx = 937.5
        line6_rect.y = line5_rect.bottom + 20
        screen.blit(line6, line6_rect)
        # display line 7
        line7 = font2.render("{}, do you wish to buy?".format(curr_player.name), True, BLACK)
        line7_rect = line7.get_rect()
        line7_rect.centerx = 937.5
        line7_rect.y = line6_rect.bottom + 30
        screen.blit(line7, line7_rect)
        # make yes button
        yes_button = pygame.Rect(base.x + 20, base.bottom - 20 - 50, 70, 50)
        pygame.draw.rect(screen, (40, 220, 50), yes_button)
        yes = font2.render("Yes", True, BLACK)
        yes_rect = yes.get_rect()
        yes_rect.center = yes_button.center
        screen.blit(yes, yes_rect)
        # make no button
        no_button = pygame.Rect(base.right - 90, base.bottom - 20 - 50, 70, 50)
        pygame.draw.rect(screen, (220, 50, 40), no_button)
        no = font2.render("No", True, BLACK)
        no_rect = no.get_rect()
        no_rect.center = no_button.center
        screen.blit(no, no_rect)
        pygame.display.update()
        # if player is an AI, generate random response
        if isinstance(curr_player, AIPlayer):
            pygame.time.wait(2000)
            response = random.choice(["y", "n"])
        # if human player check to see where they clicked to get their response
        else:
            buying_prop = True
            response = None
            while buying_prop:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        buying_prop = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if yes_button.left <= mouse_pos[0] <= yes_button.right and yes_button.top <= mouse_pos[
                            1] <= yes_button.bottom:
                            buying_prop = False
                            response = "y"
                        elif no_button.left <= mouse_pos[0] <= no_button.right and no_button.top <= mouse_pos[
                            1] <= no_button.bottom:
                            buying_prop = False
                            response = "n"
        # return manually inputted variable if there is one
        if test is not None:
            return test
        # otherwise, return the response
        return response

    def buy_prop(self, curr_player, tile=None, ):
        """
        Function for when a player buys a property (either through them landing on it or auction)
        :param curr_player: player making the purchase
        :param tile: tile being purchased (necessary in case they are buying a property they are not currently on)
        :return:
        """
        # create smaller base to put text on (covers previous text apart from which property was bought)
        base = pygame.Rect((450 + tile_height + 150), 300, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # if they are not buying a specific tile, then retrieve the tile they are currently on
        if tile is None:
            tile = tiles[curr_player.pos - 1]
        # create line 3 text
        line3 = font2.render("{} has bought ".format(curr_player.name) + "{}!".format(tile.space), True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = 350
        screen.blit(line3, line3_rect)
        # set transparency of image at bank_prop_list[current_tile] to be 0 (disappear from rhs)
        bank_prop_list[tile.space].set_alpha(0)
        # reblit rhs
        self.reblit_right()
        # reblit lhs
        self.reblit_left()
        pygame.display.update()

    def auction_prop(self, tile):
        """
        Function for when a property is being auctioned. Creates the base where auction menu will be called for each
         player
        :param tile: tile being auctioned
        :return:
        """
        # create base for the property being auctioned
        base = pygame.Rect((450 + tile_height + 150), (tile_height + 100), 675 - 2 * tile_height, 675 - 2 * tile_height)
        pygame.draw.rect(screen, WHITE, base)
        # line 1: "Auction for: *Property name*"
        line1 = font2.render("Auction for: {}".format(tile.space), True, BLACK)
        line1_rect = line1.get_rect()
        line1_rect.centerx = 937.5
        line1_rect.y = (tile_height + 150)
        screen.blit(line1, line1_rect)
        pygame.display.update()

    def auction_menu(self, player, curr_price, test=None):
        """
        Function for when a player is bidding on a property. Gives option to pass or raise the current bid by set
         amounts and gets players decision
        :param player: player making a bid
        :param curr_price: current price of the property being auctioned
        :param test: Variable to allow for manually passing a response (for testing)
        :return:
        """
        # create smaller base to put text on (covers previous text apart from which property is being auctioned)
        base = pygame.Rect((450 + tile_height + 150), 300, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create third line of text: "Current bid: £x"
        line3 = font2.render("Current bid: £{}".format(str(curr_price)), True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = 330
        screen.blit(line3, line3_rect)
        # create fourth line of text: "*Player_name*, will you:"
        line4 = font2.render("{}, will you:".format(player.name), True, BLACK)
        line4_rect = line4.get_rect()
        line4_rect.centerx = 937.5
        line4_rect.y = line3_rect.bottom + 20
        screen.blit(line4, line4_rect)
        # create button 1: Pass
        pass_button = pygame.Rect(base.x + 50, base.bottom - 210, 100, 50)
        pygame.draw.rect(screen, (230, 200, 130), pass_button)
        pass_txt = font2.render("Pass", True, BLACK)
        pass_rect = pass_txt.get_rect()
        pass_rect.center = pass_button.center
        screen.blit(pass_txt, pass_rect)
        # create button 2: Raise £50
        fifty_button = pygame.Rect(base.right - 150, base.bottom - 210, 100, 50)
        pygame.draw.rect(screen, (230, 200, 130), fifty_button)
        fifty = font2.render("Raise £50", True, BLACK)
        fifty_rect = fifty.get_rect()
        fifty_rect.center = fifty_button.center
        screen.blit(fifty, fifty_rect)
        # create button 3: Raise £100
        hund_button = pygame.Rect(base.x + 50, base.bottom - 90, 100, 50)
        pygame.draw.rect(screen, (230, 200, 130), hund_button)
        hund = font2.render("Raise £100", True, BLACK)
        hund_rect = hund.get_rect()
        hund_rect.center = hund_button.center
        screen.blit(hund, hund_rect)
        # create button 4: Raise £500
        fhund_button = pygame.Rect(base.right - 150, base.bottom - 90, 100, 50)
        pygame.draw.rect(screen, (230, 200, 130), fhund_button)
        fhund_txt = font2.render("Raise £500", True, BLACK)
        fhund_txt_rect = fhund_txt.get_rect()
        fhund_txt_rect.center = fhund_button.center
        screen.blit(fhund_txt, fhund_txt_rect)
        pygame.display.update()
        # generate automatic response if it's an AI
        if isinstance(player, AIPlayer):
            pygame.time.wait(2000)
            if player.money >= curr_price + 500:
                response = random.choice(["1", "2", "3", "4"])
            elif player.money >= curr_price + 100:
                response = random.choice(["1", "2", "3"])
            elif player.money >= curr_price + 50:
                response = random.choice(["1", "2"])
            else:
                response = "1"
        else:
            response = None
            bidding = True
            while bidding:
                # get which button was clicked by the player
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        bidding = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if pass_button.left <= mouse_pos[0] <= pass_button.right and pass_button.top <= mouse_pos[
                            1] <= pass_button.bottom:
                            response = "1"
                            bidding = False
                        elif fifty_button.left <= mouse_pos[0] <= fifty_button.right and fifty_button.top <= mouse_pos[
                            1] <= fifty_button.bottom:
                            response = "2"
                            bidding = False
                        elif hund_button.left <= mouse_pos[0] <= hund_button.right and hund_button.top <= mouse_pos[
                            1] <= hund_button.bottom:
                            response = "3"
                            bidding = False
                        elif fhund_button.left <= mouse_pos[0] <= fhund_button.right and fhund_button.top <= mouse_pos[
                            1] <= fhund_button.bottom:
                            response = "4"
                            bidding = False
        # return the manually inputted value if there is one
        if test is not None:
            return test
        # otherwise, return the chosen value
        return response

    def noone_bought(self):
        """
        Function in case no-one buys the property that was being auctioned
        :return:
        """
        # create smaller base to put text on (covers previous text apart from which property was auctioned)
        base = pygame.Rect((450 + tile_height + 150), 300, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create line 3
        line3 = font2.render("No-one bought the property!", True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = 350
        screen.blit(line3, line3_rect)
        pygame.display.update()

    def return_prop(self, prop):
        """
        Function to make a property indicator reappear on the right side in case of mortgage
        :param prop: property being returned
        :return:
        """
        # set transparency of image at bank_prop_list[current_tile] to be 1 (disappear from rhs)
        bank_prop_list[prop.space].set_alpha(100)

    def owned_tile(self, player, tile):
        """
        Function for when a player lands on another player's property
        :param player: player who landed on the tile
        :param tile: tile that was landed on
        :return:
        """
        # create smaller base to put text on (covers previous text apart from where they landed)
        base = pygame.Rect((450 + tile_height + 150), 300, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create line 3
        line3 = font2.render("{} ".format(tile.space) + "is owned by {}".format(tile.owner), True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = 350
        screen.blit(line3, line3_rect)
        # create line 4
        line4 = font2.render("{}, time to pay rent!".format(player.name), True, BLACK)
        line4_rect = line4.get_rect()
        line4_rect.centerx = 937.5
        line4_rect.y = line3_rect.bottom + 30
        screen.blit(line4, line4_rect)
        pygame.display.update()

    def pay_rent(self, rent, payee, receiver):
        """
        Function to blit the message when a player pays another player rent
        :param rent: amount being paid
        :param payee: player making the payment
        :param receiver: player receiveing the payment
        :return:
        """
        # create text to display
        line5 = font2.render("{} ".format(payee.name) + "pays {} ".format(receiver.name) +
                             "£{} in rent!".format(str(rent)), True, BLACK)
        line5_rect = line5.get_rect()
        line5_rect.centerx = 937.5
        line5_rect.y = 500
        screen.blit(line5, line5_rect)
        pygame.display.update()

    def pot_luck(self, card):
        """
        Function for when a player lands on a Pot Luck tile. Displays the card description
        :param card: card that was drawn
        :return:
        """
        # get card description on the board
        c = pot_luck.get_rect()
        c.centerx = 937.5
        c.y = 375
        screen.blit(pot_luck, c)
        desc = card.get_description()
        desc = wrap_text(desc, 170)
        gap = 5
        for descs in desc:
            line3 = font2.render(descs, True, BLACK)
            line3_rect = line3.get_rect()
            line3_rect.centerx = 937.5
            line3_rect.y = 450 + gap
            gap += line3_rect.height
            screen.blit(line3, line3_rect)
            pygame.display.update()
        # wait 2.5 seconds to display the card
        pygame.time.wait(2500)

    def opp_knocks(self, card):
        """
        Function for when a player lands on an Opportunity Knocks tile. Displays the card description
        :param card: card that was drawn
        :return:
        """
        # get card description on the board
        c = opp_knocks.get_rect()
        c.centerx = 937.5
        c.y = 375
        screen.blit(opp_knocks, c)
        desc = card.get_description()
        desc = wrap_text(desc, 170)
        gap = 5
        for descs in desc:
            line3 = font2.render(descs, True, BLACK)
            line3_rect = line3.get_rect()
            line3_rect.centerx = 937.5
            line3_rect.y = 450 + gap
            gap += line3_rect.height
            screen.blit(line3, line3_rect)
            pygame.display.update()
        # wait 2.5 seconds to display the card
        pygame.time.wait(2500)

    def free_parking(self, player):
        """
        Function for when a player lands on the free-parking tile
        :param player: player who landed on free-parking
        :return:
        """
        # create smaller base to put text on (covers previous text apart from where they landed)
        base = pygame.Rect((450 + tile_height + 150), 300, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create line 3
        line3 = font2.render("Wooo! {} has hit the jackpot and gets richer!".format(player.name), True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = 350
        screen.blit(line3, line3_rect)
        # create line 4
        line4 = font2.render("Collect {} from free parking!".format(self.game.free_parking_money), True, BLACK)
        line4_rect = line4.get_rect()
        line4_rect.centerx = 937.5
        line4_rect.y = line3_rect.bottom + 20
        screen.blit(line4, line4_rect)
        # re-blit left side to show new player money
        self.reblit_left()
        pygame.display.update()
        pygame.time.wait(1000)

    def income_tax(self, player):
        """
        Function for when a player lands on the Income Tax tile
        :param player: player who landed on the tile
        :return:
        """
        # create smaller base to put text on (covers previous text apart from where they landed)
        base = pygame.Rect((450 + tile_height + 150), 300, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create line 3
        line3 = font2.render("{} must pay £200 to the bank".format(player.name), True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = 350
        screen.blit(line3, line3_rect)
        # re-blit the left side to show new player money
        self.reblit_left()
        pygame.display.update()

    def super_tax(self, player):
        """
        Function for when a player lands on the Super Tax tile
        :param player: player who landed on the tile
        :return:
        """
        # create smaller base to put text on (covers previous text apart from where they landed)
        base = pygame.Rect((450 + tile_height + 150), 300, 675 - (2 * tile_height), 675 - (2 * tile_height) - 83.75)
        pygame.draw.rect(screen, WHITE, base)
        # create line 3
        line3 = font2.render("{} must pay £100 to the bank".format(player.name), True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = 350
        screen.blit(line3, line3_rect)
        # re-blit the left side to show new player money
        self.reblit_left()
        pygame.display.update()

    def end_game(self, player):
        """
        Function for when the game is over (either because there is only one player left or time runs out)
        :param player: player who has won the game
        :return:
        """
        # create base to put text on
        base = pygame.Rect((450 + tile_height + 150), (tile_height + 100), 675 - 2 * tile_height, 675 - 2 * tile_height)
        pygame.draw.rect(screen, WHITE, base)
        # create line 1 
        line1 = font2.render("The game is over!", True, BLACK)
        line1_rect = line1.get_rect()
        line1_rect.centerx = 937.5
        line1_rect.y = tile_height + 120
        screen.blit(line1, line1_rect)
        # create line 2 
        line2 = font2.render("{} wins with a net worth of:".format(player.name), True, BLACK)
        line2_rect = line2.get_rect()
        line2_rect.centerx = 937.5
        line2_rect.y = 350
        screen.blit(line2, line2_rect)
        # create line 3
        line3 = font2.render("{}".format(player.net_worth), True, BLACK)
        line3_rect = line3.get_rect()
        line3_rect.centerx = 937.5
        line3_rect.y = line2_rect.bottom + 20
        screen.blit(line3, line3_rect)
        pygame.display.update()
        pygame.time.wait(5000)


house_costs = {
    "Brown": 50,
    "Blue": 50,
    "Purple": 100,
    "Orange": 100,
    "Red": 150,
    "Yellow": 150,
    "Green": 200,
    "Deep blue": 200
}
