## Fifteen Visualizer

import pygame
import sys
from typing import List, Tuple
from FifteenPuzzle import FifteenPuzzle
from FifteenSolver import FifteenSolver
from FifteenTrace import FifteenTrace, Move, Score

# Configuration Constants
TILE_SIZE = 80
TILE_MARGIN = 5
FPS = 30
STATUS_HEIGHT = 50  # Added: Extra height for the bottom status bar

# Colors
BACKGROUND_COLOR = (50, 60, 70)
TEXT_COLOR = (0, 0, 0)
EMPTY_COLOR = (50, 50, 50)
STATUS_LINE_COLOR = (255, 255, 255)
TILE_COLOR_CORRECT = (100, 200, 100)  # Green
TILE_COLOR_WRONG = (200, 200, 100)  # Yellow
SCORE_COLOR = (255, 50, 50)  # Red for viz scores


class FifteenVisualizer:
    def __init__(self, puzzle: FifteenPuzzle, solver: FifteenSolver):
        self.puzzle = puzzle
        self.solver = solver

        # Calculate screen dimensions
        self.grid_w = puzzle.width
        self.grid_h = puzzle.height
        self.screen_width = self.grid_w * TILE_SIZE
        # Modified: Add STATUS_HEIGHT to the total window height
        self.screen_height = self.grid_h * TILE_SIZE + STATUS_HEIGHT

        # Pygame Init
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Fifteen Puzzle - Manual")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font = pygame.font.SysFont("arial", int(TILE_SIZE * 0.5), bold=True)
        self.score_font = pygame.font.SysFont("arial", int(TILE_SIZE * 0.25), bold=True)

        # Solution State
        self.solution: List[FifteenTrace] = []
        self.solution_index: int = 0

        # Animation State
        self.is_playing: bool = False
        self.animation_speed: int = 30
        self.animation_timer: int = 0

    def generate_solution(self):
        """Runs the solver and resets playback state."""
        print("Solving...")
        self.is_playing = False
        self.solution_index = 0

        # Expecting solver.solve to return List[FifteenTrace]
        self.solution = self.solver.solve()
        pygame.display.set_caption(f"Solution Found: {len(self.solution)} steps")
        pygame.display.set_caption(f"Solver ran with {len(self.solution)} results")

        # print(f"Solution found with {len(self.solution)} steps.")

    def step_forward(self):
        """Executes the next move in the solution."""
        if self.solution and self.solution_index < len(self.solution):
            trace = self.solution[self.solution_index]

            self.puzzle.set_state(trace.starting_state, trace.move_from)
            self.puzzle.make_move(trace.move_to)

            self.solution_index += 1
            return True
        else:
            self.is_playing = False
            return False

    def step_backward(self):
        if self.solution and self.solution_index > 0:
            # We are currently at state AFTER solution[index-1]
            # We want to undo the move performed at solution[index-1]
            last_trace = self.solution[self.solution_index - 1]

            self.puzzle.set_state(last_trace.starting_state, last_trace.move_from)
            self.solution_index -= 1
            return True
        else:
            return False

    def _get_tile_rect(self, index):
        """Helper to calculate rect for a given grid index."""
        x = index % self.grid_w
        y = index // self.grid_w
        rect_x = x * TILE_SIZE + TILE_MARGIN
        rect_y = y * TILE_SIZE + TILE_MARGIN
        rect_w = TILE_SIZE - (2 * TILE_MARGIN)
        rect_h = TILE_SIZE - (2 * TILE_MARGIN)
        return pygame.Rect(rect_x, rect_y, rect_w, rect_h)

    def _draw_grid(self):
        """Draws the basic grid tiles and numbers."""
        self.screen.fill(BACKGROUND_COLOR)

        for i, tile_number in enumerate(self.puzzle.board):
            tile_rect = self._get_tile_rect(i)

            if tile_number == 0:
                pygame.draw.rect(self.screen, EMPTY_COLOR, tile_rect, border_radius=8)
            else:
                expected_number = i + 1
                color = (
                    TILE_COLOR_CORRECT
                    if tile_number == expected_number
                    else TILE_COLOR_WRONG
                )
                pygame.draw.rect(self.screen, color, tile_rect, border_radius=8)

                text_surf = self.font.render(str(tile_number), True, TEXT_COLOR)
                text_rect = text_surf.get_rect(center=tile_rect.center)
                self.screen.blit(text_surf, text_rect)

    def _draw_overlay(self):
        """Draws the 'viz' scores from the current trace step."""
        if not self.solution or self.solution_index >= len(self.solution):
            return

        # Get the trace for the *upcoming* move
        current_trace = self.solution[self.solution_index]

        # Iterate through the visualization list: List[Tuple[Move, Score]]
        for move_index, score in current_trace.viz:
            target_rect = self._get_tile_rect(move_index)

            # Create score text
            score_surf = self.score_font.render(str(score), True, SCORE_COLOR)

            # Position in lower-left corner with small padding
            score_rect = score_surf.get_rect(
                bottomleft=(target_rect.left + 5, target_rect.bottom - 2)
            )

            self.screen.blit(score_surf, score_rect)

    def _draw_status_line(self):
        # Added: Draw Step count in the bottom status area if a solution exists
        if self.solution:
            step_text = f"Step: {self.solution_index}"
            # Using white color for contrast against dark background
            text_surf = self.font.render(step_text, True, STATUS_LINE_COLOR)
            # Position at the bottom left, accounting for the new extra height
            self.screen.blit(text_surf, (10, self.screen_height - STATUS_HEIGHT + 5))

    def draw_board(self):
        """Main draw function combining grid and overlay."""
        self._draw_grid()
        self._draw_overlay()
        self._draw_status_line()

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Quit
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                # Solver Controls
                elif event.key == pygame.K_s:
                    self.generate_solution()
                elif event.key == pygame.K_d:
                    self.is_playing = False
                    self.step_forward()
                elif event.key == pygame.K_a:
                    self.is_playing = False
                    self.step_backward()
                elif event.key == pygame.K_p:
                    if self.solution:
                        self.is_playing = not self.is_playing
                elif event.key == pygame.K_j:
                    self.solution_index = len(self.solution) - 1
                    print(f"Jumped to {self.solution_index}")
                elif event.key == pygame.K_c:
                    print(self.puzzle.board, file=sys.stderr)

                # Standard Controls
                elif event.key == pygame.K_SPACE:
                    self.is_playing = False
                    self.solution = []
                    self.puzzle.shuffle()
                    pygame.display.set_caption("Fifteen Puzzle - Shuffled")

                # Manual Movement (Interrupts solution visualization)
                target_index = -1
                if event.key == pygame.K_LEFT:
                    target_index = self.puzzle.empty_index + 1
                elif event.key == pygame.K_RIGHT:
                    target_index = self.puzzle.empty_index - 1
                elif event.key == pygame.K_UP:
                    target_index = self.puzzle.empty_index + self.grid_w
                elif event.key == pygame.K_DOWN:
                    target_index = self.puzzle.empty_index - self.grid_w

                if target_index != -1 and self.puzzle.is_legal_move(target_index):
                    # Manual move invalidates current trace playback
                    self.solution = []
                    self.is_playing = False
                    self.puzzle.make_move(target_index)

    def update(self):
        """Handles automatic playback timing."""
        if self.is_playing:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.step_forward()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw_board()
            self.clock.tick(FPS)


if __name__ == "__main__":
    puzz = FifteenPuzzle(3, 3)
    solv = FifteenSolver(puzz)
    viz = FifteenVisualizer(puzz, solv)
    viz.run()
