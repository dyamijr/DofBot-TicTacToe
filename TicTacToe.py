class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]  # 3x3 board represented as a list
        self.current_winner = None  # Keep track of the winner

    def print_board(self):
        # Print the board in a user-friendly format
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    @staticmethod
    def print_board_nums():
        # Print a board with numbers indicating each position
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print("| " + " | ".join(row) + " |")

    def available_moves(self):
        # Return a list of available moves (empty spots on the board)
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def empty_squares(self):
        return " " in self.board

    def num_empty_squares(self):
        return self.board.count(" ")

    def make_move(self, square, letter):
        # Assign the square to the letter (X or O)
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check if the player has won
        row_ind = square // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([s == letter for s in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([s == letter for s in column]):
            return True

        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal1]) or all([s == letter for s in diagonal2]):
                return True

        return False


def minimax(state, depth, player):
    max_player = "X"  # Human player
    other_player = "O" if player == "X" else "X"

    # Base case: check for a terminal state
    if state.current_winner == other_player:
        return {"position": None, "score": 10 - depth if other_player == max_player else depth - 10}

    elif not state.empty_squares():  # No empty squares (tie)
        return {"position": None, "score": 0}

    if player == max_player:
        best = {"position": None, "score": -float("inf")}  # Maximize the max_player
    else:
        best = {"position": None, "score": float("inf")}  # Minimize the other_player

    for possible_move in state.available_moves():
        # Make a move
        state.make_move(possible_move, player)

        # Recursively call minimax
        sim_score = minimax(state, depth + 1, other_player)  # Switch players

        # Undo the move
        state.board[possible_move] = " "
        state.current_winner = None
        sim_score["position"] = possible_move  # Keep track of the move

        # Update the best score
        if player == max_player:  # Maximizing
            if sim_score["score"] > best["score"]:
                best = sim_score
        else:  # Minimizing
            if sim_score["score"] < best["score"]:
                best = sim_score

    return best


def play():
    game = TicTacToe()
    game.print_board_nums()

    letter = "X"  # Starting letter
    while game.empty_squares():
        if letter == "O":  # AI turn
            print("AI is thinking...")
            move = minimax(game, 0, "O")["position"]
        else:  # Human turn
            valid_square = False
            while not valid_square:
                square = input(f"{letter}'s turn. Input move (0-8): ")
                try:
                    square = int(square)
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                except ValueError:
                    print("Invalid square. Try again.")

            move = square

        # Make the move
        game.make_move(move, letter)
        game.print_board()
        print("")  # Empty line for spacing

        if game.current_winner:
            print(f"{letter} wins!")
            return

        # Switch players
        letter = "O" if letter == "X" else "X"

    print("It's a tie!")


if __name__ == "__main__":
    play()
