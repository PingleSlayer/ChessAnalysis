import chess
import chess.engine

from helpfunctions import load_openings
from options import ENGINE_NAME


# Load the position dictionary
position_dict = load_openings() 


def position_comment(node):
    if "Comment: " in node.comment:
        return node.comment.split("Comment: [")[1].split("]")[0]
    else:
        if node.comment:
            comment = node.comment
        else:
            comment = "None"
        node.comment = f"Comment: [{comment}]"
        return comment
    


def position_name(node, write=False):
    if "Name: " in node.comment:
        return node.comment.split("Name: [")[1].split("]")[0]
    else:
        # Get FEN without the last two integers
        fen_parts = node.board().fen().rsplit(' ', 2)[:-2]
        fen_key = ' '.join(fen_parts)

        # Check if the current FEN is in the opening dictionary
        opening_name = None
        if fen_key in position_dict:
            opening_name = position_dict[fen_key]
        else:
            opening_name = "None"
        
        # Add opening to the comment of the node
        if write:
            if node.comment:
                node.comment += f', Name: [{opening_name}]'
            else:
                node.comment = f'Name: [{opening_name}]'     

        return opening_name


def position_evaluation(node, write=False, engine_depth=None, engine_time=0.1):
    if "Eval: " in node.comment:
        return float(node.comment.split("Eval: [")[1].split("]")[0])
    else:
        engine_path = f"Engine/{ENGINE_NAME}"
        with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
            # Calculate and add position evaluation to the comment
            if engine_depth:
                result = engine.analyse(node.board(), chess.engine.Limit(depth=engine_depth))
            else:
                result = engine.analyse(node.board(), chess.engine.Limit(time=engine_time))
            eval_score = result["score"].relative.score(mate_score=10000) / 100
            if node.board().turn == chess.BLACK:
                eval_score = -eval_score
            eval_str = f"{float(eval_score):.2f}"

            # Add eval to the comment for the node
            if write:
                if node.comment:
                    node.comment += f', Eval: [{eval_str}]'
                else:
                    node.comment = f'Eval: [{eval_str}]'

        return eval_score


