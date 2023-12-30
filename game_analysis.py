from io import StringIO
import chess
import chess.pgn

from position_analysis import position_comment, position_name, position_evaluation
from move_analysis import move_score, move_info, move_tag


def game_accuracy(game, write=False, engine_depth=None, engine_time=0.1):
    total_white_move_score = 0
    total_white_moves = 0
    total_black_move_score = 0
    total_black_moves = 0
    
    og_comments = []
    # Iterate through the moves in the game to calculate average move score
    for node in game.mainline():
        if not write:
            og_comments.append(node.comment)
        if node.board().turn == chess.BLACK:
            total_white_move_score += move_score(node, write=True, engine_depth=engine_depth, engine_time=engine_time)
            total_white_moves += 1
        else:
            total_black_move_score += move_score(node, write=True, engine_depth=engine_depth, engine_time=engine_time)
            total_black_moves += 1

    avg_white_move_score = total_white_move_score / total_white_moves
    avg_black_move_score = total_black_move_score / total_black_moves

    total_white_deviation = 0
    total_black_deviation = 0
    # Iterate through the moves in the game to calculate standard deviation
    for node in game.mainline():
        if node.board().turn == chess.BLACK:
            total_white_deviation += pow((move_score(node, write=True, engine_depth=engine_depth, engine_time=engine_time) - avg_white_move_score),2)
        else:
            total_black_deviation += pow((move_score(node, write=True, engine_depth=engine_depth, engine_time=engine_time) - avg_black_move_score),2)

    stdev_white_move_score = total_white_deviation / total_white_moves
    stdev_black_move_score = total_black_deviation / total_black_moves

    # Delete from pgn        
    if not write:
        for i, node in enumerate(game.mainline()):
            node.comment = og_comments[i]

    return avg_white_move_score, stdev_white_move_score, avg_black_move_score, stdev_black_move_score


def game_analysis(pgn_string, write=False, engine_depth=None, engine_time=0.1):
    # Load the PGN
    game = chess.pgn.read_game(StringIO(pgn_string))
    og_comments = []
    # Iterate through the moves in the game
    for node in game.mainline():
        if not write:
            og_comments.append(node.comment)
        # Add position information to the game object
        position_comment(node)
        print(position_name(node, write=True))
        position_evaluation(node, write=True, engine_depth=engine_depth, engine_time=engine_time)

        # Add move information to the game object
        move_info(node, write=True)
        move_score(node, write=True, engine_depth=engine_depth, engine_time=engine_time)
        move_tag(node, write=True, engine_depth=engine_depth, engine_time=engine_time)

    avg_white_move_score, stdev_white_move_score, avg_black_move_score, stdev_black_move_score = game_accuracy(game, write=True)

    print(f"White -> avg move score: {avg_white_move_score}, stdev: {stdev_white_move_score}\n")
    print(f"Black -> avg move score: {avg_black_move_score}, stdev: {stdev_black_move_score}\n")
    
    # Delete from pgn
    if not write:
        for i, node in enumerate(game.mainline()):
            node.comment = og_comments[i]

    return game

