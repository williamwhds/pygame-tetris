import pygame
from matrix import Matrix
from time import time

class Piece:
    def __init__(self, color:tuple, xpos:int, ypos:int):
        '''Creates a piece object with the specified color, x/row position and y/column position'''
        self.color = color # (R, G, B)
        self.xpos = xpos # Rows
        self.ypos = ypos # Columns
        self.moving = True # If the piece is moving or not

    def draw(self, screen:tuple):
        '''Draws the piece on the screen'''
        x = 100 + 5 + 20 * (self.xpos - 1 if self.xpos > 0 else 0) # Conditional to prevent negative values
        y = 50 + 5 + 20 * (self.ypos - 1 if self.ypos > 0 else 0)

        # Getting a darker color for the piece's outline
        a, b, c = self.color # Extracting the piece's color
        
        # Darkening it
        a -= 65 
        b -= 65
        c -= 65
        rgb = [a, b, c]
        for i in range(3):
            if rgb[i] < 0:
                rgb[i] = 0
        darker_color = tuple(rgb)
        
        pygame.draw.rect(
            screen,
            darker_color,
            [x, y, 20, 20]
        )

        pygame.draw.rect(
            screen,
            self.color,
            [x, y, 17, 17],
        )

    def drop_and_collision(self, clock_time:int, matrix:Matrix):
        '''Drops the piece and checks for collisions; Calls the remove_full_line method from the matrix when the piece stops moving'''
        if self.moving: # If the piece is moving
            # If there is a piece below or the piece is at the bottom of the screen
            if matrix.check_collision(self.ypos+1, self.xpos):
                self.moving = False
                matrix.set_collision(self.ypos, self.xpos, self)
                if matrix.remove_full_line():
                    matrix.score += 1
                matrix.print()
                print(f"X:{self.xpos}, Y:{self.ypos}")
            elif self.ypos >= len(matrix.matrix):
                self.ypos = len(matrix.matrix)
                self.moving = False
                matrix.set_collision(self.ypos, self.xpos, self)
                if matrix.remove_full_line():
                    matrix.score += 1
                matrix.print()
                print(f"X:{self.xpos}, Y:{self.ypos}")
                
            if clock_time < int(time()): # A second has passed and the piece is moving
                self.ypos += 1
    
    def move_left(self, matrix:Matrix):
        '''Moves the piece to the left and checks for collisions'''
        if self.moving:
            if matrix.check_collision(self.ypos, self.xpos-1) == False and self.xpos > 1:
                self.xpos -= 1
    
    def move_right(self, matrix:Matrix):
        '''Moves the piece to the right and checks for collisions'''
        if self.moving:
            if matrix.check_collision(self.ypos, self.xpos+1) == False and self.xpos < matrix.columns:
                self.xpos += 1

    def move_down(self, matrix:Matrix):
        '''Moves the piece down and checks for collisions'''
        if self.moving:
            if matrix.check_collision(self.ypos+1, self.xpos) == False and self.ypos < matrix.rows:
                self.ypos += 1
