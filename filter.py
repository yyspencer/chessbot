import sys
import re

input_file = "./data/2023-03.pgn"
output_file = "newfiltered.pgn"

white_elo_pattern = re.compile(r'^\[WhiteElo\s+"(\d+)"\]$')
black_elo_pattern = re.compile(r'^\[BlackElo\s+"(\d+)"\]$')

with open(input_file, "r", encoding="utf-8", errors="replace") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:

    current_game_lines = []
    white_elo = None
    black_elo = None

    def process_game():
        # Check the stored ratings and decide whether to write the game
        if white_elo is not None and black_elo is not None:
            if not (int(white_elo) < 2000 and int(black_elo) < 2000):
                # Write the game only if it's not both under 2000
                for line in current_game_lines:
                    fout.write(line + "\n")
                fout.write("\n")  # blank line separating games

    for line in fin:
        line = line.rstrip("\n")
        
        # Start of a new game is often recognized by the [Event ...] tag
        # If we detect a new event and we already have lines from a previous game, process that game first.
        if line.startswith("[Event ") and current_game_lines:
            # Finish the previous game
            process_game()
            # Reset for the new game
            current_game_lines = []
            white_elo = None
            black_elo = None

        # Collect line for the current game
        if line.strip() or line.startswith("[Event "):
            current_game_lines.append(line)
        
        # Extract WhiteElo and BlackElo
        we = white_elo_pattern.match(line)
        if we:
            white_elo = we.group(1)

        be = black_elo_pattern.match(line)
        if be:
            black_elo = be.group(1)

    # After the loop, if there's a game accumulated, process it too
    if current_game_lines:
        process_game()

print(f"Filtering complete. Output written to {output_file}")