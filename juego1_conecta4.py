"""
Este módulo contiene la implementación del juego Conecta 4.
Incluye la lógica del juego, la gestión del tablero y la verificación de condiciones de victoria.
"""
# Importaciones
import sys
import math
import numpy as np
import pygame
# Constantes
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
# Variables
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=redefined-outer-name
game_over = False
turn = 0
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
# Crea una matriz llena de zeros y de la mida que sea establecida en row_count y column_count.
# Quien llame a esta funcion se le retornara el valor de la variable


def create_board():
    """
    Crea el tablero de juego de Conecta 4 con todas las posiciones inicializadas a cero.

    Returns:
        np.ndarray: Un array de NumPy con dimensiones (ROW_COUNT, COLUMN_COUNT) inicializado a cero.
    """
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board
# Escoge las cordenadas de la board y eso sea el lugar a donde la piece se posicionara


def drop_piece(board, row, col, piece):
    """
    Coloca una pieza en el tablero de Conecta 4.

    Args:
        board (np.ndarray): El tablero de juego representado como un array de NumPy.
        row (int): La fila en la que se colocará la pieza.
        col (int): La columna en la que se colocará la pieza.
        piece (int): El valor de la pieza a colocar en el tablero (por ejemplo, 1 para el jugador 1, 2 para el jugador 2).
    Returns:
        None
    """
    board[row][col] = piece

# Se asegura que el movimiento es valido, en el caso que lo sea devolvera al remitente un 0.


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0
# Se asegura que la siguiente fila este abierta, en el caso que lo sea devolvera la itirenacion.


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
# Printara la board por pantalla


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizonatl position |
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical position ---
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check posivitely diagonals /
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatitely diagonals \
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
# Esta funcion se encarga de dibujar la tabla con los circulos negros
# Para mas informacion porfavor vaya a la documentacion de pygame


def draw_board(board):
    # Jugador 1
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r *
                             SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    # Jugador 2
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()


# Llamada de las funciones
board = create_board()
print_board(board)
pygame.init()

# Creacion de la ventana
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
# Loop principal del juego
while not game_over:
    # Esto hace que si el jugador hace click en la X de la ventana el programa se cierre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Esto hace la animacion de arriba de la ficha y cambia de color dependiendo el juagdor
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(
                    screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(
                    screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
        # Se espera a que el jugador 1 haga su turno
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                        # pylint: enable=invalid-name

            # Se espera a que el jugador 2 haga su turno
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
