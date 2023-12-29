from io import StringIO
import chess
import chess.pgn

from position_analysis import position_name, evaluation
from move_analysis import move_score, move_info, move_tag


def game_analysis(pgn_string, engine_depth=None, engine_time=0.1):
    # Load the PGN
    game = chess.pgn.read_game(StringIO(pgn_string))

    # Iterate through the moves in the game
    for node in game.mainline():
        # Add position information to the game object
        position_name(node, write=True)
        evaluation(node, write=True, engine_depth=engine_depth, engine_time=engine_time)

        # Add move information to the game object
        move_info(node, write=True)
        move_score(node, write=True, engine_depth=engine_depth, engine_time=engine_time)
        move_tag(node, write=True, engine_depth=engine_depth, engine_time=engine_time)

    return game
