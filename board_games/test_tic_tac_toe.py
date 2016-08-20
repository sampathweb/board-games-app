import unittest
from tic_tac_toe import TicTacToe


class TicTacToeTest(unittest.TestCase):
    """Test Cases for TicTacToe
    """

    def test_creation(self):
        self.assertIsNotNone(TicTacToe())

    def test_player_a_win(self):
        game = TicTacToe()
        game.record_player_a_move((0,0))
        game.record_player_b_move((0,1))
        game.record_player_a_move((1,0))
        game.record_player_b_move((1,1))
        self.assertFalse(game.has_ended())
        game.record_player_a_move((2,0))
        self.assertTrue(game.has_ended())
        self.assertEqual(game.game_result, "A")


    def test_player_a_lost(self):
        game = TicTacToe()
        game.record_player_a_move((0,0))
        game.record_player_b_move((0,1))
        game.record_player_a_move((1,0))
        game.record_player_b_move((1,1))
        game.record_player_a_move((2,2))
        self.assertFalse(game.has_ended())
        game.record_player_b_move((2,1))
        self.assertTrue(game.has_ended())
        self.assertEqual(game.game_result, "B")

    def test_draw(self):
        game = TicTacToe()
        game.record_player_a_move((0,0))
        game.record_player_b_move((0,1))
        game.record_player_a_move((1,0))
        game.record_player_b_move((1,1))
        game.record_player_a_move((2,2))
        game.record_player_b_move((2,0))
        game.record_player_a_move((2,1))
        game.record_player_b_move((1,2))
        self.assertFalse(game.has_ended())
        game.record_player_a_move((0,2))
        self.assertTrue(game.has_ended())
        self.assertEqual(game.game_result, "D")

    def test_abort(self):
        game = TicTacToe()
        game.record_player_a_move((0,0))
        game.abort_game()
        self.assertTrue(game.has_ended())
        self.assertEqual(game.game_result, "E")


if __name__ == "__main__":
    unittest.main()
