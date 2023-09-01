from collections.abc import Iterable
import pygame

BLUE = (0, 0, 155)
WHITE = (255, 255, 255)

class Matrix:
    '''A matrix that stores piece objects. Its methods are used to add, remove and check for collisions, draw the board and pieces and remove full lines. It also manages the score.'''
    def __init__(self, columns:int, rows:int):
        '''Initiates the score and creates a matrix with the specified amount of columns and rows.'''
        self.score = 0
        self.columns = columns
        self.rows = rows
        
        matrix = []

        for row in range(rows):
            new_row = []
            for column in range(columns):
                new_row.append(0)
            matrix.append(new_row)
        self.matrix = matrix

    def print(self):
        '''Prints the matrix; Replaces 0 with a dot and piece objects with ■'''
        for row in self.matrix:
            for column in row:
                if column == 0:
                    print(".", end=" ")
                else: print("■", end=" ")
            print()

    def set_collision(self, row:int, column:int, piece):
        '''Setting a collision in the matrix; Storing a piece dict made from from a piece object in the matrix'''
        value = {"color": piece.color, "xpos": piece.xpos, "ypos": piece.ypos} # The value to be stored in the matrix
        self.matrix[row-1][column-1] = value

    def check_collision(self, row:int, column:int):
        '''Checks if there is a piece object in the row and column provided. Returns True if there is, False if there isn't'''
        if row < 1 or row > self.rows or column < 1 or column > self.columns: # If the row or column is out of bounds
            return False
        elif self.matrix[row-1][column-1] != 0: # If there is a piece object in the row and column provided
            return True
        else: # No pieces here! :)
            return False

    def remove_collision(self, row:int, column:int):
        '''Removes a collision in the matrix'''
        self.matrix[row-1][column-1] = 0

    def draw(self, screen:tuple, piece:dict):
        '''Draws the piece on the screen. This is for dict/not moving pieces only'''
        x = 100 + 5 + 20 * (piece["xpos"] - 1 if piece["xpos"] > 0 else 0) # Conditional to prevent negative values
        y = 50 + 5 + 20 * (piece["ypos"] - 1 if piece["ypos"] > 0 else 0)

        # Getting a darker color for the piece's outline
        a, b, c = piece["color"] # Extracting the piece's color
        
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
            piece["color"],
            [x, y, 17, 17],
        )

    def draw_border(self, screen:tuple, box_size:int = 20):
        pygame.draw.rect(
            screen,
            BLUE,
            [100, 50, (10*box_size) + 10, (20*box_size) + 10], #x, y, width, height
            5
        )

    def draw_pieces(self, screen:tuple):
        '''Draws the pieces that are not moving on the screen'''
        for row in range(self.rows):
            for column in range(self.columns):
                cell_value = self.matrix[row][column]
                if isinstance(cell_value, dict): # If the cell contains a piece represented by a dictionary
                    self.draw(screen, cell_value)

    def draw_board(self, screen:tuple, x:int=100, y:int=50):
        row_count = self.rows
        column_count = self.columns
        for column in range(column_count):
            column = column + 1
            pygame.draw.line(screen, BLUE, (x + 5 + 20 * column, y), (x + 5 + 20 * column, y + 20 * row_count))
        for row in range(row_count):
            row = row + 1
            pygame.draw.line(screen, BLUE, (x, y + 5 + 20 * row), (x + 20 * column_count, y + 5 + 20 * row))

    def draw_score(self, screen:tuple, font:pygame.font.Font):
        '''Draws the score on the screen'''
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (320, 60))

    def draw_all(self, screen:tuple, font:pygame.font.Font):
        '''Draws the score, board, border and pieces'''
        self.draw_board(screen)
        self.draw_pieces(screen)
        self.draw_border(screen)
        self.draw_score(screen, font)

    def check_full_line(self):
        '''If it finds a row full of pieces, return the row's index. Else, return None. '''
        for row in range(self.rows):
            if all(self.matrix[row][column] != 0 for column in range(self.columns)):
                return row
        return None
    
    def remove_full_line(self):
        '''Removes a full line from the matrix, shifts the lines above it down and returns True. If there is no full line, returns False.'''
        full_line = self.check_full_line() # The index of the full line
        if full_line is not None: # If there is a full line
            for row in range(full_line, 0, -1):
                for column in range(self.columns):
                    self.matrix[row][column] = self.matrix[row-1][column]
                    if isinstance(self.matrix[row-1][column], dict):    # Dict's ypos needs to be updated for it to be drawn correctly.
                        self.matrix[row][column]["ypos"] += 1           # See draw_pieces method.
            for column in range(self.columns):
                self.matrix[0][column] = 0
            return True
        return False
