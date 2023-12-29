import chess

from position_analysis import position_name, evaluation


def move_info(node, write=False):
    if node.parent == None:
        return None
    if "UCI: "  in node.comment:
        uci = node.comment.split("UCI: [")[1].split("]")[0]
    else:
        uci = node.move
        if write:
            if node.comment:
                node.comment += f', UCI: [{f"{uci}"}]'
            else:
                node.comment = f'UCI: [{f"{uci}"}]'
    if "Piece: " in node.comment:
        moved_piece = node.comment.split("Piece: [")[1].split("]")[0]
    else:
        moved_piece = chess.piece_name(node.parent.board().piece_at(node.move.from_square).piece_type)
        if write:
            if node.comment:
                node.comment += f', Piece: [{f"{moved_piece}"}]'
            else:
                node.comment = f'Piece: [{f"{moved_piece}"}]'
    if "Capture: " in node.comment:
        captured_piece = node.comment.split("Capture: [")[1].split("]")[0]
    else:
        if node.board().is_capture(node.move):
            captured_piece = chess.piece_name(node.parent.board().piece_at(node.move.to_square).piece_type)
            if write:
                if node.comment:
                    node.comment += f', Capture: [{f"{captured_piece}"}]'
                else:
                    node.comment = f'Capture: [{f"{captured_piece}"}]'
        else:
            captured_piece = None
        
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
            og_eval = evaluation(node.parent, write=write, engine_depth=engine_depth, engine_time=engine_time)
        else:
            og_eval = float(node.parent.comment.split("Eval: [")[1].split("]")[0])
        if "Eval: " not in node.comment:
            new_eval = evaluation(node, write=write, engine_depth=engine_depth, engine_time=engine_time)
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
        eval = evaluation(node, write=write, engine_depth=engine_depth, engine_time=engine_time)
        og_move_score = move_score(node.parent, write=write, engine_depth=engine_depth, engine_time=engine_time)
        new_move_score = move_score(node, write=write, engine_depth=engine_depth, engine_time=engine_time)
    
        # Check for a Book move
        if position_name(node, write=write) != "Not Theory":
            tag = "Book"
        # Check for a Forced move
        elif len(list(node.parent.board().legal_moves)) == 1:
            tag = "Forced"
        # Check for a Miss
        elif og_move_score is not None and og_move_score <= -1.5 and new_move_score <= -1.5:
            tag = "Miss"
        elif new_move_score >= 0:
            tag = "Best"
        elif new_move_score >= -0.05:
            tag = "Excellent"
        elif new_move_score >= -0.1:
            tag = "Nice"
        elif new_move_score >= -0.25:
            tag = "Good"
        elif new_move_score >= -0.5 and eval * (1 if node.board().turn == chess.BLACK else -1) <= -0.5:
            tag = "Ok"
        elif new_move_score >= -1 and eval * (1 if node.board().turn == chess.BLACK else -1) <= -0.5:
            tag = "Inaccurate"
        elif new_move_score >= -2.5 and eval * (1 if node.board().turn == chess.BLACK else -1) <= -0.5:
            tag = "Questionable"
        elif eval * (1 if node.board().turn == chess.BLACK else -1) <= 0:
            tag = "Dubious"
        elif new_move_score >= -0.5:
            tag = "Decent"
        elif new_move_score >= -1:
            tag = "Inaccurate"
        elif new_move_score >= -2:
            tag = "Wrong"
        elif new_move_score >= -3:
            tag = "Mistake"
        elif new_move_score >= -5:
            tag = "Blunder"
        elif new_move_score >= -9:
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
