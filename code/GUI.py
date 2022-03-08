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


# def make_grid():
#     # board vertical lines
#     pygame.draw.line(screen, (255, 255, 255), (1900, 0), (1900, 1300))
#     pygame.draw.line(screen, (255, 255, 255), (1745, 0), (1745, 1300))
#     pygame.draw.line(screen, (255, 255, 255), (755, 0), (755, 1300))
#     pygame.draw.line(screen, (255, 255, 255), (600, 0), (600, 1300))
#     # board horizontal lines
#     pygame.draw.line(screen, (255, 255, 255), (600, 0), (1900, 0))
#     pygame.draw.line(screen, (255, 255, 255), (600, 155), (1900, 155))
#     pygame.draw.line(screen, (255, 255, 255), (600, 1145), (1900, 1145))
#     pygame.draw.line(screen, (255, 255, 255), (600, 1299), (1900, 1299))
#     # tile vertical lines
#     pygame.draw.line(screen, (255, 255, 255), (1635, 0), (1635, 155))
#     pygame.draw.line(screen, (255, 255, 255), (1525, 0), (1525, 155))
#     pygame.draw.line(screen, (255, 255, 255), (1415, 0), (1415, 155))
#     pygame.draw.line(screen, (255, 255, 255), (1305, 0), (1305, 155))
#     pygame.draw.line(screen, (255, 255, 255), (1195, 0), (1195, 155))
#     pygame.draw.line(screen, (255, 255, 255), (1085, 0), (1085, 155))
#     pygame.draw.line(screen, (255, 255, 255), (975, 0), (975, 155))
#     pygame.draw.line(screen, (255, 255, 255), (865, 0), (865, 155))
#     pygame.draw.line(screen, (255, 255, 255), (1635, 1145), (1635, 1300))
#     pygame.draw.line(screen, (255, 255, 255), (1525, 1145), (1525, 1300))
#     pygame.draw.line(screen, (255, 255, 255), (1415, 1145), (1415, 1300))
#     pygame.draw.line(screen, (255, 255, 255), (1305, 1145), (1305, 1300))
#     pygame.draw.line(screen, (255, 255, 255), (1195, 1145), (1195, 1300))
#     pygame.draw.line(screen, (255, 255, 255), (1085, 1145), (1085, 1300))
#     pygame.draw.line(screen, (255, 255, 255), (975, 1145), (975, 1300))
#     pygame.draw.line(screen, (255, 255, 255), (865, 1145), (865, 1300))
#     # tile horizontal lines
#     pygame.draw.line(screen, (255, 255, 255), (600, 265), (755, 265))
#     pygame.draw.line(screen, (255, 255, 255), (600, 375), (755, 375))
#     pygame.draw.line(screen, (255, 255, 255), (600, 485), (755, 485))
#     pygame.draw.line(screen, (255, 255, 255), (600, 595), (755, 595))
#     pygame.draw.line(screen, (255, 255, 255), (600, 705), (755, 705))
#     pygame.draw.line(screen, (255, 255, 255), (600, 815), (755, 815))
#     pygame.draw.line(screen, (255, 255, 255), (600, 925), (755, 925))
#     pygame.draw.line(screen, (255, 255, 255), (600, 1035), (755, 1035))
#     pygame.draw.line(screen, (255, 255, 255), (1745, 265), (1900, 265))
#     pygame.draw.line(screen, (255, 255, 255), (1745, 375), (1900, 375))
#     pygame.draw.line(screen, (255, 255, 255), (1745, 485), (1900, 485))
#     pygame.draw.line(screen, (255, 255, 255), (1745, 595), (1900, 595))
#     pygame.draw.line(screen, (255, 255, 255), (1745, 705), (1900, 705))
#     pygame.draw.line(screen, (255, 255, 255), (1745, 815), (1900, 815))
#     pygame.draw.line(screen, (255, 255, 255), (1745, 925), (1900, 925))
#     pygame.draw.line(screen, (255, 255, 255), (1745, 1035), (1900, 1035))



# get the tile data from excel
tiles = tile.Tile.load_tiles_from_xlsx("ExcelData/PropertyTycoonBoardData.xlsx")

# create list to store the coordinates of each tile
tiles_coord = []
# iterator to go through the 40 tiles
i = 1
# for first row (bottom) y is the same and x decreases by 110 each iteration (width of a tile)
x = 1145
for i in range (1, 11):
    tiles_coord.append((x, 1145))
    x -= 110
# for second row (left side) x is the same and y decreases by 110 each iteration
y = 1145
for i in range (11, 21):
    tiles_coord.append((155, y))
    y -= 110
# for third row (top) y is the same and x increases by 110 each iteration
x = 265
for i in range (21, 31):
    tiles_coord.append((x, 155))
    x += 110
#for fourth row (right side) x is same and y increases by 110 each iteration
y = 155
for i in range (31, 41):
    tiles_coord.append((1145, y))

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


    #make_grid()
    screen.blit(background, (450, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
