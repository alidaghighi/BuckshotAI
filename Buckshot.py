from enum import *
import random
from typing import Literal

class Items(Enum):
    HANDCUFFS = 0
    HAND_SAW = 1
    CIGARETTES = 2
    BEER = 3
    MAGNIFYING_GLASS = 4

class ValidMoves(Enum):
    SHOOT_D = 0
    SHOOT_P = 1
    USE_HANDCUFFS = 2
    USE_HAND_SAW = 3
    USE_CIGARETTES = 4
    USE_BEER = 5
    USE_MAGNIFYING_GLASS = 6
    NO_MOVE = -1

    
    
class InvalidMoveError(Exception):
    print("Invalid move attempted")


class Buckshot:
    def __init__(
        self,
        charges: int, # The maximum health 
        player_health: int, # The player's health
        player_items: list, # The player's items
        num_lives_bullet: int, # The number of live bullets
        num_blanks_bullet: int, # The number of blank bullets
        current_bullet: str, # The current bullet in the chamber
        dealer_health: int, # The dealer's health
        dealer_items: list, # The dealer's items
        player_turn: bool, # Whose turn it is
    ):
        self.charges = charges
        self.player_health = player_health
        self.player_items = player_items
        self.num_lives_bullet = num_lives_bullet
        self.num_blanks_bullet = num_blanks_bullet
        self.current_bullet = current_bullet
        self.dealer_health = dealer_health
        self.dealer_items = dealer_items
        self.player_turn = player_turn
        self.handcuffed = 0 # 0 = not handcuffed, 1 = handcuffed and will remove next turn, 2 = handcuffed and will skip next turn
        self.gun_is_sawed = False
        self.live_probability = 1
        self.blank_probability = 0
        self.loaded_shells = self.loadedShells()
    
    def loadedShells(self) -> list[Literal["live", "blank"] | None]:
        # print(self.num_lives_bullet, self.num_blanks_bullet)
        shells = ["live"] * self.num_lives_bullet + ["blank"] * self.num_blanks_bullet
        def custom_shuffle(lst):
            n = len(lst)
            for i in range(n - 1, 0, -1):
                j = random.randint(0, i)
                lst[i], lst[j] = lst[j], lst[i]
        custom_shuffle(shells)
        shells += [None] * (8 - len(shells))
        return shells
    
    def get_all_actions(self):
        all_actions = []
        
        
        current_items = self.player_items if self.player_turn else self.dealer_items
    
        if Items.BEER in current_items:
            all_actions += [ValidMoves.USE_BEER]
        if Items.CIGARETTES in current_items:
            all_actions += [ValidMoves.USE_CIGARETTES]
        if Items.HANDCUFFS in current_items and self.handcuffed == 0:
            all_actions += [ValidMoves.USE_HANDCUFFS]
        if Items.HAND_SAW in current_items and self.gun_is_sawed == False:
            all_actions += [ValidMoves.USE_HAND_SAW]
        if Items.MAGNIFYING_GLASS in current_items:
            all_actions += [ValidMoves.USE_MAGNIFYING_GLASS]
        
            
        if self.player_turn:
            all_actions += [ValidMoves.SHOOT_D, ValidMoves.SHOOT_P]
        else:
            all_actions += [ValidMoves.SHOOT_P, ValidMoves.SHOOT_D]
        
        return all_actions
    
    def move(self, move: ValidMoves):
        if move not in self.get_all_actions(): 
            err = f"{move} not possible"
            raise InvalidMoveError(err)
        
        
        match move:
            case ValidMoves.SHOOT_D:
                round = self.loaded_shells.pop(0)
                if round == "live":
                    self.dealer_health -= 1 if not self.gun_is_sawed else 2
                    self.dealer_health = max(0, self.dealer_health)
                    if self.handcuffed > 0: # Decrement turns left until next handcuff
                        self.handcuffed -= 1
                    else:
                        self.player_turn = False if self.player_turn else True # If the player shoots dealer with a live, it is not the players turn. If the dealer shoots themselves with a live, it is the players turn.
                elif round == "blank":
                    self.current_bullet = None
                    self.gun_is_sawed = False
                elif round == None:
                    if self.num_blanks_bullet > self.num_lives_bullet:
                        self.num_lives_bullet += 1
                    else:
                        self.num_blanks_bullet += 1
                    self.current_bullet = None
                    self.loaded_shells = self.loadedShells()
                    self.move(ValidMoves.SHOOT_D)
            
            
            case ValidMoves.SHOOT_P:
                round = self.loaded_shells.pop(0)
                if round == "live":
                    self.player_health -= 1 if not self.gun_is_sawed else 2
                    self.player_health = max(0, self.player_health)
                    if self.handcuffed > 0: # Decrement turns left until next handcuff
                        self.handcuffed -= 1
                    else:
                        self.player_turn = True if self.player_turn else False # If the player shoots themselves with a live, it is not the players turn. If the dealer shoots the player with a live, it is the players turn.
                elif round == "blank":
                    self.current_bullet = None
                    self.gun_is_sawed = False
                elif round == None:
                    if self.num_blanks_bullet > self.num_lives_bullet:
                        self.num_lives_bullet += 1
                    else:
                        self.num_blanks_bullet += 1
                    self.current_bullet = None
                    self.loaded_shells = self.loadedShells()
                    self.move(ValidMoves.SHOOT_P)
                
                
            case ValidMoves.USE_BEER:
                self.loaded_shells.pop()
                self.remove_item(Items.BEER)
                self.current_bullet = None
                
                
            
            case ValidMoves.USE_MAGNIFYING_GLASS:
                self.current_bullet = self.loaded_shells[0]
                self.remove_item(Items.MAGNIFYING_GLASS)
                
            
            case ValidMoves.USE_CIGARETTES:
                if self.player_turn:
                    self.player_health += 1
                    self.player_health = max(self.charges, self.player_health)
                else:
                    self.dealer_health += 1
                    self.dealer_health = max(self.charges, self.dealer_health)
                
                
                self.remove_item(Items.CIGARETTES)
                
                
            
            case ValidMoves.USE_HANDCUFFS:
                if self.handcuffed: return None
                
                self.remove_item(Items.HANDCUFFS)
                
                self.handcuffed = 2
                
                
                
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

