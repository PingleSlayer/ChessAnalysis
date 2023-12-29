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
