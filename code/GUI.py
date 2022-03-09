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


# function to populate an array with the coordinates of each tile
def get_coordinates():

    # create list to store the coordinates of each tile
    tiles_coord = []
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
        tiles_coord.append((x, y))
        x -= tile_width

    # x is where the board starts plus the height of a tile
    x = (screen_width_excl_board * (2 / 3)) + tile_height
    # y starts at screen height - height of a tile
    y = screen_height - tile_height
    for i in range(11, 21):
        # for second row (left) x stays the same and y decreases by width of a tile each iteration
        tiles_coord.append((x, y))
        y -= tile_width

    # x starts at the where the board starts plus height of a tile
    x = (screen_width_excl_board * (2 / 3)) + tile_height
    # y is the height of a tile (because there is no space above the board)
    y = tile_height
    for i in range(21, 31):
        # for third row (top) y stays the same and x increases by width of tile each iteration
        tiles_coord.append((x, y))
        x += tile_width

    # x is where the board ends minus the height of a tile
    x = (screen_width - screen_width_excl_board * (1 / 3)) - tile_height
    # y starts at the height of a tile
    y = tile_height
    for i in range(31, 41):
        tiles_coord.append((x, y))
        y += tile_width

    return tiles_coord


# create font to be used
font = pygame.font.SysFont('franklingothicmediumcond', 4)
BLACK = (0, 0, 0)

# write the text for each tile
# for tile in tiles:
#     # get current tile's position
#     curr_pos = tile.pos
#     # skip non-customisable tiles (corners, pot lucks, opportunity knocks, and taxes)
#     if curr_pos in [1, 3, 5, 8, 11, 18, 21, 23, 31, 34, 37, 39]:
#         continue
#     else:
#         # create image for the name
#         name_img = font.render(tile.space, True, BLACK)
#         # create image for the price
#         price_img = font.render(tile.cost, True, BLACK)
#
#         # set a buffer for the coloured rectangle at the top of the property tiles (40px)
#         prop_buffer = 40
#         # does not apply to station or utilities
#         if curr_pos in [6, 13, 16, 26, 29, 36]:
#             prop_buffer = 0
#
#         # looking at the first row (from GO to Jail)
#         if curr_pos < 11:
#             # get x-coordinate of name (half the width of text to the left of the center of the tile)
#             x_name = tiles_coord[curr_pos-1][0]+(55-(name_img.get_rect().width/2))
#             # y-coordinate is 10 pixels below the top of the tile plus the buffer
#             y_name = 1147 + prop_buffer
#             # get x-coordinate of price (same process as above)
#             x_price = tiles_coord[curr_pos-1][0]+(55-(price_img.get_rect().width/2))
#             # get y-coordinate of price (10 pixels up from the bottom of the tile plus the height of the text)
#             y_price = 1300-(10 + price_img.get_rect().height)
#         # looking at second row (from Jail to Free Parking) - so rotated 90 degrees clockwise
#         elif curr_pos < 21:
#             # rotate image
#             name_img = pygame.transform.rotate(name_img, 90)
#             # get x-coordinate of name (10 pixels to the left of the tile's border plus width of text plus buffer)
#             x_name = 155-(10+name_img.get_rect().width-prop_buffer)
#             # get y-coordinate of name (half the height of the text up from the center of the tile_
#             y_name = tiles_coord[curr_pos-1][1]+(55-(name_img.get_rect().height/2))
#             # get x-coordinate of price (10 px from the left side of tile)
#             x_price =
#             # get y-coordinate of price
#
#         elif curr_pos < 31:
#             # get x-coordinate of name
#
#             # get y-coordinate of name
#
#             # get x-coordinate of price
#
#             # get y-coordinate of price
#
#         else:
#             # get x-coordinate of name
#
#             # get y-coordinate of name
#
#             # get x-coordinate of price
#
#             # get y-coordinate of price
#
#         # draw the name on image
#         screen.blit(name_img, (x_name, y_name))
#         # draw price on image
#         screen.blit(price_img, (x_price, y_price))

run = True
while run:

    screen.blit(background, (450, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
