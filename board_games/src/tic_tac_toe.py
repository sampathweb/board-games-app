#! /usr/bin/env python
from __future__ import print_function
from builtins import super

from collections import defaultdict
import random

from .exceptions import InvalidMoveError


class TicTacToe(object):
    """Defines the Rules and maintains the State of the TicTacToe App.
    """
    def __init__(self, play_bot=False, bot_level=1, player_a_marker="A", player_b_marker="B"):

        self.play_bot = play_bot
        self.player_a_marker = player_a_marker
        self.player_b_marker = player_b_marker
        self.reset_game(bot_level)

    def reset_game(self, bot_level):

        self.bot_level = bot_level
        # Set board positions
        self.game_choices = self._genrate_all_game_positions()

        self.winning_combos = self._generate_winning_positions()

        self.game_result = ""
        self.player_a_choices = set()
        self.player_b_choices = set()
        self.player_a_turn = True

    @property
    def game_result(self):
        return self._game_result

    @game_result.setter
    def game_result(self, value):
        self._game_result = value

    def get_valid_choices(self):
        return list(self.game_choices)

    def is_game_on(self):
        return self.game_result == ""

    def has_ended(self):
        return self.game_result != ""

    def abort_game(self):
        self.game_choices = []  # Reset Game Choices
        self.game_result = "E"  # Game Aborted

    def _genrate_all_game_positions(self):
        game_choices = []
        for row in range(3):
            for col in range(3):
                game_choices.append((row,col))

        return game_choices

    def _generate_winning_positions(self):
        winning_combos = []
        for row in range(3):
            win_set = set()
            for col in range(3):
                win_set.add((row,col))
            winning_combos.append(win_set)
        for col in range(3):
            win_set = set()
            for row in range(3):
                win_set.add((row,col))
            winning_combos.append(win_set)
        winning_combos.append(set([(0,0), (1,1), (2,2)]))
        winning_combos.append(set([(0,2), (1,1), (2,0)]))

        return winning_combos

    def generate_bot_move(self):
        '''Returns the computer selected row, col'''
        selections = defaultdict(list)
        if self.bot_level == 1:  # Easy - Pick any one from valid_choices list
            selected_item = random.choice(self.game_choices)
        elif self.bot_level == 2:  # Hard - Try to block the player from winning
            for win_set in self.winning_combos:
                rem_items = list(win_set - self.player_a_choices - self.player_b_choices)
                selections[len(rem_items)].append(rem_items)
            if selections.get(1):
                selected_item = random.choice(random.choice(selections[1]))
            elif selections.get(2):
                selected_item = random.choice(random.choice(selections[2]))
            else:
                selected_item = random.choice(random.choice(selections[3]))
        return selected_item

    def print_positions(self):
        '''Returns None.  Prints the current Positions'''
        print('  | 0 | 1 | 2 |')
        print('---------------')
        for row in range(3):
            print(row, end=' |')
            for col in range(3):
                if (row, col) in self.player_a_choices:
                    print('', self.player_a_marker, end=' |')
                elif (row, col) in self.player_b_choices:
                    print('', self.player_b_marker, end=' |')
                else:
                    print('   ', end='|')
            print('')

    def check_winning_combinations(self, player_choices):
        '''Returns True if Player has a winning combination'''
        for win_set in self.winning_combos:
            if win_set.issubset(player_choices):
                return True
        return False

    def check_game_draw(self):
        if self.game_result == "" and self.game_choices:
            return False
        return True

    def _get_player_choices(self, player_marker):
        if player_marker == self.player_a_marker:
            return self.player_a_choices
        else:
            return self.player_b_choices

    def _record_player_move(self, player_marker, selected_item):

        if not self.is_game_on():
            raise InvalidMoveError("Game is not On.  Cannot record a move.")

        # Verify that selected item is a valid selection
        if selected_item not in self.game_choices:
            raise InvalidMoveError("Not one of the valid open positions")

        player_choices = self._get_player_choices(player_marker)
        player_choices.add(selected_item)
        item_idx = self.game_choices.index(selected_item)
        self.game_choices = self.game_choices[:item_idx] + self.game_choices[item_idx+1:]

        if self.check_winning_combinations(player_choices):
            self.game_result = player_marker

        elif self.check_game_draw():
            self.game_result = "D"

    def record_player_a_move(self, selected_item):
        self._record_player_move(self.player_a_marker, selected_item)

        # Make BOT Move if game has not ended
        if self.play_bot and self.has_ended() is False:
            bot_selection = self.generate_bot_move()
            self._record_player_move(self.player_b_marker, bot_selection)


    def record_player_b_move(self, selected_item):
        self._record_player_move(self.player_b_marker, selected_item)
