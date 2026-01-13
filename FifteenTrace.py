from dataclasses import dataclass
from typing import List, Tuple

Move = int
Score = int

@dataclass
class FifteenTrace:
    move_from: Move
    move_to: Move
    starting_state : Tuple
    # mapping of Move -> Score, including this move
    viz: List[Tuple[Move, Score]]

