import time
import random
from Buckshot import *

class Search:
    def __init__(self):
        pass
        
    def obvious_moves(game: Buckshot):
        
        # obvious moves
    # |------------- Condition ------------- | ------------- Move ------------- |
    # | Is the shell live, does the current  | Use the hand saw                 |
    # | player have a hand saw, and is the   |                                  |
    # | other player's health equal to 2?    |                                  |
    # |--------------------------------------|----------------------------------|
    # | Is the shell live and the current    | Shoot the other player           |  
    # | player does not have a hand saw?     |                                  |
    # |--------------------------------------|----------------------------------|
    # | Is the shell blank? Shoot self       | Use the magnifying glass         |
    # | Does the current player have a       |                                  |
    # | magnifying glass, and is the current |                                  | 
    # | shell unknown?                       |                                  |
    # |--------------------------------------|----------------------------------|
    # | Is the current player not on maximum | Use cigarettes                   |
    # | health?                              |                                  |
    # |--------------------------------------|----------------------------------|
    # | Is there more than 2 shells in the   | Use handcuffs                    |
    # | gun, with at least one blank shell?  |                                  |
    # |--------------------------------------|----------------------------------|

        if game.current_bullet == "live" and game.dealer_items == Items.HAND_SAW and game.dealer_health == 2:
            return ValidMoves.USE_HAND_SAW
        elif game.current_bullet == "live" and Items.HAND_SAW not in game.dealer_items:
            return ValidMoves.SHOOT_P
        elif game.current_bullet == "blank":
            return ValidMoves.SHOOT_D
        elif game.current_bullet == None and Items.MAGNIFYING_GLASS in game.dealer_items:
            return ValidMoves.USE_MAGNIFYING_GLASS
        elif game.player_health < 4 and Items.CIGARETTES in game.dealer_items:
            return ValidMoves.USE_CIGARETTES
        elif len(game.loaded_shells) > 2 and game.num_blanks_bullet > 0 and Items.HANDCUFFS in game.dealer_items:
            return ValidMoves.USE_HANDCUFFS
        else:
            return random.choice(game.get_all_actions())    
        
        
    def minimax(game: Buckshot, depth: int, maximizingPlayer: bool):
        if depth == 0 or game.isEnd():
            return game.evaluate()
        
        if maximizingPlayer:
            maxEval = float('-inf')
            for action in game.get_all_actions():
                new_game = game.copy()
                new_game.move(action)
                eval = Search.minimax(new_game, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float('inf')
            for action in game.get_all_actions():
                new_game = game.copy()
                new_game.move(action)
                eval = Search.minimax(new_game, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval
