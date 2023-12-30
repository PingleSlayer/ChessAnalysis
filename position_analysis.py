import chess
import chess.engine

from api import get_position_info
from options import ENGINE_NAME


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
    

def position_name(node, write=False):
    if "ECO: " in node.comment and "Name: " in node.comment:
        return node.comment.split("ECO: [")[1].split("]")[0], node.comment.split("Name: [")[1].split("]")[0]
    else:
        result = get_position_info(node.board().fen())
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


