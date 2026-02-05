import random
from game_logic import TicTacToeGame

class AIPlayer:
    def __init__(self, difficulty="Hard"):
        self.difficulty = difficulty

    def get_move(self, game: TicTacToeGame):
        if self.difficulty == "Easy":
            return self._get_random_move(game)
        elif self.difficulty == "Medium":
            return self._get_medium_move(game)
        else:
            return self._get_best_move(game)

    def _get_medium_move(self, game):
        # Medium: 50% chance to block/win, 50% random
        # Or simpler: Always block/win if immediate, but no depth searching
        
        # Check for immediate win
        for i in game.get_empty_cells():
            game.board[i] = game.current_player
            if game._check_winner(game.current_player):
                game.board[i] = " "
                return i
            game.board[i] = " "
            
        # Check for immediate block
        opponent = "O" if game.current_player == "X" else "X"
        for i in game.get_empty_cells():
            game.board[i] = opponent
            if game._check_winner(opponent):
                game.board[i] = " "
                return i
            game.board[i] = " "
            
        # Otherwise random
        return self._get_random_move(game)

    def _get_random_move(self, game):
        empty = game.get_empty_cells()
        return random.choice(empty) if empty else None

    def _get_best_move(self, game):
        best_score = -float('inf')
        move = None
        
        # Optimization: If it's the first move, pick the center or a corner randomly to save time
        if len(game.get_empty_cells()) == 9:
            return 4 # Center
            
        for i in game.get_empty_cells():
            game.board[i] = "O" # AI is always 'O' in this context usually, logic needs current player
            # But the AI is playing as 'O' (usually), let's assume usage pattern:
            # Player is X, AI is O.
            
            # Wait, better design: Pass the AI's symbol. 
            # But let's assume the game state 'current_player' is the AI when this is called.
            ai_symbol = game.current_player
            
            score = self._minimax(game, 0, False, ai_symbol)
            game.board[i] = " "
            
            if score > best_score:
                best_score = score
                move = i
                
        return move

    def _minimax(self, game, depth, is_maximizing, ai_symbol):
        human_symbol = "X" if ai_symbol == "O" else "O"
        
        if game._check_winner(ai_symbol):
            return 10 - depth
        if game._check_winner(human_symbol):
            return depth - 10
        if " " not in game.board:
            return 0
            
        if is_maximizing:
            best_score = -float('inf')
            for i in game.get_empty_cells():
                game.board[i] = ai_symbol
                score = self._minimax(game, depth + 1, False, ai_symbol)
                game.board[i] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in game.get_empty_cells():
                game.board[i] = human_symbol
                score = self._minimax(game, depth + 1, True, ai_symbol)
                game.board[i] = " "
                best_score = min(score, best_score)
            return best_score
