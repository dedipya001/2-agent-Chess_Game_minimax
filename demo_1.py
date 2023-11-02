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

# Define the positions of user's king and boat and opponent's king
user_king_col, user_king_row = 3, 0  # Adjust these values according to your initial setup
user_boat_col, user_boat_row = 4, 0
opponent_king_col, opponent_king_row = 3, 7  # Adjust these values as well

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

opponent_king_img = pygame.image.load("king.png")
opponent_king_img = pygame.transform.scale(opponent_king_img, (SQUARE_SIZE, SQUARE_SIZE))

# Create a Pygame window
pygame.display.set_caption("Chess Game")
# Create a Pygame window with an extended area for scores
window = pygame.display.set_mode((WIDTH + 300, HEIGHT))

# Variables to keep track of the selected piece and whether it's the user's turn
selected_piece = None
user_turn = True
highlighted_squares = []  # Store the highlighted squares

# Create a function to calculate valid moves for the king and boat
def calculate_valid_moves(piece_col, piece_row, piece_type):
    valid_moves = []
    selected_piece = None  # Initialize selected_piece as None
    user_turn = True
    highlighted_squares = [] 

    if piece_type == 'king':
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    new_col, new_row = piece_col + i, piece_row + j
                    if 0 <= new_col < 8 and 0 <= new_row < 8:
                        valid_moves.append((new_col, new_row))
    # ...
# Inside the event loop, handle boat movement
    elif piece_type == 'boat':
        if (col, row) == selected_piece:
            if event.type == pygame.KEYDOWN:
                new_col, new_row = col, row
                if event.key == pygame.K_LEFT:
                    # Move left
                    new_col -= 1
                elif event.key == pygame.K_RIGHT:
                    # Move right
                    new_col += 1
                elif event.key == pygame.K_UP:
                    # Move up
                    new_row -= 1
                elif event.key == pygame.K_DOWN:
                    # Move down
                    new_row += 1

                if 0 <= new_col < 8 and 0 <= new_row < 8:
                    # Check collision and path rules (for example, not jumping over other pieces)
                    # If your rules are met, update the user's point balance and the boat's position
                    if (new_col, new_row) != (user_king_col, user_king_row) and (new_col, new_row) != (opponent_king_col, opponent_king_row):
                        # Deduct points for the boat's movement (20 points per move)
                        user_points -= 20
                        # Update user points display
                        user_points_text = FONT.render(f"User Points: {user_points}", True, (0, 0, 0))
                        selected_piece = (new_col, new_row)
                # Update user points (if the move didn't happen, no point deduction)
                else:
                    selected_piece = (col, row)
# ...


    return valid_moves

# Create a function to highlight the valid moves for a piece
def highlight_valid_moves(valid_moves):
    for move in valid_moves:
        col, row = move
        pygame.draw.rect(chessboard, LIGHT_GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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
            elif (col, row) == (user_king_col, user_king_row):
                # User has clicked the king
                selected_piece = (col, row)
                valid_moves = calculate_valid_moves(col, row, 'king')
                highlight_valid_moves(valid_moves)
                highlighted_squares = valid_moves
            elif (col, row) == (user_boat_col, user_boat_row):
                # User has clicked the boat
                selected_piece = (col, row)
                valid_moves = calculate_valid_moves(col, row, 'boat')
                highlight_valid_moves(valid_moves)
                highlighted_squares = valid_moves

    # Draw the chessboard and pieces
    window.blit(chessboard, (0, 0))
    window.blit(user_king_img, (SQUARE_SIZE * user_king_col, SQUARE_SIZE * user_king_row))
    window.blit(user_boat_img, (SQUARE_SIZE * user_boat_col, SQUARE_SIZE * user_boat_row))
    window.blit(opponent_king_img, (SQUARE_SIZE * opponent_king_col, SQUARE_SIZE * opponent_king_row))

    # Draw a larger box-like area for scores at the top right corner
    pygame.draw.rect(window, (220, 220, 220), (WIDTH, 0, 300, HEIGHT))

    # Draw points for both players within the larger box
    user_points_text = FONT.render("User Points: 1000", True, (0, 0, 0))
    opponent_points_text = FONT.render("Opponent Points: 1000", True, (0, 0, 0))

    user_points_y = 20
    opponent_points_y = user_points_text.get_height() + user_points_y + 10

    window.blit(user_points_text, (WIDTH + 20, user_points_y))
    window.blit(opponent_points_text, (WIDTH + 20, opponent_points_y))

    pygame.display.update()
