import time
import random
from Buckshot import *

def typePrint(m):
    l = list(m)
    for i in range(0, len(l)):
        print(l[i], end='', flush=True)
        randomTime = random.uniform(0, 1)
        if randomTime < 0.7:
            t = 0.02
        else:
            t = 0.1
        time.sleep(t)
    print()


def displayHelp():
    typePrint("\n+=====================+\n")
    typePrint("This game is based on the actual game 'buckshot roulette'.\nIn a nutshell, this is russian roulette.\nInfo: https://en.wikipedia.org/wiki/Buckshot_Roulette\n")
    typePrint("INSTRUCTIONS:")
    typePrint("    - OBJECTIVE: SURVIVE.")
    typePrint("    - A shotgun is loaded with a disclosed number of bullets, some of which will be blanks.")
    typePrint("    - Participants are given a set amount of lives (default = 4) to survive.")
    typePrint("    - You and 'The Dealer' will take turns shooting.")
    typePrint("    - Aim at The Dealer or at yourself - shooting yourself with a blank skips the Dealers turn.")
    typePrint("    - Participants are given items to help out. Use them wisely.")
    typePrint("    - if you have chosen wrongly, type 'q'/'quit'/'back' to go back.")
    typePrint()
    typePrint("ITEMS:")
    typePrint("    • 🚬 = Gives the user an extra life.")
    typePrint("    • 🍺 = Racks the shotgun and the bullet inside will be discarded.")
    typePrint("    • 🔪 = Shotgun will deal double damage for one turn.")
    typePrint("    • 🔍 = User will see what bullet is in the chamber.")
    typePrint("    • ⛓ = Handcuffs the other person so they miss their next turn.")
    typePrint("\nGood Luck.\n")
    typePrint("+=====================+")
        
def displayItems(items):
    for i in items:
        match i:
            case Items.CIGARETTES:
                typePrint("(c)🚬")
            case Items.BEER:
                typePrint("(b)🍺")
            case Items.HAND_SAW:
                typePrint("(s)🔪")
            case Items.MAGNIFYING_GLASS:
                typePrint("(m)🔍")
            case Items.HANDCUFFS:
                typePrint("(h)⛓")
            case _:
                typePrint("Unknown item.")        

def displayMove(move):
    match move:
        case ValidMoves.USE_CIGARETTES:
            return "Using cigarettes."
        case ValidMoves.USE_BEER:
            return "Using beer."
        case ValidMoves.USE_HAND_SAW:
            return "Using hand saw."
        case ValidMoves.USE_MAGNIFYING_GLASS:
            return "Using magnifying glass."
        case ValidMoves.USE_HANDCUFFS:
            return "Using handcuffs."
        case ValidMoves.SHOOT_D:
            return "Shooting Dealer."
        case ValidMoves.SHOOT_P:
            return "Shooting Player."
        case _:
            return "Unknown move."


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
    
        
def main():
    typePrint("[DEALER]: PLEASE SIGN THE WAIVER.")
    askforhelp = ''

    while askforhelp not in ["a","b"]:
        askforhelp = input("(a) Read Waiver or (b) Sign and continue? ").lower().strip(" ")

    if askforhelp == "a":
        displayHelp()
        input("READY? ")
    name = ""
    while name in ["DEALER"] or not (3 < len(name) < 10):
        if name:
            typePrint("INVALID NAME.")
        name = input("ENTER NAME: ").strip(" ").upper()
    items = [Items.CIGARETTES,Items.MAGNIFYING_GLASS]
    player_turn =  True
    game = Buckshot(
        charges=4,
        player_health=4,
        player_items=items.copy(),
        num_lives_bullet=2,
        num_blanks_bullet=2,
        current_bullet=None,
        dealer_health=4,
        dealer_items=items.copy(),
        player_turn=player_turn,
    )
    while not game.isEnd():
        typePrint("\n\n")
        # typePrint(f"The number of blank bullets: {game.num_blanks_bullet}")
        # typePrint(f"The number of live bullets: {game.num_lives_bullet}")
        typePrint(f"shells: {game.loaded_shells}")
        if player_turn:
            typePrint(f"now it's {name}'s turn: ")
            typePrint(f"Dealer's health: {game.dealer_health}")
            typePrint(f"Your health: {game.player_health}")
            typePrint("====================================")
            time.sleep(0.5)
            typePrint("a) use item")
            typePrint("b) shoot")
            p_choice = input("Choose: ").lower().strip(" ")
            match p_choice:
                case "a":
                    typePrint("Items:")
                    displayItems(game.player_items)
                    item = input("Choose item: ").strip(" ")
                    match item:
                        case "c":
                            game.move(ValidMoves.USE_CIGARETTES)
                        case "b":
                            game.move(ValidMoves.USE_BEER)
                        case "s":
                            game.move(ValidMoves.USE_HAND_SAW)
                            typePrint("Now you deal double damage for one turn.")
                        case "m":
                            game.move(ValidMoves.USE_MAGNIFYING_GLASS)
                            typePrint("You see the bullet in the chamber.")
                            typePrint(f"The bullet is {game.current_bullet}")
                        case "h":
                            game.move(ValidMoves.USE_HANDCUFFS)
                            typePrint("The dealer is handcuffed.")
                        case _:
                            typePrint("Invalid item.")
                            continue
                case "b":
                    typePrint("Who do you want to shoot?")
                    typePrint("a) Dealer")
                    typePrint("b) Yourself")
                    choice = input("Choose: ").lower().strip(" ")
                    if choice == "a":
                        game.move(ValidMoves.SHOOT_D)
                        player_turn = False
                        game.player_turn = player_turn
                    elif choice == "b":
                        game.move(ValidMoves.SHOOT_P)
                    else:
                        typePrint("Invalid choice.")
                        continue
                case "q","quit","back":
                    continue
                case _:
                    typePrint("Invalid choice.")
                    continue
            
        else:
            typePrint("Dealer's turn: ")
            time.sleep(0.5)
            typePrint(f"Dealer's health: {game.dealer_health}")
            typePrint(f"Your health: {game.player_health}")
            typePrint("====================================")
            time.sleep(0.5)
            typePrint("Dealer's items:")
            displayItems(game.dealer_items)
            move = obvious_moves(game)
            typePrint(f"Dealer will {displayMove(move)}")
            time.sleep(0.5)
            match move:
                case ValidMoves.USE_CIGARETTES:
                    game.move(ValidMoves.USE_CIGARETTES)
                case ValidMoves.USE_BEER:
                    game.move(ValidMoves.USE_BEER)
                case ValidMoves.USE_HAND_SAW:
                    game.move(ValidMoves.USE_HAND_SAW)
                    typePrint("Dealer deals double damage for one turn.")
                case ValidMoves.USE_MAGNIFYING_GLASS:
                    game.move(ValidMoves.USE_MAGNIFYING_GLASS)
                    typePrint("Dealer sees the bullet in the chamber.")
                case ValidMoves.USE_HANDCUFFS:
                    game.move(ValidMoves.USE_HANDCUFFS)
                    typePrint("You are handcuffed.")
                case ValidMoves.SHOOT_D:
                    game.move(ValidMoves.SHOOT_D)
                case ValidMoves.SHOOT_P:
                    game.move(ValidMoves.SHOOT_P)
                    player_turn = True
                    game.player_turn = player_turn
                case _:
                    typePrint("Invalid move.")
                    continue 
main()
