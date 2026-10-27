# Project Roadmap: Go Game

---

## Part 1: Prisoners and Scoring (Western Method)

- [x] **Task 1: Liberty Detection Algorithm (BFS / Flood-Fill)**
  - [x] Write a function to find all connected stones of the same colour (a "group").
  - [x] Traverse adjacent spaces to count all unique empty `+` liberties for that group.
- [x] **Task 2: Capture Logic & Prisoner Counters**
  - [x] Add `self.black_prisoners` and `self.white_prisoners` to the `game` class `__init__`.
  - [x] After a move, check adjacent enemy groups. If a group has `0` liberties, remove its stones from the board.
  - [x] Add the number of captured stones to the active player's prisoner count.
- [x] **Task 3: Suicide Rule Validation**
  - [x] Check if a newly placed stone (and its connected group) results in `0` liberties.
  - [x] If it has `0` liberties and does not capture any enemy stones, reject the move as illegal.
    - [x] This should not capture the stone you placed if it captures everything around it.
- [x] **Task 4: Passing and Game-End Trigger**
  - [x] Implement a "pass" option for players instead of placing a stone.
  - [x] Track consecutive passes using a counter. If both players pass consecutively (2 passes in a row), end the main loop and trigger scoring.
- [ ] **Task 5: Territory Flood-Fill**
  - [ ] Scan all remaining empty `+` spaces on the board at game-end.
    - Goal to do this by selecting first empty space then flood filling until the test chars would be captured. When they are declared captured, check which colours are bordering the test chars. 
      - If both colours are bordering test chars, then it is neutral, black only is black territory and white only is white territory.
  - [ ] Group connected empty spaces into distinct territory regions.
  - [ ] Check the border of each region:
    - Bordered only by Black $\rightarrow$ Black territory.
    - Bordered only by White $\rightarrow$ White territory.
    - Bordered by both $\rightarrow$ Neutral (Dame) / 0 points.
- [ ] **Task 6: Final Score Calculation**
  - [ ] Compute final scores using the Western formula: $\text{Score} = \text{Territory} + \text{Prisoners}$.
  - [ ] Display the winner.

---

## Part 2: Building the Go Bot (Minimax AI)

- [ ] **Task A: Board Deep-Copying**
  - [ ] Write a method to create a fully independent clone of the board and game state so the bot can simulate future moves without altering the live game.
- [ ] **Task B: Legal Move Generator**
  - [ ] Write a function that scans the board and returns a list of all valid coordinates where a player can legally place a stone (filtering out taken tiles and suicide moves).
- [ ] **Task C: Heuristic Evaluation Function**
  - [ ] Write a function that takes a simulated board state, estimates the current point differential (stones + approximate territory + prisoners), and returns a single numerical score (positive for Black advantage, negative for White advantage).
- [ ] **Task D: Minimax / Lookahead Algorithm**
  - [ ] Write a recursive function taking a target `depth`.
  - [ ] Loop through legal moves, apply them to a copied board, evaluate the outcome, and choose the move that optimises the bot's score while anticipating the opponent's counter-moves.
- [ ] **Task E: Bot Integration**
  - [ ] In the main game loop, replace `makeMove()` with your bot's decision function (`bot.findBestMove(gameTest, depth=...)`) when it is the computer's turn to play.