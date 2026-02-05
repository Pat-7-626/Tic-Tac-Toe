class TicTacToeGame:
    def __init__(self):
        self.board = [" " for _ in range(9)]  # 3x3 board as a 1D list
        self.current_player = "X"
        self.winner = None
        self.game_over = False

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.winner = None
        self.game_over = False

    def make_move(self, position):
        """
        Attempts to make a move at the given position (0-8).
        Returns True if successful, False if invalid.
        """
        if self.game_over or self.board[position] != " ":
            return False

        self.board[position] = self.current_player
        
        winning_line = self._check_winner(self.current_player)
        if winning_line:
            self.winner = self.current_player
            self.game_over = True
            return winning_line # Return the winning line for UI to highlight
        elif " " not in self.board:
            self.game_over = True  # Draw
            
        if not self.game_over:
            self._switch_player()
            
        return True

    def _switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def _check_winner(self, player):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Cols
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        
        for a, b, c in win_conditions:
            if self.board[a] == player and self.board[b] == player and self.board[c] == player:
                return (a, b, c) # Return indices
        return None

    def get_empty_cells(self):
        return [i for i, x in enumerate(self.board) if x == " "]
