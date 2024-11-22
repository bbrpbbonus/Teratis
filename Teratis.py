import pygame
import random
import sys
import json
import time

from typing import List, Tuple, Optional, Set, Dict
from dataclasses import dataclass
from enum import Enum
import math


# Game States
class GameState(Enum):
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3
    WON = 4


# Enhanced color palette
COLORS = [
    (255, 215, 0),  # Gold
    (147, 112, 219),  # Purple
    (0, 191, 255),  # Deep Sky Blue
    (50, 205, 50),  # Lime Green
    (255, 99, 71),  # Tomato Red
]


class UIManager:
    def __init__(self, screen_width: int, screen_height: int, block_size: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.sidebar_width = 200
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        self.colors = {
            "background": (15, 23, 42),  # slate-900
            "panel": (30, 41, 59),  # slate-800
            "text": (226, 232, 240),  # slate-200
            "score": (250, 204, 21),  # yellow-400
            "combo": (192, 132, 252),  # purple-400
            "time": (96, 165, 250),  # blue-400
            "progress_bg": (51, 65, 85),  # slate-700
            "progress_fill": (250, 204, 21),  # yellow-400
        }

        self.pulse_time = 0
        self.particles = []

    def create_particle(self, x: int, y: int, color: Tuple[int, int, int]):
        return {
            "x": x,
            "y": y,
            "dx": random.uniform(-2, 2),
            "dy": random.uniform(-2, 2),
            "lifetime": 30,
            "color": color,
            "size": random.uniform(2, 4),
        }

    def update_particles(self):
        for particle in self.particles[:]:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["lifetime"] -= 1
            if particle["lifetime"] <= 0:
                self.particles.remove(particle)

    def draw_sidebar(
        self,
        screen: pygame.Surface,
        score: int,
        time_left: int,
        combo: int,
        target_score: int,
    ):
        sidebar_rect = pygame.Rect(
            self.screen_width - self.sidebar_width,
            0,
            self.sidebar_width,
            self.screen_height,
        )
        pygame.draw.rect(screen, self.colors["panel"], sidebar_rect)

        # Score section
        y_pos = 20
        score_text = self.font_large.render(f"{score}", True, self.colors["score"])
        score_label = self.font_small.render("SCORE", True, self.colors["text"])
        screen.blit(score_text, (self.screen_width - self.sidebar_width + 20, y_pos))
        screen.blit(
            score_label, (self.screen_width - self.sidebar_width + 20, y_pos + 40)
        )

        # Progress bar
        y_pos += 80
        progress_rect = pygame.Rect(
            self.screen_width - self.sidebar_width + 20,
            y_pos,
            self.sidebar_width - 40,
            10,
        )
        progress_fill_rect = pygame.Rect(
            progress_rect.left,
            progress_rect.top,
            progress_rect.width * (score / target_score),
            progress_rect.height,
        )
        pygame.draw.rect(screen, self.colors["progress_bg"], progress_rect)
        pygame.draw.rect(screen, self.colors["progress_fill"], progress_fill_rect)

        # Time section
        y_pos += 40
        minutes = time_left // 60
        seconds = time_left % 60
        time_text = self.font_medium.render(
            f"{minutes:02d}:{seconds:02d}", True, self.colors["time"]
        )
        screen.blit(time_text, (self.screen_width - self.sidebar_width + 20, y_pos))

        # Combo section
        if combo > 1:
            y_pos += 60
            pulse = abs(math.sin(self.pulse_time)) * 8
            combo_text = self.font_medium.render(
                f"COMBO x{combo}", True, self.colors["combo"]
            )
            combo_pos = (self.screen_width - self.sidebar_width + 20 + pulse, y_pos)
            screen.blit(combo_text, combo_pos)
            self.pulse_time += 0.1

    def draw_grid_background(self, screen: pygame.Surface):
        for y in range(0, self.screen_height, 4):
            for x in range(0, self.screen_width - self.sidebar_width, 4):
                pygame.draw.circle(screen, (30, 41, 59), (x + 2, y + 2), 1)

    def draw_block_shadow(self, screen: pygame.Surface, x: int, y: int):
        shadow_rect = pygame.Rect(
            x * self.block_size + 2,
            y * self.block_size + 2,
            self.block_size - 1,
            self.block_size - 1,
        )
        shadow_surface = pygame.Surface((self.block_size - 1, self.block_size - 1))
        shadow_surface.fill((0, 0, 0))
        shadow_surface.set_alpha(64)
        screen.blit(shadow_surface, shadow_rect)

    def draw_particles(self, screen: pygame.Surface):
        for particle in self.particles:
            alpha = int(255 * (particle["lifetime"] / 30))
            color = (*particle["color"], alpha)
            pygame.draw.circle(
                screen,
                color,
                (int(particle["x"]), int(particle["y"])),
                particle["size"],
            )

    def draw_game_over(
        self,
        screen: pygame.Surface,
        score: int,
        high_scores: List[dict],
        game_state: GameState,
    ):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        y_pos = self.screen_height // 3

        # Display "YOU WON!" if the game is won
        if game_state == GameState.WON:
            game_over_text = "YOU WON!"
            text_color = (0, 255, 0)  # Green color
        else:
            game_over_text = "GAME OVER"
            text_color = (255, 0, 0)  # Red color

        # Game Over text with shadow
        text = self.font_large.render(game_over_text, True, text_color)
        shadow = self.font_large.render(game_over_text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width // 2, y_pos))
        screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(text, text_rect)

        y_pos += 60
        score_text = self.font_medium.render(
            f"Final Score: {score}", True, self.colors["text"]
        )
        score_rect = score_text.get_rect(center=(self.screen_width // 2, y_pos))
        screen.blit(score_text, score_rect)

        y_pos += 60
        title = self.font_medium.render("High Scores", True, self.colors["score"])
        title_rect = title.get_rect(center=(self.screen_width // 2, y_pos))
        screen.blit(title, title_rect)

        for i, score_data in enumerate(high_scores[:5]):
            y_pos += 30
            score_line = self.font_small.render(
                f"{i+1}. {score_data['name']}: {score_data['score']}",
                True,
                self.colors["text"],
            )
            score_rect = score_line.get_rect(center=(self.screen_width // 2, y_pos))
            screen.blit(score_line, score_rect)

        y_pos += 60
        restart_text = self.font_small.render(
            "Press R to Restart", True, self.colors["text"]
        )
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, y_pos))
        screen.blit(restart_text, restart_rect)

        # Check if "R" is pressed to restart the game when won
        if game_state == GameState.WON:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.restart_game()  # Call method to restart the game


@dataclass
class GameConfig:
    block_size: int = 30
    grid_width: int = 10
    grid_height: int = 20
    time_limit: int = 180
    target_score: int = 1000
    initial_fall_speed: int = 500


@dataclass
class Block:
    x: int
    y: int
    color: Tuple[int, int, int]
    shape: Optional["BlockShape"] = None
    matched: bool = False

    def __hash__(self):
        return hash((self.x, self.y, self.color))

    def __eq__(self, other):
        if not isinstance(other, Block):
            return NotImplemented
        return (self.x, self.y, self.color) == (other.x, other.y, other.color)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def draw(
        self, screen: pygame.Surface, block_size: int, ui_manager: UIManager
    ) -> None:
        if self.shape:
            for y, row in enumerate(self.shape.blocks):
                for x, has_block in enumerate(row):
                    if has_block:
                        ui_manager.draw_block_shadow(screen, self.x + x, self.y + y)
                        pygame.draw.rect(
                            screen,
                            self.color,
                            (
                                (self.x + x) * block_size,
                                (self.y + y) * block_size,
                                block_size - 1,
                                block_size - 1,
                            ),
                        )
        else:
            ui_manager.draw_block_shadow(screen, self.x, self.y)
            pygame.draw.rect(
                screen,
                self.color,
                (
                    self.x * block_size,
                    self.y * block_size,
                    block_size - 1,
                    block_size - 1,
                ),
            )

    def moved(self, dx: int, dy: int) -> "Block":
        return Block(self.x + dx, self.y + dy, self.color, self.shape, self.matched)


class BlockShape:
    def __init__(self, color: Tuple[int, int, int], shape_type: str):
        self.color = color
        self.shape_type = shape_type
        self.rotation = 0
        self.blocks = self.get_shape_blocks()

    def get_shape_blocks(self) -> List[List[bool]]:
        shapes = {
            "I": [[True], [True], [True], [True]],
            "L": [[True, False], [True, False], [True, True]],
            "T": [[True, True, True], [False, True, False]],
            "S": [[False, True, True], [True, True, False]],
            "O": [[True, True], [True, True]],
        }
        return shapes.get(self.shape_type, [[True]])

    def rotate(self) -> None:
        self.rotation = (self.rotation + 90) % 360
        rotated = list(zip(*self.blocks[::-1]))
        self.blocks = [list(row) for row in rotated]
        
    def restart(self):
        # Reset game variables to restart the game
        self.score = 0
        self.game_state = GameState.PLAYING  # Change to playing state to start a new game
        self.reset_player()  # Reset player or other game-specific elements
        self.reset_level()  # Reset level or any other necessary game elements



class Game:
    def __init__(self):
        pygame.init()

        self.config = GameConfig()
        self.screen = pygame.display.set_mode(
            (
                self.config.grid_width * self.config.block_size + 200,
                self.config.grid_height * self.config.block_size,
            )
        )
        pygame.display.set_caption("Teratis")

        self.state = GameState.PLAYING
        self.ui_manager = UIManager(
            self.screen.get_width(), self.screen.get_height(), self.config.block_size
        )
        self.high_score_manager = HighScoreManager()
        self.next_block = None

        self.reset_game()

    def reset_game(self):
        self.grid = [
            [None for _ in range(self.config.grid_width)]
            for _ in range(self.config.grid_height)
        ]
        self.current_block = None
        self.next_block = None
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.fall_speed = self.config.initial_fall_speed
        self.combo_count = 0
        self.state = GameState.PLAYING

    def create_new_block(self) -> None:
        if not self.current_block and self.state == GameState.PLAYING:
            if self.next_block:
                self.current_block = self.next_block
            else:
                x = self.config.grid_width // 2
                color = random.choice(COLORS)
                new_block = Block(x, 0, color)
                new_block.shape = BlockShape(
                    color, random.choice(["I", "L", "T", "S", "O"])
                )
                self.current_block = new_block

            # Create next block
            x = self.config.grid_width // 2
            color = random.choice(COLORS)
            self.next_block = Block(x, 0, color)
            self.next_block.shape = BlockShape(
                color, random.choice(["I", "L", "T", "S", "O"])
            )

            if not self.is_valid_move(self.current_block, 0, 0):
                self.state = GameState.GAME_OVER
                self.show_game_over_animation()
                return

    def is_valid_move(self, block: Block, dx: int, dy: int) -> bool:
        if not block.shape:
            return False

        for y, row in enumerate(block.shape.blocks):
            for x, has_block in enumerate(row):
                if has_block:
                    new_x = block.x + x + dx
                    new_y = block.y + y + dy

                    if not (
                        0 <= new_x < self.config.grid_width
                        and 0 <= new_y < self.config.grid_height
                    ):
                        return False

                    if new_y >= 0 and self.grid[new_y][new_x] is not None:
                        return False
        return True

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.toggle_pause()
            elif event.key == pygame.K_r:
                self.reset_game()
            elif self.state == GameState.PLAYING:
                self.handle_gameplay_input(event)
        elif event.type == pygame.KEYUP and self.state == GameState.PLAYING:
            if event.key == pygame.K_DOWN:
                self.fall_speed = self.config.initial_fall_speed

    def handle_gameplay_input(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_LEFT:
            self.move_block(-1)
        elif event.key == pygame.K_RIGHT:
            self.move_block(1)
        elif event.key == pygame.K_DOWN:
            self.fall_speed = 50
        elif event.key == pygame.K_UP:
            self.rotate_block()
        elif event.key == pygame.K_SPACE:
            self.hard_drop()

    def toggle_pause(self):
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def move_block(self, dx: int) -> None:
        if self.current_block and self.is_valid_move(self.current_block, dx, 0):
            self.current_block = self.current_block.moved(dx, 0)

    def hard_drop(self):
        if not self.current_block:
            return
        while self.is_valid_move(self.current_block, 0, 1):
            self.current_block.move(0, 1)
        self.place_block()

    def rotate_block(self):
        if self.current_block:
            old_blocks = self.current_block.shape.blocks.copy()
            self.current_block.shape.rotate()
            if not self.is_valid_move(self.current_block, 0, 0):
                self.current_block.shape.blocks = old_blocks

    def drop_block(self) -> bool:
        if not self.current_block:
            return False

        if self.is_valid_move(self.current_block, 0, 1):
            self.current_block.move(0, 1)
            return False
        else:
            self.place_block()
            return True

    def place_block(self) -> None:
        if not self.current_block:
            return

        for y, row in enumerate(self.current_block.shape.blocks):
            for x, has_block in enumerate(row):
                if has_block:
                    grid_x = self.current_block.x + x
                    grid_y = self.current_block.y + y
                    self.grid[grid_y][grid_x] = Block(
                        grid_x, grid_y, self.current_block.color
                    )
                    self.add_landing_effect(grid_x, grid_y)

        matches = self.find_matches()
        if matches:
            self.remove_matches(matches)
            self.apply_gravity()

            while True:
                matches = self.find_matches()
                if not matches:
                    break
                self.remove_matches(matches)
                self.apply_gravity()

        self.current_block = None

    def add_landing_effect(self, x: int, y: int):
        radius = self.config.block_size // 2
        for _ in range(5):
            self.ui_manager.particles.append(
                self.ui_manager.create_particle(
                    x * self.config.block_size + radius,
                    y * self.config.block_size + radius,
                    (255, 255, 255),
                )
            )

    def find_matches(self) -> List[List[Block]]:
        matches = []
        for y in range(self.config.grid_height - 1, -1, -1):
            line = []
            line_complete = True

            for x in range(self.config.grid_width):
                if self.grid[y][x] is None:
                    line_complete = False
                    break
                line.append(self.grid[y][x])

            if line_complete:
                matches.append(line)

        return matches

    def remove_matches(self, matches: List[List[Block]]) -> None:
        if not matches:
            self.combo_count = 0
            return

        lines_cleared = len(matches)
        base_scores = {1: 100, 2: 300, 3: 500, 4: 800}
        score_gain = base_scores.get(lines_cleared, 800) * self.combo_count
        self.score += score_gain
        self.combo_count += 1

        for line in matches:
            for block in line:
                self.grid[block.y][block.x] = None
                for _ in range(5):
                    self.ui_manager.particles.append(
                        self.ui_manager.create_particle(
                            block.x * self.config.block_size,
                            block.y * self.config.block_size,
                            block.color,
                        )
                    )

    def apply_gravity(self) -> None:
        for x in range(self.config.grid_width):
            empty_y = None

            for y in range(self.config.grid_height - 1, -1, -1):
                if self.grid[y][x] is None:
                    if empty_y is None:
                        empty_y = y
                elif empty_y is not None:
                    self.grid[empty_y][x] = self.grid[y][x]
                    self.grid[y][x] = None
                    self.grid[empty_y][x].y = empty_y
                    empty_y -= 1

    def show_game_over_animation(self):
        fade_surface = pygame.Surface((self.config.block_size, self.config.block_size))
        fade_surface.fill((0, 0, 0))

        for alpha in range(0, 255, 5):
            fade_surface.set_alpha(alpha)
            for y in range(self.config.grid_height):
                for x in range(self.config.grid_width):
                    if self.grid[y][x]:
                        self.screen.blit(
                            fade_surface,
                            (x * self.config.block_size, y * self.config.block_size),
                        )
            pygame.display.flip()
            pygame.time.wait(10)

    def draw(self) -> None:
        self.screen.fill(self.ui_manager.colors["background"])
        self.ui_manager.draw_grid_background(self.screen)

        if self.state == GameState.PAUSED:
            self.draw_pause_screen()
        elif self.state in [GameState.GAME_OVER, GameState.WON]:
            self.ui_manager.draw_game_over(
                self.screen, self.score, self.high_score_manager.high_scores, self.state
            )
        else:
            self.draw_game_screen()

        self.ui_manager.update_particles()
        self.ui_manager.draw_particles(self.screen)

        pygame.display.flip()

    def draw_game_screen(self):
        for y in range(self.config.grid_height):
            for x in range(self.config.grid_width):
                pygame.draw.rect(
                    self.screen,
                    (50, 50, 50),
                    (
                        x * self.config.block_size,
                        y * self.config.block_size,
                        self.config.block_size,
                        self.config.block_size,
                    ),
                    1,
                )
                if self.grid[y][x]:
                    self.grid[y][x].draw(
                        self.screen, self.config.block_size, self.ui_manager
                    )

        if self.current_block:
            self.current_block.draw(
                self.screen, self.config.block_size, self.ui_manager
            )

        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_remaining = max(0, self.config.time_limit - elapsed_time)

        self.ui_manager.draw_sidebar(
            self.screen,
            self.score,
            time_remaining,
            self.combo_count,
            self.config.target_score,
        )

    def draw_pause_screen(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 48)
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(text, text_rect)

    def run(self) -> None:
        clock = pygame.time.Clock()
        fall_time = 0

        while True:
            if self.state == GameState.PLAYING:
                elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
                if elapsed_time >= self.config.time_limit:
                    self.state = GameState.GAME_OVER
                    self.show_game_over_animation()
                    self.high_score_manager.add_score(self.score)

                if self.score >= self.config.target_score:
                    self.state = GameState.WON
                    self.show_game_over_animation()
                    player_name = self.get_player_name()
                    self.high_score_manager.add_score(self.score, player_name)

                delta_time = clock.tick(60)
                fall_time += delta_time

                if fall_time >= self.fall_speed:
                    if self.current_block:
                        self.drop_block()
                    fall_time = 0

                if not self.current_block:
                    self.create_new_block()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_input(event)

            self.draw()
            clock.tick(60)

    def get_player_name(self) -> str:
        name = ""
        font = pygame.font.Font(None, 36)
        input_active = True
        cursor_visible = True
        cursor_timer = 0
        max_name_length = 12

        # Add a clock to control the blinking cursor
        self.clock = pygame.time.Clock()

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < max_name_length:
                            name += event.unicode

            # Draw semi-transparent overlay
            self.screen.fill(self.ui_manager.colors["background"])
            overlay = pygame.Surface(
                (self.screen.get_width(), self.screen.get_height())
            )
            overlay.fill((0, 0, 0))
            overlay.set_alpha(150)
            self.screen.blit(overlay, (0, 0))

            # Draw input box
            box_width = 400
            box_height = 200
            box_x = (self.screen.get_width() - box_width) // 2
            box_y = (self.screen.get_height() - box_height) // 2
            pygame.draw.rect(
                self.screen,
                self.ui_manager.colors["panel"],
                (box_x, box_y, box_width, box_height),
                border_radius=10,
            )

            # Draw prompt text
            prompt_text = font.render(
                "Enter your name", True, self.ui_manager.colors["text"]
            )
            prompt_rect = prompt_text.get_rect(
                center=(self.screen.get_width() // 2, box_y + 50)
            )
            self.screen.blit(prompt_text, prompt_rect)

            # Draw input text box inside the input area
            input_rect = pygame.Rect(box_x + 50, box_y + 100, box_width - 100, 40)
            pygame.draw.rect(
                self.screen, self.ui_manager.colors["background"], input_rect
            )
            pygame.draw.rect(self.screen, self.ui_manager.colors["text"], input_rect, 2)

            # Blinking cursor logic
            cursor_timer += self.clock.tick(60)
            if cursor_timer >= 500:
                cursor_visible = not cursor_visible
                cursor_timer = 0

            # Render name text
            name_surface = font.render(name, True, self.ui_manager.colors["text"])
            self.screen.blit(name_surface, (input_rect.x + 5, input_rect.y + 5))

            # Draw cursor if visible
            if cursor_visible and len(name) < max_name_length:
                cursor_pos = input_rect.x + 5 + name_surface.get_width()
                pygame.draw.line(
                    self.screen,
                    self.ui_manager.colors["text"],
                    (cursor_pos, input_rect.y + 5),
                    (cursor_pos, input_rect.y + input_rect.height - 5),
                )

            pygame.display.flip()

        return name.strip() or "Player"


class HighScoreManager:
    def __init__(self):
        self.high_scores: List[Dict] = self.load_high_scores()

    def load_high_scores(self) -> List[Dict]:
        try:
            with open("high_scores.json", "r") as f:
                return json.load(f)
        except:
            return []

    def save_high_scores(self):
        
        with open("high_scores.json", "w") as f:
            json.dump(self.high_scores, f)

    def add_score(self, score: int, player_name: str = "Player"):
        self.high_scores.append(
            {"score": score, "name": player_name, "date": time.strftime("%Y-%m-%d")}
        )
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]
        self.save_high_scores()


if __name__ == "__main__":
    game = Game()
    game.run()