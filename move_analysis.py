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

