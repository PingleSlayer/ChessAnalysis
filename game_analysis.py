from io import StringIO
import chess
import chess.pgn

from position_analysis import position_name, evaluation
from move_analysis import move_score, move_info, move_tag


def game_analysis(pgn_string):
    # Load the PGN
    game = chess.pgn.read_game(StringIO(pgn_string))

    # Iterate through the moves in the game
    for node in game.mainline():
        # Add position information to the game object
        position_name(node, write=True)
        evaluation(node, write=True, engine_time=0.1)

        # Add move information to the game object
        move_info(node, write=True)
        move_score(node, write=True, engine_time=0.1)

    return game
