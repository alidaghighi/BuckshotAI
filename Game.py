import time
import random
from Buckshot import *
from Search import *
from TypePrint import typePrint



name = ""

def displayHelp():
    typePrint("\n+=====================+\n")
    typePrint("This game is based on the actual game 'buckshot roulette'.\nIn a nutshell, this is russian roulette.\nInfo: https://en.wikipedia.org/wiki/Buckshot_Roulette\n")
    typePrint("INSTRUCTIONS:")
    typePrint("    - OBJECTIVE: SURVIVE.")
    typePrint("    - A shotgun is loaded with a disclosed number of bullets, some of which will be blanks. (Maximum of 8 bullets)")
    typePrint("    - Participants are given a set amount of lives each round to survive.")
    typePrint("        - round 1: 2 lives")
    typePrint("        - round 2: 4 lives")
    typePrint("        - round 3: 6 lives")
    typePrint("    - You and 'The Dealer' will take turns shooting.")
    typePrint("    - Aim at The Dealer or at yourself - shooting will end your turn no matter what.")
    typePrint("    - Participants are given random items to help out. Use them wisely.")
    typePrint("    - if you have chosen wrongly, type 'q'/'quit'/'back' to go back.")
    print()
    typePrint("ITEMS:")
    typePrint("    • 🚬 = Cigarette: Gives the user an extra life.")
    typePrint("    • 🍺 = Beer: Racks the shotgun and the bullet inside will be discarded.")
    typePrint("    • 🔪 = Hand Saw: Shotgun will deal double damage for one turn.")
    typePrint("    • 🔍 = Magnifying Glass: User will see what bullet is in the chamber.")
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
        case ValidMoves.SHOOT_D:
            return "Shooting Dealer."
        case ValidMoves.SHOOT_P:
            return "Shooting Player."
        case _:
            return "Unknown move."

def StartRound(round: int, scores: list, playerItems: list, dealerItems: list):
    global name
    player_turn = True
    game = Buckshot(
        round=round,
        player_items=playerItems,
        dealer_items=dealerItems,
        player_turn=player_turn,
    )
    while not game.isEnd():
        typePrint("\n\n")
        typePrint(f"The number of blank bullets: {game.num_blanks_bullet}")
        typePrint(f"The number of live bullets: {game.num_lives_bullet}")
        if  game.num_blanks_bullet == 0 and game.num_lives_bullet == 0:
            typePrint("The gun is empty.")
            typePrint("Reloading...")
            game.reload()
            continue
        
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
            player_turn = game.player_turn
            
        else:
            typePrint("Dealer's turn: ")
            time.sleep(0.5)
            typePrint(f"Dealer's health: {game.dealer_health}")
            typePrint(f"Your health: {game.player_health}")
            typePrint("====================================")
            time.sleep(0.5)
            typePrint("Dealer's items:")
            displayItems(game.dealer_items)
            move = Search.obvious_moves(game)
            if move == ValidMoves.NO_MOVE:
                move = Search.search(game, 3, True)
            move = Search.search(game, 3, True)
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
                case ValidMoves.SHOOT_D:
                    game.move(ValidMoves.SHOOT_D)
                case ValidMoves.SHOOT_P:
                    game.move(ValidMoves.SHOOT_P)
                case _:
                    typePrint("Invalid move.")
                    continue 
            player_turn = game.player_turn
    typePrint("Round is OVER.")
    if game.player_health > 0:
        typePrint("Player Won this round.")
        scores.append("player")
    else:
        typePrint("Dealer Won this round.")
        scores.append("dealer")
    

def itemGenerator(itemNumber):
    # Generate random items for the player
    items = []
    for i in range(itemNumber):
        item = random.choice(list(Items))
        items.append(item)
    return items
    

        
def main():
    typePrint("[DEALER]: PLEASE SIGN THE WAIVER.")
    askforhelp = ''
    global name
    while askforhelp not in ["a","b"]:
        askforhelp = input("(a) Read Waiver or (b) Sign and continue? ").lower().strip(" ")

    if askforhelp == "a":
        displayHelp()
        input("READY? ")
    while name in ["DEALER"] or not (3 < len(name) < 10):
        if name:
            typePrint("INVALID NAME.")
        name = input("ENTER NAME [between 4-9 chars]: ").strip(" ").upper()
    
    scores = []
    round = 1
    while True:
        match round:
            case 1:
                typePrint("ROUND 1")
                typePrint("Initial HP: 2")
                typePrint("No Items for the first round...")
                playerItems = []
                dealerItems = []
                StartRound(1, scores, playerItems, dealerItems)
            case 2:
                typePrint("ROUND 2")
                typePrint("Initial HP: 4")
                playerItems = itemGenerator(2)
                dealerItems = itemGenerator(2)
                typePrint("Player's Starting Items:")
                displayItems(playerItems)
                typePrint("Dealer's Starting Items:")
                displayItems(dealerItems)
                StartRound(2, scores, playerItems, dealerItems)
            case 3:
                typePrint("ROUND 3")
                typePrint("Initial HP: 6")
                typePrint("Careful...")
                typePrint("If the HP goes lower than 2...")
                typePrint("IT IS SUDDEN DEATH!")
                typePrint("Have fun :)")
                playerItems = itemGenerator(4)
                dealerItems = itemGenerator(4)
                typePrint("Player's Starting Items:")
                displayItems(playerItems)
                typePrint("Dealer's Starting Items:")
                displayItems(dealerItems)
                StartRound(3, scores, playerItems, dealerItems)
                break
        round += 1
    
main()
