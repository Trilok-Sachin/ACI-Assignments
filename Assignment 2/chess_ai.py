import math

# Constants for piece types and players
EMPTY = ' '

P1 = 'P1'
P2 = 'P2'

P1S = 'P1S'
P1K = 'P1K'
P2S = 'P2S'
P2K = 'P2K'

# Create an empty 3x3 chess-like board
board = [[P1S, P1K, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, P2S, P2K]]

# Function to print the current board
def print_board():
    for row in board:
        print(row)


# Function to get the opponent player
def get_opponent(player):
    if player.startswith('P1'):
        return 'P2' 
    else:
        return 'P1'

# Function to check if a move is valid for the knight (K) piece
def is_valid_knight_move(board, start_x, start_y, end_x, end_y, piece):

    opponent_player = get_opponent(piece)

    dx = abs(start_x - end_x)
    dy = abs(start_y - end_y)
    return ((dx == 1 and dy == 2) or (dx == 2 and dy == 1)) and ((board[end_x][end_y]==EMPTY) or (board[end_x][end_y].startswith(opponent_player)))

# Function to check if a move is valid for the pawn (S) piece
def is_valid_pawn_move(board, start_x, start_y, end_x, end_y, piece):
    dx = end_x - start_x
    dy = end_y - start_y

    opponent_player = get_opponent(piece)

    if piece == P1S:
        
        return (dx == 1 and abs(dy) == 0 and board[end_x][end_y] == EMPTY) or (dx == 1 and abs(dy) == 1 and board[end_x][end_y].startswith(opponent_player))
    elif piece == P2S:
        return (dx == -1 and abs(dy) == 0 and board[end_x][end_y] == EMPTY) or (dx == -1 and abs(dy) == 1 and board[end_x][end_y].startswith(opponent_player))

# Function to check if a move is valid for any piece
def is_valid_move(board, start_x, start_y, end_x, end_y, piece):
    if start_x < 0 or start_x > 2 or start_y < 0 or start_y > 2:
        return False

    if end_x < 0 or end_x > 2 or end_y < 0 or end_y > 2:
        return False

    if piece in (P1S, P2S):
        return is_valid_pawn_move(board, start_x, start_y, end_x, end_y, piece)
    elif piece in (P1K, P2K):
        return is_valid_knight_move(board, start_x, start_y, end_x, end_y, piece)

# Function to check if a player has won
def has_won(player, board):
    opponent_pawn = P2S if player.startswith('P1') else P1S
    opponent_knight = P2K if player.startswith('P1') else P1K

    for row in board:
        if opponent_pawn in row or opponent_knight in row:
            return False
    return True

# Evaluation function
def evaluate(player):
    if has_won(player, board):
        return 1
    elif has_won(get_opponent(player), board):
        return -1
    else:
        return 0

def static_evaluation_function(board):

    #P1 pieces - P2 pieces
    eval_val = 0
    for row in board:
        for square in row:
            if square == P1S:
                eval_val += 1
            elif square == P1K:
                eval_val += 3
            elif square == P2S:
                eval_val -= 1
            elif square == P2K:
                eval_val -= 3
            
    return eval_val

def no_moves_left_for_player(player, board):
    if player == P1:
        P1_pieces = []
        P1S_row = None
        for i, row in enumerate(board):
            if P1S in row:
                P1_pieces.append(P1S)
                P1S_row = i
            elif P1K in row:
                P1_pieces.append(P1K)

        print(P1_pieces)
        if P1S in P1_pieces and P1K not in P1_pieces and P1S_row == 2:
            print('No moves left for player:', P1)
            return True
    else:
        P2_pieces = []
        P2S_row = None
        for i, row in enumerate(board):
            if P2S in row:
                P2_pieces.append(P2S)
                P2S_row = i
            elif P2K in row:
                P2_pieces.append(P2K)

        if P2S in P2_pieces and P2K not in P2_pieces and P2S == 0:
            print('No moves left for player:', P2)
            return True

            


# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):

    if depth == 0 or has_won(P1, board) or has_won(P2, board) or no_moves_left_for_player(P1, board) or no_moves_left_for_player(P2, board):
        print('static_evaluation_function', static_evaluation_function(board))
        
        return static_evaluation_function(board), None, None

    
    if maximizing_player:

        avl_pieces = [P1S, P1K]
        piece_wise_moves ={}
        for piece in avl_pieces:
            piece_wise_moves[piece] = generate_moves(board, piece)

        print(piece_wise_moves)

        max_eval = -math.inf
        best_move = None
        best_piece = None

        for piece in avl_pieces:
            for move in piece_wise_moves[piece]:

                child_board = [row[:] for row in board]
                child_board = apply_move(child_board, move, piece)

                eval, _, _ = minimax(child_board, depth - 1, alpha, beta, False)
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                    best_piece = piece
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        print(max_eval, best_move, best_piece)
        return max_eval, best_move, best_piece
    else:

        avl_pieces = [P2S, P2K]
        piece_wise_moves ={}
        for piece in avl_pieces:
            piece_wise_moves[piece] = generate_moves(board, piece)

        print(piece_wise_moves)

        min_eval = math.inf
        best_move = None
        best_piece = None

        for piece in avl_pieces:
            for move in piece_wise_moves[piece]:
                
                child_board = [row[:] for row in board]
                child_board = apply_move(child_board, move, piece)

                eval, _, _ = minimax(child_board, depth - 1, alpha, beta, True)
                print(move, eval)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                    best_piece = piece
                beta = min(beta, eval)
                
                if beta <= alpha:
                    break
        print(min_eval, best_move, best_piece)
        return min_eval, best_move, best_piece

# Function to generate all possible moves for a player
def generate_moves(board, piece):
    moves = []
    for start_x in range(3):
        for start_y in range(3):
            if board[start_x][start_y]==piece:
                for end_x in range(3):
                    for end_y in range(3):
                        if is_valid_move(board, start_x, start_y, end_x, end_y, piece):
                            moves.append((start_x, start_y, end_x, end_y))
    return moves

# Function to apply a move to the board
def apply_move(board, move, piece):

    start_x, start_y, end_x, end_y = move
    board[start_x][start_y] = EMPTY
    board[end_x][end_y] = piece

    return board
        

# Main game loop
current_player = P1

while True:
    print_board()
    print(f"Player {current_player}'s turn")

    if current_player.startswith('P1'):

        if no_moves_left_for_player(P2, board):
            
            print_board()

            print('Game Ends!')
            break

        avl_pieces = [P1S, P1K]
        start_x, start_y, end_x, end_y = -1, -1, -1, -1

        piece_to_move = input("Select the piece to move:")

        while not is_valid_move(board, start_x, start_y, end_x, end_y, piece_to_move):
            
            move = input("Enter your move (e.g., 'start_x start_y end_x end_y'): ").split()
            
            if len(move) != 4 or piece_to_move not in avl_pieces:
                print("Invalid input. Try again.", piece_to_move)
                continue
            start_x, start_y, end_x, end_y = map(int, move)

        if board[start_x][start_y] in avl_pieces and is_valid_move(board, start_x, start_y, end_x, end_y, piece_to_move):
            board = apply_move(board, (start_x, start_y, end_x, end_y), piece_to_move)

            if has_won(current_player, board):
                print_board()
                print(f"Player {current_player} wins!")
                break
            elif no_moves_left_for_player(current_player, board):
                
                print_board()
                break
                # print(f"Player {current_player} wins!")

            current_player = P2 if current_player.startswith('P1') else P1
    else:
        # AI's turn (Minimax algorithm)
        if no_moves_left_for_player(P1, board):
            
            print_board()
            print('Game Ends!')
            break
        print("AI's Turn...")
        _, best_move, best_piece = minimax(board, 3, -math.inf, math.inf, False)
        
        if best_move:
            board = apply_move(board, best_move, best_piece)

        if has_won(current_player, board):
            print_board()
            print(f"Player {current_player} wins!")
            break
        

        current_player = P1 if current_player.startswith('P2') else P2
