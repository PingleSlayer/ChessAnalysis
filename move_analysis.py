import chess

from position_analysis import position_name, position_evaluation
from constants import MOVE_TAG_BOUNDARIES


def move_info(node, write=False):
    if node.parent == None:
        return None
    # Get UCI
    if "UCI: "  in node.comment:
        uci = node.comment.split("UCI: [")[1].split("]")[0]
    else:
        uci = node.move
        if write:
            if node.comment:
                node.comment += f', UCI: [{f"{uci}"}]'
            else:
                node.comment = f'UCI: [{f"{uci}"}]'
    # Get piece
    if "Piece: " in node.comment:
        moved_piece = node.comment.split("Piece: [")[1].split("]")[0]
    else:
        moved_piece = chess.piece_name(node.parent.board().piece_at(node.move.from_square).piece_type)
        if write:
            if node.comment:
                node.comment += f', Piece: [{f"{moved_piece}"}]'
            else:
                node.comment = f'Piece: [{f"{moved_piece}"}]'
    # Get captured piece
    if "Capture: " in node.comment:
        captured_piece = node.comment.split("Capture: [")[1].split("]")[0]
    else:
        if node.parent.board().is_capture(node.move):
            if node.parent.board().is_en_passant(node.move):
                captured_piece = "pawn"  # En passant capture involves capturing a pawn
            else:
                captured_piece = chess.piece_name(node.parent.board().piece_at(node.move.to_square).piece_type)
            
            if write:
                if node.comment:
                    node.comment += f', Capture: [{f"{captured_piece}"}]'
                else:
                    node.comment = f'Capture: [{f"{captured_piece}"}]'
        else:
            captured_piece = None
    # Get promotion piece
    if "Promotion: " in node.comment:
        promotion_piece = node.comment.split("Promotion: [")[1].split("]")[0]
    else:
        if node.move.promotion:
            promotion_piece = chess.piece_name(node.move.promotion)
            if write:
                if node.comment:
                    node.comment += f', Promotion: [{f"{promotion_piece}"}]'
                else:
                    node.comment = f'Promotion: [{f"{promotion_piece}"}]'
        else:
            promotion_piece = None

    return uci, moved_piece, captured_piece, promotion_piece


def move_score(node, write=False, engine_depth=None, engine_time=0.1):
    if node.parent == None:
        return None
    if "Move score: " in node.comment:
        return float(node.comment.split("Move score: [")[1].split("]")[0])
    else:
        if "Eval: " not in node.parent.comment:
            og_eval = position_evaluation(node.parent, write=write, engine_depth=engine_depth, engine_time=engine_time)
        else:
            og_eval = float(node.parent.comment.split("Eval: [")[1].split("]")[0])
        if "Eval: " not in node.comment:
            new_eval = position_evaluation(node, write=write, engine_depth=engine_depth, engine_time=engine_time)
        else:
            new_eval = float(node.comment.split("Eval: [")[1].split("]")[0])

        if node.board().turn == chess.BLACK:
            move_score = new_eval - og_eval
        else:
            move_score = og_eval - new_eval

        # Add move score to the comment for the node
        if write:
            if node.comment:
                node.comment += f', Move score: [{f"{float(move_score):.2f}"}]'
            else:
                node.comment = f'Move score: [{f"{float(move_score):.2f}"}]'

        return move_score


def move_tag(node, write=False, engine_depth=None, engine_time=0.1):
    if node.parent == None:
        return None
    if "Move tag: " in node.comment:
        return node.comment.split("Tag: [")[1].split("]")[0]
    else:
        eval = position_evaluation(node, write=write, engine_depth=engine_depth, engine_time=engine_time)
        relative_eval = eval * (1 if node.board().turn == chess.WHITE else -1)
        og_move_score = move_score(node.parent, write=write, engine_depth=engine_depth, engine_time=engine_time)
        new_move_score = move_score(node, write=write, engine_depth=engine_depth, engine_time=engine_time)

        # Check for book move
        if position_name(node, write=write) != "Not Theory":
            tag = "Book"
        # Check for forced move
        elif len(list(node.parent.board().legal_moves)) == 1:
            tag = "Forced"
        # Check for miss
        elif og_move_score is not None and og_move_score <= MOVE_TAG_BOUNDARIES["Miss 1"] and new_move_score <= MOVE_TAG_BOUNDARIES["Miss 2"]:
            tag = "Miss"
        # Check for good move
        elif new_move_score >= MOVE_TAG_BOUNDARIES["Decent"]:
            if new_move_score >= MOVE_TAG_BOUNDARIES["Best"]:
                tag = "Best"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Excellent"]:
                tag = "Excellent"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Good"]:
                tag = "Good"
            else:
                tag = "Decent"
        # Check for suboptimal winning move
        elif relative_eval >= MOVE_TAG_BOUNDARIES["Winning"]:
            if new_move_score >= MOVE_TAG_BOUNDARIES["Okay"]:
                tag = "Okay"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Suboptimal"]:
                tag = "Suboptimal"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Inaccurate"]:
                tag = "Inaccurate"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Ineffective"]:
                tag = "Ineffective"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Dubious"]:
                tag = "Dubious"
            else:
                tag = "Blunder"
        # Check for suboptimal not losing move
        elif relative_eval >= -MOVE_TAG_BOUNDARIES["Winning"]:
            if new_move_score >= MOVE_TAG_BOUNDARIES["Reasonable"]:
                tag = "Reasonable"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Inconsistent"]:
                tag = "Inconsistent"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Weak"]:
                tag = "Weak"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Error"]:
                tag = "Error"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Fumble"]:
                tag = "Fumble"
            else:
                tag = "Blunder"
        # Check for losing move
        else:
            if new_move_score >= MOVE_TAG_BOUNDARIES["Ok"]:
                tag = "Ok"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Misstep"]:
                tag = "Misstep"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Questionable"]:
                tag = "Questionable"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Subpar"]:
                tag = "Subpar"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Bad"]:
                tag = "Bad"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Blunder"]:
                tag = "Blunder"
            elif new_move_score >= MOVE_TAG_BOUNDARIES["Disaster"]:
                tag = "Disaster"
            else:
                tag = "Catastrophe"

        # Add move classification to the comment for the node
        if write:
            if node.comment:
                node.comment += f', Move Tag: [{tag}]'
            else:
                node.comment = f'Move Tag: [{tag}]'

    return tag
