import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 700
SQUARE_SIZE = WIDTH // 8
BROWN = (139, 69, 19)
PALE_WHITE = (255, 222, 173)
LIGHT_GREEN = (144, 238, 144)
FONT = pygame.font.Font(None, 36)

# Define the positions of user's kings and boat
user_king1_col, user_king1_row = 4, 0  # User's first king
user_king2_col, user_king2_row = 4, 7  # User's second king
user_boat_col, user_boat_row = 0, 6  # User's boat

# Initialize user and opponent scores
user_points = 1000
opponent_points = 1000

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

# Create a Pygame window
pygame.display.set_caption("Chess Game")
# Create a Pygame window with an extended area for scores
window = pygame.display.set_mode((WIDTH + 300, HEIGHT))

# Variables to keep track of the selected piece and whether it's the user's turn
selected_piece = None
user_turn = True
highlighted_squares = []  # Store the highlighted squares

# Create a function to calculate valid moves for the kings and boat
def calculate_valid_moves(piece_col, piece_row, piece_type):
    valid_moves = []

    if piece_type == 'king':
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    new_col, new_row = piece_col + i, piece_row + j
                    if 0 <= new_col < 8 and 0 <= new_row < 8:
                        valid_moves.append((new_col, new_row))
    elif piece_type == 'boat':
        # Define boat's valid moves based on your rules
        # For example, moving in one direction at a time, not jumping over other pieces, etc.
        for i in range(1, 8):
            if piece_col + i < 8:
                valid_moves.append((piece_col + i, piece_row))
            if piece_col - i >= 0:
                valid_moves.append((piece_col - i, piece_row))
            if piece_row + i < 8:
                valid_moves.append((piece_col, piece_row + i))
            if piece_row - i >= 0:
                valid_moves.append((piece_col, piece_row - i))

    return valid_moves

# Create a function to highlight the valid moves for a piece
def highlight_valid_moves(valid_moves):
    for move in valid_moves:
        col, row = move
        pygame.draw.rect(chessboard, LIGHT_GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(chessboard, (0, 0, 0), (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and user_turn:
            col = event.pos[0] // SQUARE_SIZE
            row = event.pos[1] // SQUARE_SIZE
            if selected_piece is not None:
                # If a piece is already selected, dehighlight its valid moves
                for move in highlighted_squares:
                    col, row = move
                    color = BROWN if (col + row) % 2 == 0 else PALE_WHITE
                    pygame.draw.rect(chessboard, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if (col, row) == selected_piece:
                    # If the user clicks on the same piece again, unselect it
                    selected_piece = None
                    highlighted_squares = []
                else:
                    # If the user clicks on a different piece, update the selection
                    selected_piece = (col, row)
            elif (col, row) == (user_king1_col, user_king1_row) or (col, row) == (user_king2_col, user_king2_row):
                # User has clicked on a king
                selected_piece = (col, row)
                valid_moves = calculate_valid_moves(col, row, 'king')
                highlight_valid_moves(valid_moves)
                highlighted_squares = valid_moves
            elif (col, row) == (user_boat_col, user_boat_row):
                # User has clicked on the boat
                selected_piece = (col, row)
                valid_moves = calculate_valid_moves(col, row, 'boat')
                highlight_valid_moves(valid_moves)
                highlighted_squares = valid_moves

    # Draw points for both players within the larger box
    user_points_text = FONT.render(f"User Score: {user_points}", True, (0, 0, 0))
    opponent_points_text = FONT.render(f"Opponent Score: {opponent_points}", True, (0, 0, 0))

    # Adjust the position of the opponent's score text
    opponent_points_y = 20
    user_points_y = HEIGHT - 20 - user_points_text.get_height()


    pygame.draw.rect(window, BROWN, (WIDTH, 0, 300, HEIGHT))
    window.blit(chessboard, (0, 0))
    window.blit(user_king_img, (SQUARE_SIZE * user_king1_col, SQUARE_SIZE * user_king1_row))
    window.blit(user_king_img, (SQUARE_SIZE * user_king2_col, SQUARE_SIZE * user_king2_row))
    window.blit(user_boat_img, (SQUARE_SIZE * user_boat_col, SQUARE_SIZE * user_boat_row))
    window.blit(user_points_text, (WIDTH, user_points_y))
    window.blit(opponent_points_text, (WIDTH, opponent_points_y))
    


    pygame.display.update()
