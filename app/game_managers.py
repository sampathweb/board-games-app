from board_games.tic_tac_toe import TicTacToe, InvalidMoveError


class InvalidGameError(Exception):
    """Raised when Game is not in registry
    """
    pass


class GameManager(object):

    def __init__(self):
        """Records All Games in a Dictionary and create a sequence of game ids
        """
        self.games = {}
        self.max_game_id = 100

    def _get_next_game_id(self):
        """Returns next game id
        """
        if self.max_game_id > 100000:
            self.max_game_id = 100
        self.max_game_id += 1
        return self.max_game_id

    def new_game(self, handler):
        """Creates a new Game and returns the game id
        """
        game_id = self._get_next_game_id()
        self.games[game_id] = {
            "handler_a": handler
        }
        return game_id

    def join_game(self, game_id, handler):
        """Returns game_id if join is successful.
        Raises InvalidGame when it could not join the game
        """
        game = self.get_game(game_id)
        if game.get("handler_b") is None:
            game["handler_b"] = handler
            return game_id
        # Game ID not found.
        raise InvalidGameError

    def end_game(self, game_id):
        """Removes the Game from the games registry
        """
        if game_id in self.games:
            del self.games[game_id]


    def get_pair(self, game_id, handler):
        """Returns the paired Handler
        """
        game = self.get_game(game_id)
        if handler == game.get("handler_a"):
            return game.get("handler_b")
        elif handler == game.get("handler_b"):
            return game.get("handler_a")
        else:
            raise InvalidGameError


    def get_game(self, game_id):
        """Returns the game instance.  Raises Error when game not found
        """
        game = self.games.get(game_id)
        if game:
            return game
        raise InvalidGameError



class TicTacToeGameManager(GameManager):
    """Extends Game Manager to add methods specific to TicTacToe Game
    """

    def new_game(self, handler):
        """Extend new_game with tic_tac_toe instance.
        """
        game_id = super().new_game(handler)
        game = self.get_game(game_id)

        game["tic_tac_toe"] = TicTacToe()
        return game_id


    def record_move(self, game_id, selection, handler):
        """Record the move onto tic_tac_toe instance
        """
        game = self.get_game(game_id)
        if handler == game.get("handler_a"):
            game["tic_tac_toe"].record_player_a_move(selection)
        elif handler == game.get("handler_b"):
            game["tic_tac_toe"].record_player_b_move(selection)


    def abort_game(self, game_id):
        """Aborts the game
        """
        game = self.get_game(game_id)
        tic_tac_toe = game["tic_tac_toe"]
        tic_tac_toe.abort_game()

    def has_game_ended(self, game_id):
        """Returns True if the game has ended.
        Game cound end because of them won or it's a draw or no more open positions.
        """
        game = self.get_game(game_id)
        tic_tac_toe = game["tic_tac_toe"]
        if tic_tac_toe.has_ended():
            game["result"] = tic_tac_toe.game_result
            return True
        return False

    def get_game_result(self, game_id, handler):
        """Returns game result with a "W", "L", "D" or "E"
        """
        game = self.get_game(game_id)
        if not game.get("result"):
            # Compute game result
            self.has_game_ended(game_id)

        if game["result"] == "D" or game["result"] == "E":
            return game["result"]
        elif (game["result"] == "A" and game["handler_a"] == handler) or \
                (game["result"] == "B" and game["handler_b"] == handler):
            return "W"
        elif game["result"]:
            return "L"
        else:
            return ""  # Game is still ON.
