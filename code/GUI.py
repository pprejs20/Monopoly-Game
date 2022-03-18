import pygame
from pygame.locals import *
import tile

# set up board lines
pygame.init()

screen_width = 1650
screen_height = 975

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Property Tycoon')

background = pygame.image.load("Images/Board2.png")

# get the tile data from excel
tiles = tile.Tile.load_tiles_from_xlsx("ExcelData/PropertyTycoonBoardData.xlsx")
# define board height and width
board_height = board_width = screen_height
# define tile width
tile_width = 82.5
# define tile height
tile_height = 116.25
# create font to be used
font = pygame.font.SysFont('franklingothicmediumcond', 15)
BLACK = (0, 0, 0)


# function to populate an array with the coordinates of each tile
def get_coordinates():
    # create list to store the coordinates of each tile
    coord_list = []
    # iterator to go through the 40 tiles
    i = 1

    # first get screen width without board because there is space on either side of board (2/3 on left and 1/3 on right)
    screen_width_excl_board = screen_width - board_width

    # x starts where board ends minus the height of a tile (because first tile, GO, is in bottom right)
    x = (screen_width - screen_width_excl_board * (1 / 3)) - tile_height
    # y is the screen height minus height of a tile (because there is no space below board)
    y = screen_height - tile_height
    for i in range(1, 11):
        # for first row (bottom) y stays the same and x decreases by width of a tile each iteration
        coord_list.append((x, y))
        x -= tile_width

    # x is where the board starts plus the height of a tile
    x = (screen_width_excl_board * (2 / 3)) + tile_height
    # y starts at screen height - height of a tile
    y = screen_height - tile_height
    for i in range(11, 21):
        # for second row (left) x stays the same and y decreases by width of a tile each iteration
        coord_list.append((x, y))
        y -= tile_width

    # x starts at the where the board starts plus height of a tile
    x = (screen_width_excl_board * (2 / 3)) + tile_height
    # y is the height of a tile (because there is no space above the board)
    y = tile_height
    for i in range(21, 31):
        # for third row (top) y stays the same and x increases by width of tile each iteration
        coord_list.append((x, y))
        x += tile_width

    # x is where the board ends minus the height of a tile
    x = (screen_width - screen_width_excl_board * (1 / 3)) - tile_height
    # y starts at the height of a tile
    y = tile_height
    for i in range(31, 41):
        coord_list.append((x, y))
        y += tile_width

    return coord_list


tiles_coord = get_coordinates()


# function to wrap text in tiles (if necessary)
def wrap_text(string):
    # create list to store rendered text images
    imgs = []
    # render image of string
    string_img = font.render(str(string), True, BLACK)
    # check width to see if it fits in tile (with gap of 7.5 px on either side)
    if string_img.get_rect().width > 64.5:
        # split given string into words
        words = string.split()

        # get ready to loop through all the words
        while len(words) > 0:
            # create list to store words in a line
            line = []
            # add word until they no longer fit the width
            while len(words) > 0:
                line.append(words.pop(0))
                width1, height1 = font.size(' '.join(line + words[:1]))
                if width1 > 64.5:
                    break

            # append the words that did fit in the line
            ln = ' '.join(line)
            imgs.append(ln)
    else:
        imgs.append(string)
    return imgs


# function to print text on board
def get_text():
    # write the text for each tile
    for t in tiles:
        # get current tile's position
        curr_pos = t.pos
        # skip non-customisable tiles (corners, pot lucks, opportunity knocks, and taxes)
        if curr_pos in [1, 3, 5, 8, 11, 18, 21, 23, 31, 34, 37, 39]:
            continue
        else:
            # get text for name and pass to wrap text function
            name = wrap_text(t.space)
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


setup = False
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not setup:
        screen.blit(background, (450, 0))
        get_text()
        setup = True

    pygame.display.update()
pygame.quit()
