import chess
import chess.engine

from api import get_opening_info, get_tablebase_result
from options import ENGINE_PATH
from constants import PIECE_VALUES


def count_pieces(fen):
    # Extract the piece placement part of the FEN string
    pieces_part = fen.split(' ')[0]
    total_pieces = 0

    # Iterate through each character in the pieces part
    for char in pieces_part:
        if char.isalpha():
            # Increment the count for the piece type
            total_pieces += 1

    return total_pieces


def count_material(fen):
    # Extract the piece placement part of the FEN string
    pieces_part = fen.split(' ')[0]
    white_material = 0
    black_material = 0

    # Iterate through each character in the pieces part
    for char in pieces_part:
        if char.isalpha():
            # Increment the count for the piece type
            if char.isupper():
                white_material += PIECE_VALUES[char]
            else:
                black_material += PIECE_VALUES[char.upper()]

    return white_material, black_material


def get_evaluation(board, engine_depth=None, engine_time=0.1):
    with chess.engine.SimpleEngine.popen_uci(ENGINE_PATH) as engine:
        # Calculate and add position evaluation to the comment
        if engine_depth:
            result = engine.analyse(board, chess.engine.Limit(depth=engine_depth))
        else:
            result = engine.analyse(board, chess.engine.Limit(time=engine_time))
        eval_score = result["score"].relative.score(mate_score=10000) / 100
        if board.turn == chess.BLACK:
            eval_score = -eval_score

    return eval_score


def position_comment(node):
    if "Comment: " in node.comment:
        return node.comment.split("Comment: [")[1].split("]")[0]
    else:
        if node.comment:
            comment = node.comment
            node.comment = f"Comment: [{comment}]"
            return comment
        else:
            return None
    

def position_info(node, write=False):
    if "ECO: " in node.comment and "Name: " in node.comment:
        return node.comment.split("ECO: [")[1].split("]")[0], node.comment.split("Name: [")[1].split("]")[0]
    else:
        result = get_opening_info(node.board().fen())
        if result == None:
            return None
        else:
            eco, opening, _, _, _ = result

        # Add opening to the comment of the node
        if write:
            if node.comment:
                node.comment += f', ECO: [{eco}], Name: [{opening}]'
            else:
                node.comment = f'ECO: [{eco}], Name: [{opening}]'     

        return eco, opening


def position_evaluation(node, write=False, engine_depth=None, engine_time=0.1):
    if "Eval: " in node.comment:
        return float(node.comment.split("Eval: [")[1].split("]")[0])
    else:
        if count_pieces(node.board().fen()) <= 7:
            result = get_tablebase_result(node.board().fen())
            if result == "win":
                if node.board().turn == chess.WHITE:
                    eval_score = 100
                else:
                    eval_score = -100
            elif result == "draw" or result == "cursed-win" or result == "blessed-loss":
                eval_score = 0
            elif result == "loss":
                if node.board().turn == chess.WHITE:
                    eval_score = -100
                else:
                    eval_score = 100
            else:
                eval_score = get_evaluation(node.board(), engine_depth=engine_depth, engine_time=engine_time)
        eval_str = f"{float(eval_score):.2f}"

        # Add eval to the comment for the node
        if write:
            if node.comment:
                node.comment += f', Eval: [{eval_str}]'
            else:
                node.comment = f'Eval: [{eval_str}]'

        return eval_score


