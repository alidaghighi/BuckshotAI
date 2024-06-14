# Buckshot AI

Desperate effort of making AI to play Buckshot Roulette game

--- 
# Table of Contents

- [Buckshot AI](#buckshot-ai)
- [Table of Contents](#table-of-contents)
- [Basic information of the game](#basic-information-of-the-game)
  - [INSTRUCTIONS](#instructions)
      - [ITEMS:](#items)
- [How does the code works](#how-does-the-code-works)
  - [How to run it](#how-to-run-it)
  - [Searching](#searching)
    - [Finding Obvious Moves](#finding-obvious-moves)
    - [Minimax Search](#minimax-search)
  - [Evaluating](#evaluating)

# Basic information of the game
This game is based on the actual game `Buckshot roulette`. 

In a nutshell, this is russian roulette. But with extra flavour. It's PVE (Player-Vs-Enviorment), where you play against an AI called Dealer.

Info: https://en.wikipedia.org/wiki/Buckshot_Roulette\

## INSTRUCTIONS
- OBJECTIVE: SURVIVE.
- A shotgun is loaded with a disclosed number of bullets, some of which will be blanks. (Maximum of 8 bullets)
- Participants are given a set amount of lives each round to survive.
    - round 1: 2 lives
    - round 2: 4 lives
    - round 3: 6 lives
- You and 'The Dealer' will take turns shooting.
- Aim at The Dealer or at yourself - shooting will end your turn no matter what.
- Participants are given random items to help out. Use them wisely.
- if you have chosen wrongly, type 'q', 'quit', 'back' to go back.

#### ITEMS:
- 🚬 = Cigarette: Gives the user an extra life.
- 🍺 = Beer: Racks the shotgun and the bullet inside will be discarded.
- 🔪 = Hand Saw: Shotgun will deal double damage for one turn.
- 🔍 = Magnifying Glass: User will see what bullet is in the chamber.

---

# How does the code works

The code contains the model of the game which tried to implement the game logic as close as possible to the actual game. There's no GUI so everything is in Terminal. SOON &trade; there will be a good TUI for it. But for now we have to use menues. :)

## How to run it

clone the repo
```bash
git clone https://github.com/alidaghighi/BuckshotAI
```
go to the directory

```bash
cd BuckshotAI
```
run the `Game.py` file

```bash
python Game.py
```

---

As the AI part of the code, we have to major sections: Searching and Evaluating.

## Searching
In this code we have two types of searching:
1. Finding "Obvious Moves"
2. Minimax Search

if the AI can find an obvious move, it will take it. Otherwise, it will use Minimax Search to find the best move.

### Finding Obvious Moves

Well the Obvious moves are as the name says... obvious. Here's a table of the obvious moves:

| Condition | Move |
|-----------|------|
| Is the shell live, does the current player have a hand saw, and is the other player's health equal to 2? | Use the hand saw |
| Is the shell live and the current player does not have a hand saw? | Shoot the other player |
| Is the shell blank? | Shoot self |
| Does the current player have a magnifying glass, and is the current shell unknown? | Use the magnifying glass |
| Is the current player not on maximum health? | Use cigarettes | 

But what if it can't find an obvious move? Well, then it will use Minimax Search.

### Minimax Search

The Minimax Search is a recursive algorithm that tries to find the best move for the current player. It will search through all the possible moves and will evaluate the board after each move. The evaluation is done by the `gameEvaluation` function.
Essetially, the Minimax Search will go through all the possible moves.

The state of the game is the game itself. which contains the following information:
- The current player turn
- The health of the players
- The bullets in the chamber
- The items that the players have
- The round number
- The health of the dealer
- the items that the dealer has
- all the possible moves

The Minimax Search will get all the possible moves and go to the next state of the game, till we hit the depth limit or the end of the game which is either the HP of the players are 0.
At early stages of the game, the tree may not be that deep, but as the game progresses, the tree will get deeper and deeper. But to save the time for deeper searches, we will use the alpha-beta pruning.
There are two functions implemented for the Minimax Search:
- `minimax(game: Buckshot, depth: int, maximizingPlayer: bool)` function for normal minimax search
- `minimax_with_pruning(game: Buckshot, depth: int, maximizingPlayer: bool, alpha: int, beta: int)` function for minimax search with alpha-beta pruning

How the evaluation function works you may ask.

## Evaluating

Personally I think that the best approach is to try to maximize the health diffrence between dealer and player and minimize the health of the other player. So as the game progresses, the AI will try to take health diffrence between the dealer and the player in his advantage. Since we don't know the order of the bullets and the items are random so after each turn we have to go through all the possible moves and evaluate the game again and again.
So we consider the chance of the bullet being live or blank and the health diffence.
I may be wrong about this approach and the formula but here is it:
``` python
def gameEvaluation(state):
        eval = 0
        if player_health == 0:
            eval = float('-inf')
        elif dealer_health == 0:
            eval = float('inf')
        
        if number_lives_bullet + number_blanks_bullet != 0:
            live_prob = number_lives_bullet / (number_lives_bullet + number_blanks_bullet)
            blank_prob = number_blanks_bullet / (number_lives_bullet + number_blanks_bullet)
            if live_prob > blank_prob:
                eval += 1 * (1 if player_turn else -1)
            else:
                eval += -1 * (1 if player_turn else -1)
        else:
            eval += (dealer_health - player_health) * (1 if player_turn else -1)    
        return eval
```

I'm not sure if this is the best approach but it works for now. I will try to improve it in the future for sure.

---

I hope you enjoyed this little project of mine. I will try to improve it in the future. Better AI, better game logic, better everything.