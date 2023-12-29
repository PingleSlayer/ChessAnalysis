import chess
import chess.engine

from helpfunctions import load_openings


# Load the position dictionary
position_dict = load_openings() 


def position_name(node, write=False):
    if "Name: " in node.comment:
        return node.comment.split("Name: [")[1].split("]")[0]
    else:
        # Get FEN without the last two integers
        fen_parts = node.board().fen().rsplit(' ', 2)[:-2]
        fen_key = ' '.join(fen_parts)

        # Initialize opening_name outside the if block
        opening_name = None

        # Check if the current FEN is in the opening dictionary
        if fen_key in position_dict:
            opening_name = position_dict[fen_key]
            if write:
                if node.comment:
                    node.comment += f', Name: [{opening_name}]'
                else:
                    node.comment = f'Name: [{opening_name}]'
                    
        return opening_name
