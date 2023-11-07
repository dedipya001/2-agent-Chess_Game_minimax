import pygame
from pygame.locals import *
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 700
SQUARE_SIZE = WIDTH // 8
BROWN = (139, 69, 19)
PALE_WHITE = (255, 222, 173)
LIGHT_GREEN = (144, 238, 144)
FONT = pygame.font.Font(None, 36)

# Define the positions of user's king and boat
user_king_col, user_king_row = 4, 7  # User's king
user_boat_col, user_boat_row = 0, 7  # User's boat

# Define the position of the opponent's king on the first row
opponent_king_col, opponent_king_row = 4, 0  # Opponent's king

# Initialize user score
user_points = 1000

# Initialize Opponent King Kills
opponent_king_kills = 0

# Create the chessboard surface
chessboard = pygame.Surface((WIDTH, HEIGHT))
for row in range(8):
    for col in range(8):
        color = BROWN if (row + col) % 2 == 0 else PALE_WHITE
        pygame.draw.rect(chessboard, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Load and resize images for pieces
user_king_img = pygame.image.load("king.png")
user_king_img = pygame.transform.scale(user_king_img, (SQUARE_SIZE, SQUARE_SIZE))

user_boat_img = pygame.image.load("boat.png")
user_boat_img = pygame.transform.scale(user_boat_img, (SQUARE_SIZE, SQUARE_SIZE))

opponent_king_img = pygame.image.load("opponent_king.png")
opponent_king_img = pygame.transform.scale(opponent_king_img, (SQUARE_SIZE, SQUARE_SIZE))

# Create a Pygame window
pygame.display.set_caption("Chess Game")
window = pygame.display.set_mode((WIDTH + 300, HEIGHT))

# Variables to keep track of the selected piece and whose turn it is
selected_piece = None
user_turn = True  # User starts first
highlighted_squares = []  # Store the highlighted squares

# Point deductions for king and boat movements
KING_MOVE_COST = 10
BOAT_MOVE_COST = 20

# Function to respawn a killed piece
def respawn_piece():
    respawn_col = random.randint(0, 7)
    respawn_row = random.randint(0, 7)
    while (
        (respawn_col, respawn_row) == (opponent_king_col, opponent_king_row) or
        (respawn_col, respawn_row) == (user_king_col, user_king_row) or
        (respawn_col, respawn_row) == (user_boat_col, user_boat_row)
    ):
        respawn_col = random.randint(0, 7)
        respawn_row = random.randint(0, 7)
    return respawn_col, respawn_row

# Function to handle the opponent's turn
def opponent_turn():
    global user_turn, opponent_king_col, opponent_king_row, user_king_col, user_king_row, user_boat_col, user_boat_row, user_points, opponent_king_kills
    if not user_turn:
        pygame.time.wait(2000)  # Wait for 2 seconds
        # Implement the opponent's logic here (for example, random moves)
        opponent_valid_moves = calculate_valid_moves(opponent_king_col, opponent_king_row, 'king', user_king_col, user_king_row, user_boat_col, user_boat_row)
        if opponent_valid_moves:
            move = random.choice(opponent_valid_moves)
            # Check if the opponent's king kills the user's king
            if move == (user_king_col, user_king_row):
                user_king_col, user_king_row = respawn_piece()
                user_points -= 100
                opponent_king_kills += 1
                if opponent_king_kills == 3:
                    game_over("User Won")
            # Check if the opponent's king kills the user's boat
            elif move == (user_boat_col, user_boat_row):
                user_boat_col, user_boat_row = respawn_piece()
                user_points -= 100
            opponent_king_col, opponent_king_row = move
        user_turn = True

# Function to display the game over message
def display_game_over_message(result):
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render(f"Game Over - {result}", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        window.fill((255, 255, 255))  # Clear the window
        window.blit(game_over_text, game_over_rect)
        pygame.display.update()

# Function to check for game over conditions
def game_over(result):
    global user_turn
    display_game_over_message(result)
    user_turn = False

# Function to calculate valid moves for the king and boat
def calculate_valid_moves(piece_col, piece_row, piece_type, user_king_col, user_king_row, user_boat_col, user_boat_row):
    valid_moves = []

    if piece_type == 'king':
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    new_col, new_row = piece_col + i, piece_row + j
                    if 0 <= new_col < 8 and 0 <= new_row < 8 and (new_col, new_row) != (user_boat_col, user_boat_row):
                        valid_moves.append((new_col, new_row))
    elif piece_type == 'boat':
        valid_moves = []  # Initialize an empty list for the boat's valid moves
        for i in range(1, 8):
            if piece_col + i < 8 and (piece_col + i, piece_row) != (user_king_col, user_king_row):
                valid_moves.append((piece_col + i, piece_row))
            if piece_col - i >= 0 and (piece_col - i, piece_row) != (user_king_col, user_king_row):
                valid_moves.append((piece_col - i, piece_row))
            if piece_row + i < 8 and (piece_col, piece_row + i) != (user_king_col, user_king_row):
                valid_moves.append((piece_col, piece_row + i))
            if piece_row - i >= 0 and (piece_col, piece_row - i) != (user_king_col, user_king_row):
                valid_moves.append((piece_col, piece_row - i))

    return valid_moves

# Function to highlight the valid moves for a piece
def highlight_valid_moves(valid_moves):
    for move in valid_moves:
        col, row = move
        pygame.draw.rect(chessboard, LIGHT_GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(chessboard, (0, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)

# Function to move the selected piece
def move_piece(selected_piece, col, row):
    global user_king_col, user_king_row, user_boat_col, user_boat_row, user_points
    if selected_piece == (user_king_col, user_king_row):
        user_king_col, user_king_row = col, row
        # Deduct points for king movement
        user_points -= KING_MOVE_COST
    elif selected_piece == (user_boat_col, user_boat_row):
        user_boat_col, user_boat_row = col, row
        # Deduct points for boat movement
        user_points -= BOAT_MOVE_COST

# Function to check if two pieces occupy the same square
def pieces_collide(col1, row1, col2, row2):
    return col1 == col2 and row1 == row2

# Function to remove a piece with animation
def remove_piece_with_animation(col, row):
    piece_image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    original_image = None

    if pieces_collide(col, row, user_king_col, user_king_row):
        original_image = user_king_img
    elif pieces_collide(col, row, user_boat_col, user_boat_row):
        original_image = user_boat_img

    for alpha in range(255, 0, -10):
        piece_image.fill((255, 255, 255, alpha))  # Create a transparent white surface
        piece_image.blit(original_image, (0, 0))

        pygame.draw.rect(chessboard, BROWN if (col + row) % 2 == 0 else PALE_WHITE,
                         (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        window.blit(chessboard, (0, 0))
        window.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        pygame.display.update()
        pygame.time.delay(100)  # Control the speed of the animation

    pygame.draw.rect(chessboard, BROWN if (col + row) % 2 == 0 else PALE_WHITE,
                     (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    window.blit(chessboard, (0, 0))
    pygame.display.update()

    # After the animation, respawn the piece
    pass

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if user_turn:
            if event.type == MOUSEBUTTONDOWN:
                # User's turn
                col = event.pos[0] // SQUARE_SIZE
                row = event.pos[1] // SQUARE_SIZE
                if selected_piece is not None:
                    if (col, row) in highlighted_squares:
                        if pieces_collide(col, row, opponent_king_col, opponent_king_row):
                            # Respawn the killed opponent's king
                            opponent_king_col, opponent_king_row = respawn_piece()
                            user_points += 100
                            opponent_king_kills += 1
                            if opponent_king_kills == 3:
                                game_over("User Won")
                        move_piece(selected_piece, col, row)
                        selected_piece = None
                        for move in highlighted_squares:
                            col, row = move
                            color = BROWN if (col + row) % 2 == 0 else PALE_WHITE
                            pygame.draw.rect(chessboard, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                        highlighted_squares = []
                        user_turn = False  # Switch to opponent's turn
                        # Start the opponent's turn (with a 2-second delay)
                        pygame.time.set_timer(USEREVENT, 2000)
                    else:
                        selected_piece = None
                        for move in highlighted_squares:
                            col, row = move
                            color = BROWN if (col + row) % 2 == 0 else PALE_WHITE
                            pygame.draw.rect(chessboard, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                        highlighted_squares = []
                elif pieces_collide(col, row, user_king_col, user_king_row) or pieces_collide(col, row, user_boat_col, user_boat_row):
                    selected_piece = (col, row)
                    valid_moves = calculate_valid_moves(col, row, 'king' if selected_piece == (user_king_col, user_king_row) else 'boat',
                                                         user_king_col, user_king_row, user_boat_col, user_boat_row)
                    highlight_valid_moves(valid_moves)
                    highlighted_squares = valid_moves
        elif event.type == USEREVENT:
            # Opponent's turn after 2 seconds
            opponent_turn()

    # Check if the user's king or boat has been killed by the opponent's king
    if pieces_collide(user_king_col, user_king_row, opponent_king_col, opponent_king_row):
        user_king_col, user_king_row = respawn_piece()
        user_points -= 100
        user_king_kills += 1
        if user_king_kills == 3:
            game_over("User Lost")
    if pieces_collide(user_boat_col, user_boat_row, opponent_king_col, opponent_king_row):
        user_boat_col, user_boat_row = respawn_piece()
        user_points -= 100

    # Draw user's points within the larger box
    user_points_text = FONT.render(f"User Score: {user_points}", True, (0, 0, 0))

    # Adjust the position of the user's score text
    user_points_y = HEIGHT - 20 - user_points_text.get_height()

    pygame.draw.rect(pygame.display.get_surface(), BROWN, (WIDTH, 0, 300, HEIGHT))
    window.blit(chessboard, (0, 0))
    window.blit(user_king_img, (SQUARE_SIZE * user_king_col, SQUARE_SIZE * user_king_row))
    window.blit(user_boat_img, (SQUARE_SIZE * user_boat_col, SQUARE_SIZE * user_boat_row))
    window.blit(opponent_king_img, (SQUARE_SIZE * opponent_king_col, SQUARE_SIZE * opponent_king_row))
    window.blit(user_points_text, (WIDTH, user_points_y))

    pygame.display.update()

