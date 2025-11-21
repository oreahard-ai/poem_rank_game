# Poem Rank Game

An interactive terminal game where 2–5 players each receive a random four-line poem and rate every line on a 1–5 scale.

## How to play
1. Ensure you have Python 3.8+ available.
2. Run the game:
   ```bash
   python poem_game.py
   ```
3. Enter the number of players (2–5) and provide unique player names (defaults like "Player 1" are provided if you leave a name blank).
4. Each player is shown a random poem and asked to rate each of its four lines from 1 (lowest) to 5 (highest).
5. When all players finish, the game prints each player's scores and the overall group average.

## Game rules and safeguards
- Player count is validated so the game only starts with 2–5 participants.
- Ratings must be integers between 1 and 5; invalid entries are re-prompted.
- Poem assignments are randomized every session.
