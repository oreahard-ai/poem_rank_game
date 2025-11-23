# Poem Rank Game

An interactive game where 2–5 players each receive a random four-line poem and rate every line on a 1–5 scale. You can play in the terminal or through the new web experience.

## How to play
### Web version
1. Ensure you have Python 3.8+ available.
2. Install the web dependency:
   ```bash
   pip install flask
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Visit http://127.0.0.1:5000 in your browser.
5. Choose the number of players (2–5), add names, then rate every line in the assigned poems. Results are summarized on the final page.

### Terminal version
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
