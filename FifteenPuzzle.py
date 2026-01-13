import random
from typing import List, Tuple, Optional, Union


class FifteenPuzzle:
    def __init__(self, width: int = 4, height: int = 4):
        self.width = width
        self.height = height
        self.size = width * height

        # State
        self.board: List[int] = []
        self.empty_index: int = 0

        # Initialize ordered board
        self.reset()

    def reset(self):
        """Resets the board to the solved state: [1, 2, ..., 0]"""
        self.board = list(range(1, self.size)) + [0]
        self.empty_index = self.size - 1

    def is_solved(self) -> bool:
        """Checks if tiles are in order 1..N with 0 at the end."""
        # Check all positions except the last one
        for i in range(self.size - 1):
            if self.board[i] != i + 1:
                return False
        # Check the last position is the empty tile (0)
        return self.board[-1] == 0

    def is_legal_move(self, target_index: int) -> bool:
        """
        Determines if the empty tile can be swapped with the target_index.
        Checks bounds and adjacency (Manhattan distance == 1).
        """
        if target_index < 0 or target_index >= self.size:
            return False

        empty_x, empty_y = self.empty_index % self.width, self.empty_index // self.width
        target_x, target_y = target_index % self.width, target_index // self.width

        dist = abs(empty_x - target_x) + abs(empty_y - target_y)
        return dist == 1

    def legal_moves(self) -> List[int]:
        """Returns a list of indices that are valid moves from the current state."""
        moves = []
        # Potential neighbors: Left, Right, Up, Down
        offsets = [-1, 1, -self.width, self.width]

        for offset in offsets:
            neighbor_index = self.empty_index + offset
            if self.is_legal_move(neighbor_index):
                moves.append(neighbor_index)

        return moves

    def make_move(self, target_index: int) -> bool:
        """
        Swaps the empty tile with the target index if valid.
        Returns True if the move was successful, False otherwise.
        """
        if not self.is_legal_move(target_index):
            return False

        # Swap
        self.board[self.empty_index], self.board[target_index] = \
            self.board[target_index], self.board[self.empty_index]

        # Update empty pointer
        self.empty_index = target_index
        return True

    def shuffle(self, steps: int = 1000) -> List[int]:
        """
        Performs a random walk to shuffle the board.
        Returns the path taken (list of indices moved) so it can be reversed/solved.
        """
        path = []
        last_index = -1

        for _ in range(steps):
            moves = self.legal_moves()

            # Try not to immediately undo the last move to make shuffling more effective
            if len(moves) > 1 and last_index in moves:
                moves.remove(last_index)

            if moves:
                # Record current empty position (where the tile will move TO)
                # Note: The visualizer usually wants the index of the tile that moved.
                # When we swap Empty(A) with Tile(B), Tile moves to A.
                previous_empty = self.empty_index

                target = random.choice(moves)
                self.make_move(target)

                path.append(target)
                last_index = previous_empty

        return path

    # --- Methods specifically to help the Solver ---

    def get_state(self) -> Tuple[List[int], int]:
        """Returns a copy of the current board and empty index."""
        return list(self.board), self.empty_index

    def set_state(self, board: Union[List[int],Tuple], empty_index: int):
        """Forces the board to a specific state."""
        self.board = list(board)
        self.empty_index = empty_index
