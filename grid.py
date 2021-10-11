import pygame
import os

LX= pygame.image.load(os.path.join('images','letterX.png'))
LO= pygame.image.load(os.path.join('images','LetterO.png'))


class Grid:
    def __init__(self):
        self.grid_lines=[((0,200), (600,200)),
                         ((0,400), (600,400)),
                         ((200,0), (200,600)),
                         ((400,0), (400,600))]

        self.grid=[[0 for x in range(3)] for y in range (3)]
        self.switch_player= True
        self.search_dir = [(0,-1) ,(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1)]
        self.game_over=False


    def draw(self,screen):
        for line in self.grid_lines:
            pygame.draw.line(screen ,(200,200,200), line[0],line[1],2)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    screen.blit(LX, (x * 200, y * 200))
                elif self.get_cell_value(x, y) == "O":
                    screen.blit(LO, (x * 200, y * 200))

    def print_grid(self):
        for row in self.grid:
            print(row)

    def get_cell_value(self ,x ,y):
        return self.grid[y][x]

    def set_cell_value(self ,x ,y, value):
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        if self.get_cell_value(x, y) == 0:
            self.switch_player = True
            if player == "X":
                self.set_cell_value(x, y, "X")
            elif player == "O":
                self.set_cell_value(x, y, "O")
            self.check_grid(x, y, player)
        else:
            self.switch_player = False

    def is_within_bound(self,x,y):
        return 0 <= x < 3 and 0 <= y < 3

    def check_grid(self, x, y, player):
        count = 1
        for index, (dirx, diry) in enumerate(self.search_dir):
            if self.is_within_bound(x + dirx, y + diry) and self.get_cell_value(x + dirx, y + diry) == player:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.is_within_bound(xx + dirx, yy + diry) and self.get_cell_value(xx + dirx, yy + diry) == player:
                    count += 1
                    if count == 3:
                        break

                if count < 3:
                    new_dir = 0
                    # now we need to reverse the direction or else we can count 3 cells but they might not be a row or a column
                    if index == 0:
                        new_dir = self.search_dir[4]  # N to S
                    elif index == 1:
                        new_dir = self.search_dir[5]  # NW to SE
                    elif index == 2:
                        new_dir = self.search_dir[6]  # W to E
                    elif index == 3:
                        new_dir = self.search_dir[7]  # SW to NE
                    elif index == 4:
                        new_dir = self.search_dir[0]  # S to N
                    elif index == 5:
                        new_dir = self.search_dir[1]  # SE to NW
                    elif index == 6:
                        new_dir = self.search_dir[2]  # E to W
                    elif index == 7:
                        new_dir = self.search_dir[3]  # NE to SW

                    if self.is_within_bound(x + new_dir[0], y + new_dir[1]) and self.get_cell_value(x + new_dir[0],
                                                                                                    y + new_dir[
                                                                                                        1]) == player:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1

        if count == 3:
            print(player, "Wins!!!")
            self.winner = player
            self.game_over = True
        else:
            self.winner = None
            self.game_over = self.finish()



    def finish(self):
        for row in self.grid:
            for value in row:
                if value==0:
                    return False
        return True

    def clear(self):
        for y in range (len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x,y,0)

    def print_grid(self):
        for r in self.grid:
            print(r)