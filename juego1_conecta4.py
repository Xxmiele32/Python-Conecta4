"""
Este módulo contiene el juego Conecta 4.
"""
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=redefined-outer-name
# Importaciones
import sys
import math
import numpy as np
import pygame
from button import Button
# Constantes
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
BG = pygame.image.load("assets/Background.png")
# Variables
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
pygame.mixer.init()
button_sfx = pygame.mixer.Sound("assets/smw_coin.wav")
piece_sfx = pygame.mixer.Sound("assets/smw_stomp.wav")
win_sfx = pygame.mixer.Sound("assets/smw_bonus_game_end.wav")
music = pygame.mixer.music.load("assets/2-19. Slot Machine.mp3")

def create_board():
    """
    Crea el tablero de juego con todas las posiciones inicializadas a cero.
    """
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    """
    Coloca una pieza en el tablero de Conecta 4.
    """
    board[row][col] = piece

def is_valid_location(board, col):
    """
    Verifica si la posicion seleccionada es valida en el tablero.
    """
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    """
    Mira cual es la siguiente fila disponible.
    """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    """"
    Imprime la tabla en pantalla.
    """
    print(np.flip(board, 0))

def winning_move(board, piece):
    """
    Mira todas las combinaciones posibles a donde el jugador gana.
    """
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

def draw_board(board):
    """
    Dibuja la tabla distinguiendo entre los 2 jugadores a donde el Jugador 1 tendra fichas rojas y el Jugador 2 tendra fichas amarillas.
    """
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
# Llamado de las funciones
board = create_board()
print_board(board)
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Menu")

def get_font(size):
    """
    Desde la carpeta de assets se coge la fuente y la devuelve al remitente.
    """
    return pygame.font.Font("assets/font.ttf", size)

draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

def juego():
    """
    Este es el loop principal del Juego a donde se espera la entrada de los 2 jugadores.
    """
    pygame.display.set_caption("Conecta 4")
    screen.fill("black")
    pygame.mixer.music.play(-1)
    draw_board(board)
    pygame.display.update()
    game_over = False
    turn = 0
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
                        piece_sfx.play()

                        if winning_move(board, 1):
                            label = myfont.render("Player 1 wins", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
                            pygame.mixer.music.stop()
                            win_sfx.play()
                            # pylint: enable=invalid-name

                # Se espera a que el jugador 2 haga su turno
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        piece_sfx.play()

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True
                            pygame.mixer.music.stop()
                            win_sfx.play()

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)
                    sys.exit()

#Menu principal
def main_menu():
    """
    Esta la estetica del menu y sus botones.
    """
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(335, 300),
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(335, 450),
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                button_sfx.play()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sfx.play()
                    juego()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sfx.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
