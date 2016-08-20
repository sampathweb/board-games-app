from board_games.tic_tac_toe import TicTacToe, InvalidMoveError


class GameManager(object):

    def __init__(self):
        # Record all the games
        self.games = {}
        self.max_game_id = 100


    def new_game(self, handler):
        self.max_game_id += 1
        self.games[self.max_game_id] = {
            "handler_a": handler
        }
        return self.max_game_id

    def join_game(self, game_id, handler):

        game = self.games.get(game_id)
        if game:
            game["handler_b"] = handler
            return game_id
        # Game ID not found
        # Raise Error
        return None

    def end_game(self, game_id):

        if game_id in self.games:
            del self.games[game_id]


    def get_pair(self, game_id, handler):

        game = self.games.get(game_id)
        if game:
            if handler == game.get("handler_a"):
                return game.get("handler_b")
            else:
                return game.get("handler_a")
        return None

    def get_game(self, game_id):
        game = self.games.get(game_id)
        if game:
            return game
        else:
            # TODO: Raise Error
            return None



class TicTacToeGameManager(GameManager):

    def new_game(self, handler):
        game_id = super().new_game(handler)
        game = self.games[game_id]

        game["tic_tac_toe"] = TicTacToe()
        return game_id


    def record_move(self, game_id, selection, handler):

        game = self.get_game(game_id)
        if handler == game.get("handler_a"):
            game["tic_tac_toe"].record_player_a_move(selection)
        elif handler == game.get("handler_b"):
            game["tic_tac_toe"].record_player_b_move(selection)


    def abort_game(self, game_id):
        game = self.get_game(game_id)
        tic_tac_toe = game["tic_tac_toe"]
        tic_tac_toe.abort_game()

    def has_game_ended(self, game_id):

        game = self.get_game(game_id)
        tic_tac_toe = game["tic_tac_toe"]
        if tic_tac_toe.has_ended():
            game["result"] = tic_tac_toe.game_result
            return True
        return False

    def get_game_result(self, game_id, handler):

        game = self.get_game(game_id)
        if not game.get("result"):
            # Compute game result
            self.has_game_ended(game_id)

        if game["result"] == "D":
            return game["result"]
        elif (game["result"] == "A" and game["handler_a"] == handler) or \
                (game["result"] == "B" and game["handler_b"] == handler):
            return "W"
        elif game["result"]:
            return "L"
        else:
            return ""  # Game is still ON.
