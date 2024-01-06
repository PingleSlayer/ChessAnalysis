import chess

from constants import MOVE_TAG_BOUNDARIES


class Move_Analyzer:

    def __init__(self, old_node, new_node):
        self.old_node = old_node
        self.new_node = new_node