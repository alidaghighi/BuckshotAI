from copy import deepcopy
from Buckshot import *

class Search:
    def __init__(self):
        pass
        
    def obvious_moves(game: Buckshot):
        
    # obvious move
    # |------------- Condition ------------- | ------------- Move ------------- |
    # | Is the shell live, does the current  | Use the hand saw                 |
    # | player have a hand saw, and is the   |                                  |
    # | other player's health equal to 2?    |                                  |
    # |--------------------------------------|----------------------------------|
    # | Is the shell live and the current    | Shoot the other player           |  
    # | player does not have a hand saw?     |                                  |
    # |--------------------------------------|----------------------------------|
    # | Is the shell blank?                  | Shoot self                       |
    # |--------------------------------------|----------------------------------|
    # | Does the current player have a       | Use the magnifying glass         |
    # | magnifying glass, and is the current |                                  | 
    # | shell unknown?                       |                                  |
    # |--------------------------------------|----------------------------------|
    # | Is the current player not on maximum | Use cigarettes                   |
    # | health?                              |                                  |
    # |--------------------------------------|----------------------------------|

        
        if Items.CIGARETTES in game.dealer_items:
            if game.player_turn:
                if game.player_health < game.charges:
                    return ValidMoves.USE_CIGARETTES
            else:
                if game.dealer_health < game.charges:
                    return ValidMoves.USE_CIGARETTES
        elif game.current_bullet == "live" and game.dealer_items == Items.HAND_SAW and game.dealer_health == 2:
            return ValidMoves.USE_HAND_SAW
        elif game.current_bullet == "live" and Items.HAND_SAW not in game.dealer_items:
            return ValidMoves.SHOOT_P
        elif game.current_bullet == "blank":
            return ValidMoves.SHOOT_D
        elif game.current_bullet == None and Items.MAGNIFYING_GLASS in game.dealer_items and game.num_lives_bullet + game.num_blanks_bullet > 1:
            return ValidMoves.USE_MAGNIFYING_GLASS
        else:
            return ValidMoves.NO_MOVE
        
        
    def minimax(game: Buckshot, depth: int, maximizingPlayer: bool):
        if depth == 0 or game.isEnd():
            return Search.gameEvaluation(game)
        
        if maximizingPlayer:
            maxEval = float('-inf')
            for action in game.get_all_actions():
                new_game = deepcopy(game)
                new_game.move(action)
                eval = Search.minimax(new_game, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float('inf')
            for action in game.get_all_actions():
                new_game = deepcopy(game)
                new_game.move(action)
                eval = Search.minimax(new_game, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval


    def minimax_with_pruning(game: Buckshot, depth: int, maximizingPlayer: bool, alpha: int, beta: int):
        if depth == 0 or game.isEnd():
            return Search.gameEvaluation(game)
        
        if maximizingPlayer:
            maxEval = float('-inf')
            for action in game.get_all_actions():
                new_game = deepcopy(game)
                new_game.move(action)
                eval = Search.minimax_with_pruning(new_game, depth - 1, False, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for action in game.get_all_actions():
                new_game = deepcopy(game)
                new_game.move(action)
                eval = Search.minimax_with_pruning(new_game, depth - 1, True, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
        
    def gameEvaluation(game: Buckshot):
        """
        Either one of the players HP is 0 or we are trying to get to the lowest HP possible for the other player
        The number of blanks and lives should be considered
        """
        eval = 0
        if game.player_health == 0:
            eval = float('-inf')
        elif game.dealer_health == 0:
            eval = float('inf')
        
        if game.num_lives_bullet + game.num_blanks_bullet != 0:
            live_prob = game.num_lives_bullet / (game.num_lives_bullet + game.num_blanks_bullet)
            blank_prob = game.num_blanks_bullet / (game.num_lives_bullet + game.num_blanks_bullet)
            if live_prob > blank_prob:
                eval += 1 * (1 if game.player_turn else -1)
            else:
                eval += -1 * (1 if game.player_turn else -1)
        else:
            eval += (game.dealer_health - game.player_health) * (1 if game.player_turn else -1)    
        
        return eval
        
         
    
    def search(game: Buckshot, depth: int, maximizingPlayer: bool):
        blank_prob = game.num_blanks_bullet / (game.num_blanks_bullet + game.num_lives_bullet)
        live_prob = game.num_lives_bullet / (game.num_blanks_bullet + game.num_lives_bullet)
        if live_prob == 1 or blank_prob == 1:
            return ValidMoves.SHOOT_D if blank_prob > live_prob else ValidMoves.SHOOT_P
        move = Search.obvious_moves(game)
        if move != ValidMoves.NO_MOVE:
            return move    
        bestMove = None
        bestValue = float('-inf')
        for action in game.get_all_actions():
            new_game = deepcopy(game)
            new_game.move(action)
            # value = Search.minimax(new_game, depth, maximizingPlayer)
            value = Search.minimax_with_pruning(new_game, depth, maximizingPlayer, float('-inf'), float('inf'))
            if value > bestValue:
                bestValue = value
                bestMove = action
        if bestMove == None:
            bestMove = ValidMoves.SHOOT_D if blank_prob > live_prob else ValidMoves.SHOOT_P
        return bestMove
