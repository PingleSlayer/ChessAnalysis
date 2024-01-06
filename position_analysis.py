import chess
import chess.engine
import chess.pgn

from helpfunctions import get_opening_data, get_tablebase_result
from options import ENGINE_PATH
from constants import PIECE_VALUES, PIECE_NAMES, MATE_SCORE


class Position_Analyzer:

    def __init__(self, node):
        self.node = node
        self.board = node.board()
        self.fen = self.board.fen()

    def analysis(self, engine_time=0.1, computer_lines=None, mode=0):
        self.opening_analysis()
        self.engine_analysis(engine_time=engine_time, computer_lines=computer_lines)
        self.advantage_analysis()
        self.space_analysis()
        self.development_analysis()
        self.initiative_analysis()
        self.material_analysis()
        self.control_analysis()
        self.kingsafety_analysis()
        self.pawnstructure_analysis()
        self.pieceplacement_analysis()
        self.piececoordination_analysis()

    # Add opening information
    def opening_analysis(self):
        opening_data = get_opening_data(self.fen)
        if opening_data:
            eco = opening_data[0]
            name = opening_data[1]
            white = opening_data[2]
            draw = opening_data[3]
            black = opening_data[4]

            if eco and name:
                self.node.comment += f' [%opening {eco},{name}]'

            if white and draw and black:
                self.node.comment += f' [%wdb {white},{draw},{black}]'

    # Add evaluation (+ engine lines)
    def engine_analysis(self, engine_time=0.1, computer_lines=None):
        with chess.engine.SimpleEngine.popen_uci(ENGINE_PATH) as engine:
            if computer_lines:
                result = engine.analyse(self.board, chess.engine.Limit(time=engine_time), multipv=computer_lines)
                pov_scores = [info["score"] for info in result]
                depths = [info["depth"] for info in result]
                self.node.set_eval(pov_scores[0], depths[0])

                # Add engine lines as variations
                for i, variation_info in enumerate(result):
                    if "pv" in variation_info:
                        variation_moves = variation_info["pv"]
                        var_node = self.node
                        var_node = var_node.add_line(variation_moves, comment=f"Engineline ({i + 1}/{len(result)})")
                        var_node.set_eval(variation_info['score'], variation_info['depth'])
            else:
                result = engine.analyse(self.board, chess.engine.Limit(time=engine_time))
                pov_score = result["score"]
                depth = result["depth"]
                self.node.set_eval(pov_score, depth)

    # Add NAGs $10-$23
    def advantage_analysis(self):
        pov_eval = self.node.eval()
        if pov_eval is None:
            return
        eval = pov_eval.white().score(mate_score=MATE_SCORE)/100
        relative_eval = pov_eval.relative.score(mate_score=MATE_SCORE)/100
        
        if not self.board.is_check():
            with chess.engine.SimpleEngine.popen_uci(ENGINE_PATH) as engine:
                self.board.push(chess.Move.null())
                null_board = self.board.copy(stack=False)
                result = engine.analyse(null_board, chess.engine.Limit(time=0.1))
                null_relative_eval = result["score"].relative.score(mate_score=MATE_SCORE)/100
                self.board.pop()
                zugzwang_score = -(null_relative_eval + relative_eval)

            if zugzwang_score > 0:
                if self.board.turn == chess.WHITE:
                    self.node.nags.add(22) # White is in zugzwang
                else:
                    self.node.nags.add(23) # Black is in zugzwang

        if abs(eval) < 0.25:
            self.node.nags.add(10) # Drawish position or even
            if zugzwang_score < -5:
                self.node.nags.add(12) # Equal chances, active position
            else:
                self.node.nags.add(11) # Equal chances, quiet position
        elif abs(eval) < 1:
            if eval > 0:
                self.node.nags.add(14) # White has a slight advantage
            else:
                self.node.nags.add(15) # Black has a slight advantage
        elif abs(eval) < 3:
            if eval > 0:
                self.node.nags.add(16) # White has a moderate advantage
            else:
                self.node.nags.add(17) # Black has a moderate advantage
        elif abs(eval) < 9:
            if eval > 0:
                self.node.nags.add(18) # White has a decisive advantage
            else:
                self.node.nags.add(19) # Black has a decisive advantage
        else:
            if eval > 0:
                self.node.nags.add(20) # White has a crushing advantage (Black should resign)
            else:
                self.node.nags.add(21) # Black has a crushing advantage (White should resign)

    # Add NAGs $24-$29
    def space_analysis(self):
        pov_eval = self.node.eval()
        if pov_eval is None:
            return
        eval = pov_eval.white().score(mate_score=MATE_SCORE)/100

        # Count squares attacked by each side using attackers
        white_squares_attacked = 0
        black_squares_attacked = 0

        for square in chess.SQUARES:
            white_squares_attacked += len(self.board.attackers(chess.WHITE, square)) * 0.1
            black_squares_attacked += len(self.board.attackers(chess.BLACK, square)) * 0.1

        # Evaluate pawn advancement
        white_pawn_advancement = sum([square//8 for square in self.board.pieces(chess.PAWN, chess.WHITE)])
        black_pawn_advancement = 7 - sum([square//8 for square in self.board.pieces(chess.PAWN, chess.BLACK)])
        
        # Calculate the final space advantage
        space_advantage = white_squares_attacked + white_pawn_advancement - (black_squares_attacked + black_pawn_advancement)

        if space_advantage > 3:
            if eval > 3 and space_advantage > 5:
                self.node.nags.add(28)  # White has a decisive space advantage
            elif eval > 0.25 and space_advantage > 5:
                self.node.nags.add(26)  # White has a moderate space advantage
            else:
                self.node.nags.add(24)  # White has a slight space advantage
        elif space_advantage < -3:
            if eval < -3 and space_advantage < -5:
                self.node.nags.add(29)  # Black has a decisive space advantage
            elif eval < -0.25 and space_advantage < -5:
                self.node.nags.add(27)  # Black has a moderate space advantage
            else:
                self.node.nags.add(25)  # Black has a slight space advantage

    # Add NAGs $30-$35
    def development_analysis(self):
        pass

    # Add NAGs $36-$41
    def initiative_analysis(self):
        pass
    
    # Add NAGs $42-$47
    def material_analysis(self):
        pass

    # Add NAGs $48-$65    
    def control_analysis(self):
        pass
    
    # Add NAGs $66-$77
    def kingsafety_analysis(self):
        pass

    # Add NAGs $78-$85
    def pawnstructure_analysis(self):
        pass

    # Add NAGs $86-$101
    def pieceplacement_analysis(self):
        pass

    # Add NAGs $102-$105
    def piececoordination_analysis(self):
        pass

