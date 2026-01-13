import heapq
import unittest
from typing import List, Tuple, Dict
from FifteenPuzzle import FifteenPuzzle
from FifteenTrace import FifteenTrace

BoardTuple = Tuple
GameState = Tuple[List, int]

class FifteenSolver:
    def __init__(self, puzzle: FifteenPuzzle):
        self.puzzle = puzzle
        self.width = puzzle.width

    def score_board(self, board: List[int]) -> int:
        w = self.width
        score = 0
        for pos, val in enumerate(board):
            if val == 0: continue  # FIX: Ignore the empty tile to match expectations
            val -= 1  # 1 goes in (0,0)
            x0, y0 = pos % w, pos // w
            x1, y1 = val % w, val // w
            score += abs(x0 - x1) + abs(y0 - y1)
        return score

    def first_trace_info(self, heap: List[Tuple[int, int, int, GameState]]):
        seen = set()
        vals = sorted(heap)
        result = []
        for heuristic, known, move, (state, pos) in vals:
            if pos not in seen:
                seen.add(pos)
                result.append((pos, heuristic))
        return result

    def solve(self, maxsteps: int = 200):
        return self.solve_Astar(maxsteps)

    def solve_Astar(self, maxsteps: int = 100) -> List[int]:
        '''A-star search: like Dijkstra: minimize total number of moves plus estimated number remaining.
        The heuristic function is sum(Manhattan distance (current location, final location).'''
        solution = []
        p = self.puzzle

        # Preserve the starting state so we can reset after calculation
        unmoved = p.get_state()

        # candidates : List[Tuple[cost steps + heuristic, steps, move to this state, state]]
        candidates: List[Tuple[int, int, int, GameState]]
        candidates = [(0, 0, -1, unmoved)]

        ## Dict[tuple for board, steps to get there]
        results: Dict[BoardTuple, int]
        results = {}

        ## Could also add a best known cost dictionary so we do not add items to the queue that are worse than the known
        bestknown = {}

        solved = False
        while candidates and len(solution) < maxsteps:
            trace_info = self.first_trace_info(candidates)
            cost_estimate, cost_known, move_from, (original_board, move_to) = heapq.heappop(candidates)

            ob = tuple(original_board)
            if ob in results and cost_known >= results[tuple(ob)]:
                continue

            results[ob] = cost_known
            solution.append(FifteenTrace(move_from, move_to, starting_state=ob, viz=trace_info))

            p.set_state(original_board, move_to)

            # below, this is the square we are moving _from_
            original_empty = move_to

            if p.is_solved():
                solved = True
                solution.append(FifteenTrace(move_to, move_to, starting_state=ob, viz=trace_info))
                break

            cost_known += 1 # account for one more move made two lines below
            for m in p.legal_moves():
                p.make_move(m)
                cost_heuristic = self.score_board(p.board)
                cost_estimate = cost_known + cost_heuristic
                t = tuple(p.board)
                if t not in bestknown or cost_estimate < bestknown[t]:
                    bestknown[t] = cost_estimate
                    candidates.append((cost_estimate, cost_known, original_empty, p.get_state()))

                p.set_state(original_board, original_empty)

            # This is for visualizing, need to know the lowest cost estimate to get to each possible posn
            candidates.sort()

        if not solved:
            print(f'Warning: did not find a solution in {maxsteps}.')
        else:
            print(f'## Solved')
            for line in solution:
                print(f'  Move from {line.move_from} to {line.move_to} scored {line.viz[0]}')

        # Restore the board to its original state before returning the solution path
        p.set_state(*unmoved)

        return solution

    def solve_greedy(self, maxsteps: int = 100) -> List[int]:
        '''Greedy method: moves to reduce Manhattan distance of squares to their proper locations.
        Quickly gets stuck in a local minimum.'''
        solution = []
        p = self.puzzle

        # Preserve the starting state so we can reset after calculation
        unmoved = p.get_state()

        while len(solution) < maxsteps and not p.is_solved():
            original = p.get_state()
            candidates = []

            # Greedy search: try all legal moves, score them, pick the best
            for m in p.legal_moves():
                p.make_move(m)
                mscore = self.score_board(p.board)
                candidates.append((mscore, m))
                p.set_state(*original)  # Undo move

            if not candidates:
                break

            # Sort candidates by score (best/lowest score first)
            candidates.sort()

            best_score, best_move = candidates[0]
            solution.append(FifteenTrace(best_move, candidates))
            p.make_move(best_move)  # Make the best move to proceed to next state

        # Restore the board to its original state before returning the solution path
        p.set_state(*unmoved)

        return solution

