from __future__ import print_function  # Python 2, 3 Compatibility
from builtins import input  # Python 2, 3 Compatibility
from src import TicTacToe, InvalidMoveError


def get_bot_level_input():
    while True:
        bot_level = input('Select difficult level (1 - Easy, 2 - Hard): ')
        try:
            bot_level = int(bot_level)
            bot_level = min(max(bot_level, 1), 2)
            break
        except ValueError:
            print("Level needs to be numeric - Enter 1 or 2.  {} is not valid input".format(bot_level))
    print("Entering Bot Level: {}".format(bot_level))
    return bot_level

def get_player_input(valid_selections):
    '''Returns the selected row, col by the Player'''
    selected_item = tuple()
    while selected_item not in valid_selections:
        if selected_item:
            print('Your selection of {} is not valid: '.format(selected_item))
            print("Valid Choices are: {}".format(valid_selections))
        selected_item = tuple(int(val) for val in input('Enter your selection in row, col format:').split(',') if val.isdigit())
    return selected_item

if __name__ == '__main__':
    player_a_marker = "X"
    player_b_marker = "O"
    print('Welcome to a game of Tic-Tac-Toe')
    while True:
        # Start a new Game
        bot_level = get_bot_level_input()
        game = TicTacToe(play_bot=True,
            bot_level=bot_level,
            player_a_marker=player_a_marker,
            player_b_marker=player_b_marker)

        while game.has_ended() is False:
            game.print_positions()
            selected_item = get_player_input(game.get_valid_choices())
            try:
                game.record_player_a_move(selected_item)
            except InvalidMoveError:
                # Move rejected
                print("Move rejected")

        print("-" * 20)
        if game.game_result == player_a_marker:
            print('You Won.  Congratulations!')
        elif game.game_result == player_b_marker:
            print('Bot Wins.  Better luck next time!')
        elif game.game_result == 'D':
            print('Its a Draw.')
        # Print final game positions
        print("-" * 20)
        print("Final Game Positions:", end="\n\n")
        game.print_positions()
        if input('Do you want to play again Y/N: ').strip().upper() == 'N':
            break
