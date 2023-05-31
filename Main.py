import chess
import chess.engine

# Initialize the chess board
board = chess.Board()

# Function to evaluate the board position
def evaluate_board(board):
    # Calculate the score based on material advantage and position
    score = 0
    piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0  # Add the missing mapping for the king piece type
}


    for square, piece in board.piece_map().items():
        if piece.color == chess.WHITE:
            score += piece_values[piece.piece_type]
        else:
            score -= piece_values[piece.piece_type]

    return score

# Search for the best move 
def minimax(board, depth, alpha, beta, is_maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if is_maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function to get the best move for the AI
def get_best_move(board, depth):
    best_eval = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()

        if eval > best_eval:
            best_eval = eval
            best_move = move

    return best_move


depth = 3  # Set the search depth
while not board.is_game_over():
    print("Current board:")
    print(board)

    # AI's move
    best_move = get_best_move(board, depth)
    print("AI's move:", best_move)
    board.push(best_move)

    if board.is_game_over():
        break

    # User's move
    while True:
        user_move = input("Enter your move in UCI notation (e.g., e2e4): ")
        move = chess.Move.from_uci(user_move)
        if move in board.legal_moves:
            board.push(move)
            break
        else:
            print("Invalid move. Try again.")

print("Game over.")
print("Result:", board.result())
