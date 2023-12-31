MOVE_TAG_BOUNDARIES = {
    "Winning": 0.5,  
    "Miss 1": -1.5,  
    "Miss 2": -1.5,  
    "Best": 0,  
    "Excellent": -0.05,  
    "Good": -0.1, 
    "Decent": -0.25, 
    "Okay": -0.5, 
    "Suboptimal": -1,
    "Inaccurate": -1.5,  
    "Ineffective": -2,   
    "Dubious": -3,   
    "Reasonable": -0.5,   
    "Inconsistent": -1,   
    "Weak": -1.5,   
    "Error": -2,  
    "Fumble": -3, 
    "Ok": -0.5,  
    "Misstep": -1,    
    "Questionable": -1.5,   
    "Subpar": -2,   
    "Bad": -3,   
    "Blunder": -5,   
    "Disaster": -9,   
}

PIECE_NAMES = {
    "K": "King",
    "Q": "Queen",
    "R": "Rook",
    "B": "Bishop",
    "N": "Knight",
    "P": "Pawn" 
}

PIECE_VALUES = {
    "King": 0,
    "Queen": 9,
    "Rook": 5,
    "Bishop": 3,
    "Knight": 3,
    "Pawn": 1 
}

MATE_SCORE = 10000


