import pygame
from pygame.locals import *
import tile

pygame.init()
# ef978b

start_screen_size = (800, 800)
game_size = (1650, 975)
screen = pygame.display.set_mode(start_screen_size)
pygame.display.set_caption('Property Tycoon')
pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(740, 740, 60, 60))
board = pygame.image.load("Images/Board2.png")
play_original = pygame.image.load("Images/PlayOriginal.png")
play_abridged = pygame.image.load("Images/PlayAbridged.png")
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
# get the tile data from excel
tiles = tile.Tile.load_tiles_from_xlsx("ExcelData/PropertyTycoonBoardData.xlsx")
# define board height and width
board_height = board_width = game_size[1]
# define tile width
tile_width = 82.5
# define tile height
tile_height = 116.25
# create font to be used
font = pygame.font.SysFont('franklingothicmediumcond', 15)
BLACK = (0, 0, 0)


class ScreenTracker:

    def __init__(self):
        self.start_menu1 = True
        self.start_menu2 = False
        self.start_menu3 = False
        self.start_menu4 = False
        self.playing_game = False
        self.normal_mode = True
        self.no_of_players = 0
        self.no_of_ai = 0
        self.start_screen1()

    def start_screen1(self):
        while self.start_menu1:
            pygame.display.set_mode(start_screen_size)
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
                        self.playing_game = True
                        self.start_menu4 = False
                        self.game_screen()

    # function to populate an array with the coordinates of each tile
    def get_coordinates(self):
        # create list to store the coordinates of each tile
        coord_list = []
        # iterator to go through the 40 tiles
        i = 1

        # first get screen width without board because there is space on either side of board (2/3 on left and 1/3 on
        # right)
        screen_width_excl_board = game_size[0] - board_width

        # x starts where board ends minus the height of a tile (because first tile, GO, is in bottom right)
        x = (game_size[0] - screen_width_excl_board * (1 / 3)) - tile_height
        # y is the screen height minus height of a tile (because there is no space below board)
        y = game_size[1] - tile_height
        for i in range(1, 11):
            # for first row (bottom) y stays the same and x decreases by width of a tile each iteration
            coord_list.append((x, y))
            x -= tile_width

        # x is where the board starts plus the height of a tile
        x = (screen_width_excl_board * (2 / 3)) + tile_height
        # y starts at screen height - height of a tile
        y = game_size[1] - tile_height
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
        x = (game_size[0] - screen_width_excl_board * (1 / 3)) - tile_height
        # y starts at the height of a tile
        y = tile_height
        for i in range(31, 41):
            coord_list.append((x, y))
            y += tile_width

        return coord_list

    # function to wrap text in tiles (if necessary)
    def wrap_text(self, s):
        # create list to store rendered text images
        imgs = []
        # render image of string
        string_img = font.render(str(s), True, BLACK)
        # check width to see if it fits in tile (with gap of 7.5 px on either side)
        if string_img.get_rect().width > 64.5:
            # split given string into words
            words = s.split()

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
            imgs.append(s)
        return imgs

    # function to print text on board
    def get_text(self):
        # get tile coordinates
        tiles_coord = self.get_coordinates()
        # write the text for each tile
        for t in tiles:
            # get current tile's position
            curr_pos = t.pos
            # skip non-customisable tiles (corners, pot lucks, opportunity knocks, and taxes)
            if curr_pos in [1, 3, 5, 8, 11, 18, 21, 23, 31, 34, 37, 39]:
                continue
            else:
                # get text for name and pass to wrap text function
                name = self.wrap_text(t.space)
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

    def game_screen(self):
        while self.playing_game:
            pygame.display.set_mode(game_size)
            screen.blit(board, (450, 0))
            self.get_text()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing_game = False
                    break


screen_tracker = ScreenTracker()
# run = True
# while run:
#     pygame.display.update()
#     screen_tracker.start_screen1()
#     screen_tracker.start_screen2()
#     screen_tracker.game_screen()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#             break


pygame.quit()
