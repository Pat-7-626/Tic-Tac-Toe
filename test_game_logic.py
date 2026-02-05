import unittest
from game_logic import TicTacToeGame
from ai_opponent import AIPlayer

class TestTicTacToeLogic(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToeGame()

    def test_initial_state(self):
        self.assertEqual(self.game.current_player, "X")
        self.assertFalse(self.game.game_over)
        self.assertEqual(len(self.game.get_empty_cells()), 9)

    def test_make_move(self):
        self.assertTrue(self.game.make_move(0))
        self.assertEqual(self.game.board[0], "X")
        self.assertEqual(self.game.current_player, "O")

    def test_win_condition(self):
        # X wins row 0
        moves = [0, 3, 1, 4, 2] # X, O, X, O, X
        for m in moves:
            self.game.make_move(m)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "X")

    def test_draw_condition(self):
        # X O X
        # X O X
        # O X O
        moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]
        # X(0), O(1), X(2), O(4), X(3), O(5), X(7), O(6), X(8) -> Move sequence
        # Board:
        # X(0) O(1) X(2)
        # X(3) O(4) O(5) - Wait, let's just force the board
        self.game.board = [
            "X", "O", "X",
            "X", "O", "X",
            "O", "X", "O"
        ]
        self.game.current_player = "X" # Irrelevant
        # Normally check is called after a move.
        # But let's play IT out properly to be safe or mock it
        
        # Reset
        self.game.reset_game()
        # 0:X, 1:O, 2:X
        # 4:O, 3:X, 5:O
        # 7:X, 6:O, 8:X -> Draw
        sequence = [0, 1, 2, 4, 3, 5, 7, 6, 8]
        for m in sequence:
            self.game.make_move(m)
            
        self.assertTrue(self.game.game_over)
        self.assertIsNone(self.game.winner)

class TestAI(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToeGame()
        self.ai = AIPlayer(difficulty="Hard")

    def test_ai_blocks_win(self):
        # X X _
        # _ O _
        # _ _ _
        # Player X is threatening to win at 2. AI (O) should block.
        self.game.board = ["X", "X", " ", " ", "O", " ", " ", " ", " "]
        self.game.current_player = "O"
        move = self.ai.get_move(self.game)
        self.assertEqual(move, 2)

    def test_ai_takes_win(self):
        # O O _
        # X X _
        # _ _ _
        # AI (O) should win at 2
        self.game.board = ["O", "O", " ", "X", "X", " ", " ", " ", " "]
        self.game.current_player = "O"
        move = self.ai.get_move(self.game)
        self.assertEqual(move, 2)

if __name__ == '__main__':
    unittest.main()
