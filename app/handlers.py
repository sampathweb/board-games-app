"""
Request Handlers
"""
from builtins import super
import logging
import json

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado import concurrent
from tornado import gen

logger = logging.getLogger("app")


class IndexHandler(RequestHandler):
    """Redirect to Tic-Tac-Toe"""
    def get(self):
        self.redirect('/tic-tac-toe')


class TicTacToeHandler(RequestHandler):
    """APP is live"""

    def get(self):
        self.render("tic_tac_toe.html")


class TicTacToeSocketHandler(WebSocketHandler):

    def initialize(self, game_manager, *args, **kwargs):
        self.game_manager = game_manager
        self.game_id = None
        self.game_result = ""
        super().initialize(*args, **kwargs)

    def open(self):
        self.send_message(action="open", message="Connected to Game Server")

    def _convert_int(self, game_id):
        try:
            return None, int(game_id)
        except (ValueError, TypeError):
            return "Game numbers need to be Numeric: {}".format(game_id), None

    def send_pair_message(self, action, **data):
        paired_handler = self.game_manager.get_pair(self.game_id, self)
        if paired_handler:
            return paired_handler.send_message(action, **data)
        else:
            return "Could not send message to the other Player"

    def on_message(self, message):
        # Verify the validity of message
        data = json.loads(message)
        action = data.get("action", "")
        error_msg = ""
        if action == "move":
            # Game is going on
            # Set turn to False and send message to opponent
            player_selection = data.get("player_move")
            player_move = (int(player_selection[0]), int(player_selection[2]))
            print(player_move)
            if player_move:
                self.game_manager.record_move(self.game_id, player_move, self)
            error_msg = self.send_message(action="opp-move")
            if not error_msg:
                error_msg = self.send_pair_message(action="move", opp_move=player_selection)
            else:
                # Send Error Message that Pair Disconnected?
                pass

            # Check if the game is still ON
            if self.game_manager.has_game_ended(self.game_id):
                game_result = self.game_manager.get_game_result(self.game_id, self)
                self.send_message(action="end", result=game_result)
                opp_result = "L" if game_result == "W" else game_result
                self.send_pair_message(action="end", result=opp_result)
                self.game_manager.end_game(self.game_id)

        elif action == "join":
            # Get the game id
            error_msg, game_id = self._convert_int(data.get("game_id"))

            if game_id and self.game_manager.join_game(game_id, self):
                # Joined the game.
                # Send message to Player A
                self.game_id = game_id
                # Tell both players that they have been paired, so reset the pieces
                if not error_msg:
                    error_msg = self.send_message(action="paired", game_id=game_id)
                if not error_msg:
                    error_msg = self.send_pair_message(action="paired", game_id=game_id)
                # One to wait, other to move
                if not error_msg:
                    error_msg = self.send_message(action="opp-move")
                if not error_msg:
                    error_msg = self.send_pair_message(action="move")
            else:
                error_msg = "Could not find the Game: {}".format(game_id)

        elif action == "new":
            # new Game
            # Create a new game id and respond the game id
            self.game_id = self.game_manager.new_game(self)
            if not error_msg:
                error_msg = self.send_message(action="wait-pair", game_id=self.game_id)
        elif action == "abort":
            self.game_manager.abort_game(self.game_id)
            self.send_message(action="end", game_id=self.game_id, result="A")
            self.send_pair_message(action="end", game_id=self.game_id, result="A")
            self.game_manager.end_game(self.game_id)
        else:
            error_msg = "Unknown Action"

        if error_msg:
            self.send_message(action="error", message=error_msg)

    def on_close(self):
        """Overwrites WebSocketHandler.close"""
        self.send_pair_message(action="end", game_id=self.game_id, result="A")
        self.game_manager.end_game(self.game_id)

    def send_message(self, action, **data):
        """Sends the message to the connected subscriber."""
        message = {
            "action": action,
            "data": data
        }
        try:
            self.write_message(json.dumps(message))
        except WebSocketClosedError:
            logger.warning("WS_CLOSED", "Could Not send Message: " + json.dumps(message))
            # Send Websocket Closed Error to Paired Opponent
            self.send_pair_message(action="pair-closed")
            self.close()