import pygame
from time import time
from matrix import Matrix
from piece import Piece

'''
    TODO:
    - Make full tetriminos
    - Add a way to use game clock instead of time.clock()
    - Add a way to rotate the piece (space key)
    - Add a way to push the piece all the way down (up arrow key)
    - Add a way to hold a piece (enter key)
    - Add a way to make a ghost piece (piece that shows where the piece will land)
    - Add a way to make a next piece box
    - Add game over condition and screen
    - delete_full_line() function might be broken (2 or more lines are deleted at once but score is only increased by 1)
'''

BLUE = (0, 0, 155)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)

l_shape = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 0]
]

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def run_tetris_game():
    pygame.init()

    time_clock = int(time())    # The time in seconds
    clock = pygame.time.Clock() # Used to limit the frame rate

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    font = pygame.font.SysFont(None, 25)

    matrix = Matrix(10, 20)
    current_piece = Piece(ORANGE, 1, 1)

    while True:
        clock.tick(10)

        screen.fill(BLACK)

        if current_piece.moving == False:
            current_piece = Piece(ORANGE, 1, 1)

        matrix.draw_all(screen, font)

        get_input(matrix, current_piece)

        current_piece.draw(screen)
        current_piece.drop_and_collision(time_clock, matrix)

        time_clock = int(time())

        pygame.display.update()

def get_input(matrix:Matrix, current_piece:Piece):
    '''Gets the input from the user'''
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_piece.move_left(matrix)
            elif event.key == pygame.K_RIGHT:
                current_piece.move_right(matrix)
            elif event.key == pygame.K_DOWN:
                current_piece.move_down(matrix)
        elif event.type == pygame.QUIT:
            pygame.quit()

run_tetris_game()
