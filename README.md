# Battleship

## The Game

 - 2D battleship game on a 10x10 grid.
 - Each player starts with a total of 10 ships: lengths 4, 3, 3, 3, 2, 2, 2, 1, 1, 1. Unique to this program.
 - The player will play against an AI
 - The placement of the ships are randomised for both the player and the AI
 - The player can re-randomise the ship placement with the randomise button, cannot be used after first move by player.
 - Each ship is placed horizontally or vertically on the grid and is not visible to the opponent.
 - Players take turns to fire at a position on the enemy grid and the program will indicate if the shot is a miss or a hit on a enemy ship.
 - If a player hits a ship, they get an additional turn to fire again.
 - A ship is sunk if every cell of the ship has been hit.
 - The winner is the first player to destroy the opponent's fleet of ships.
 - For full rules, visit [Wikipedia](https://en.wikipedia.org/wiki/Battleship)

## Features

 - Clear symbols to mark which shots are miss, which shots have hit a ship, and if a ship is sunk.
 - After each hit or sunk, the program will automatically mark the cells where it's impossible for other ship cells to be.
 - Messages to the player to display if they win or lose.
 - Rules button that opens a link to the rules.
 - Highlights the cell where the shot will land.

## Implementation

### AI 
- Randomly selects a cell on the enemy grid to shoot at.
- If the cell has already been shot at, the AI will select a new cell. This will continue until the selected cell has not been shot at.
- Also accounts for the extra turn if it has hit a ship.

### Randomised placement
- Randomises location and orientation of each ship.
- Makes sure that all ships don't overlap, go off the grid, or be adjacent to another ship.
- Accounts for all sizes

### Sunken Ship
- Loops through the grid to find a ship cell that has been hit.
- Uses BFS to determine adjacent cell locations and determine if they are hit as well. Continues until each cell in a ship has been visited.
- In other words, determine if the whole ship is sunk or not. 
- Marks the whole ship if the ship is sunk.


### Game end conditions
- Loops through both player and AI grid.
- Checks to see if there are any standing ship
- If there isn't, the respective player losses.
- Otherwise the game continues.

## How to run
Run Battleship.py to start the game.
