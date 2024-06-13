from enum import *
import random
from typing import Literal
from TypePrint import typePrint

class Items(Enum):
    HAND_SAW = 0
    CIGARETTES = 1
    BEER = 2
    MAGNIFYING_GLASS = 3

class ValidMoves(Enum):
    SHOOT_D = 0
    SHOOT_P = 1
    USE_HAND_SAW = 2
    USE_CIGARETTES = 3
    USE_BEER = 4
    USE_MAGNIFYING_GLASS = 5
    NO_MOVE = -1


class Buckshot:
    def __init__(
        self,
        round: int, # The round 
        player_items: list, # The player's items
        dealer_items: list, # The dealer's items
        player_turn: bool, # Whose turn it is
    ):
        self.round = round
        self.charges = round * 2 # round 1: 2, round 2: 4, round 3: 6
        self.player_health = round * 2 # round 1: max HP = 2, round 2: max HP = 4, round 3: max HP = 6
        self.player_items = player_items
        self.num_lives_bullet = 0
        self.num_blanks_bullet = 0
        self.current_bullet = None
        self.dealer_health = round * 2 # round 1: max HP = 2, round 2: max HP = 4, round 3: max HP = 6
        self.dealer_items = dealer_items
        self.player_turn = player_turn
        self.gun_is_sawed = False
        self.player_sudden_death = False
        self.dealer_sudden_death = False
        self.loaded_shells = self.loadedShells()
    
    def loadedShells(self) -> list[Literal["live", "blank"] | None]:
        # Generating 2 random numbers that the sum of them can be maximum 8. Each number has to be minimum 1 and maximum 8.
        while True:
            # self.num_lives_bullet, self.num_blanks_bullet = (random.randint(1, 8), random.randint(1, 8)) if self.round > 1 else (random.randint(1, 2), random.randint(1, 2))
            self.num_lives_bullet, self.num_blanks_bullet = (random.randint(1, 8), random.randint(1, 8)) if self.round > 1 else (2, 1)
            if self.num_lives_bullet + self.num_blanks_bullet <= 8:
                break
        shells = ["live"] * self.num_lives_bullet + ["blank"] * self.num_blanks_bullet
        def custom_shuffle(lst):
            n = len(lst)
            for i in range(n - 1, 0, -1):
                j = random.randint(0, i)
                lst[i], lst[j] = lst[j], lst[i]
        custom_shuffle(shells)
        shells += [None] * (8 - len(shells))
        return shells
    
    def reload(self):
        self.loaded_shells = self.loadedShells()
    
    
    def get_all_actions(self):
        all_actions = []
        
        
        current_items = self.player_items if self.player_turn else self.dealer_items
    
        if Items.BEER in current_items:
            all_actions += [ValidMoves.USE_BEER]
        if Items.CIGARETTES in current_items:
            all_actions += [ValidMoves.USE_CIGARETTES]
        if Items.HAND_SAW in current_items and self.gun_is_sawed == False:
            all_actions += [ValidMoves.USE_HAND_SAW]
        if Items.MAGNIFYING_GLASS in current_items:
            all_actions += [ValidMoves.USE_MAGNIFYING_GLASS]
        
            
        if self.num_lives_bullet + self.num_blanks_bullet > 0:
            all_actions += [ValidMoves.SHOOT_D, ValidMoves.SHOOT_P]
        
        return all_actions
    
    def move(self, move: ValidMoves):
        match move:
            case ValidMoves.SHOOT_D:
                try:
                    round = self.loaded_shells.pop(0)
                except IndexError:
                    pass
                if round == "live":
                    if self.dealer_sudden_death:
                        self.dealer_health = 0
                        self.player_turn = not self.player_turn
                    else:
                        self.dealer_health -= 1 if not self.gun_is_sawed else 2
                        self.dealer_health = max(0, self.dealer_health)
                        self.num_lives_bullet -= 1
                        self.player_turn = not self.player_turn # After each shot, it is the other player's turn
                elif round == "blank":
                    self.current_bullet = None
                    self.gun_is_sawed = False
                    self.num_blanks_bullet -= 1
                    self.player_turn = not self.player_turn
            
            
            case ValidMoves.SHOOT_P:
                try:
                    round = self.loaded_shells.pop(0)
                except IndexError:
                    pass
                if round == "live":
                    if self.player_sudden_death:
                        self.player_health = 0
                        self.player_turn = not self.player_turn
                    else:
                        self.player_health -= 1 if not self.gun_is_sawed else 2
                        self.player_health = max(0, self.player_health)
                        self.num_lives_bullet -= 1
                        self.player_turn = not self.player_turn # After each shot, it is the other player's turn
                elif round == "blank":
                    self.current_bullet = None
                    self.gun_is_sawed = False
                    self.num_blanks_bullet -= 1
                    self.player_turn = not self.player_turn
                
                
            case ValidMoves.USE_BEER:
                try:
                    current = self.loaded_shells.pop(0)
                except IndexError:
                    pass
                self.remove_item(Items.BEER)
                self.current_bullet = None
                match current:
                    case "live":
                        self.num_lives_bullet -= 1
                    case "blank":
                        self.num_blanks_bullet -= 1
                
            
            case ValidMoves.USE_MAGNIFYING_GLASS:
                self.current_bullet = self.loaded_shells[0]
                self.remove_item(Items.MAGNIFYING_GLASS)
                
            
            case ValidMoves.USE_CIGARETTES:
                if self.player_turn:
                    self.player_health += 1
                    if self.player_health > self.charges:
                        self.player_health = self.charges
                else:
                    self.dealer_health += 1
                    if self.dealer_health > self.charges:
                        self.dealer_health = self.charges
                
                
                self.remove_item(Items.CIGARETTES)
                
                
            case ValidMoves.USE_HAND_SAW:
                if self.gun_is_sawed: return None
                
                self.remove_item(Items.HAND_SAW)
                
                self.gun_is_sawed = True
                
                
    
    def remove_item(self, item: Items):
        if self.player_turn:
            self.player_items.remove(item)
        else:
            self.dealer_items.remove(item)


    def isEnd(self):
        return self.player_health == 0 or self.dealer_health == 0

