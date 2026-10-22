"""
DSA TRAFFIC RACER — DSA Theory Game
====================================
Main application entry point. Orchestrates the Pygame loop, state machines,
player controls, traffic management, level progression, and DSA visualizers.

College Academic Project:
M.Tech Software Engineering — Data Structures and Algorithms Theory
"""

import sys
import os
import pygame

# Ensure current directory is accessible for local imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE
from game.player import PlayerCar
from game.traffic import TrafficManager
from game.road import Road
from game.collision import CollisionSystem
from game.level import LevelManager
from game.city_map import CityMapNavigator
from game.visualizer import DSAVisualizer
from game.ui import UIManager
from game.sound_manager import sound_fx


class DSATrafficRacerGame:
    """Main game controller and state manager."""

    # Game States
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game_over"
    STATE_VICTORY = "victory"
    STATE_VISUALIZER = "visualizer"
    STATE_LEADERBOARD = "leaderboard"
    STATE_INSTRUCTIONS = "instructions"

    def __init__(self, headless: bool = False):
        if headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            os.environ["SDL_AUDIODRIVER"] = "dummy"

        pygame.init()
        pygame.display.set_caption(GAME_TITLE)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = self.STATE_MENU

        # Core Game Subsystems
        self.level_mgr = LevelManager()
        self.traffic_mgr = TrafficManager()
        self.road = Road()
        self.collision_sys = CollisionSystem()
        self.city_nav = CityMapNavigator()
        self.visualizer = DSAVisualizer()
        self.ui = UIManager()

        self.player = PlayerCar()
        self.show_fullscreen_map = False
        self.game_over_reason = ""

        # Synchronize initial route with Level 1
        self._sync_level_routes()

    def _sync_level_routes(self):
        """Align map navigator landmarks with active level objective."""
        cfg = self.level_mgr.get_current()
        self.city_nav.set_route(cfg.origin_node, cfg.dest_node)

    def start_new_game(self, level_num: int = 1):
        """Reset all systems and begin gameplay at given level."""
        self.level_mgr.reset_level(level_num)
        self.traffic_mgr.reset()
        self.road.reset()
        self.collision_sys.reset()
        self.player = PlayerCar()
        self.show_fullscreen_map = False
        self._sync_level_routes()
        self.state = self.STATE_PLAYING

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # seconds elapsed

            self._handle_events()
            self._update(dt)
            self._render()

        pygame.quit()

    def _handle_events(self):
        """Process keyboard, mouse clicks, and window close events."""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click(mouse_pos)

    def _handle_keydown(self, key):
        """Process one-time keyboard actions."""
        if self.state == self.STATE_PLAYING:
            if key == pygame.K_p or key == pygame.K_ESCAPE:
                self.state = self.STATE_PAUSED
            elif key == pygame.K_r:
                self.start_new_game(self.level_mgr.current_level_num)
            elif key == pygame.K_u:
                # DSA Stack: Undo Movement
                self.player.undo_movement()
            elif key == pygame.K_m:
                # Toggle Fullscreen City Road Map
                self.show_fullscreen_map = not self.show_fullscreen_map

        elif self.state == self.STATE_PAUSED:
            if key == pygame.K_p or key == pygame.K_ESCAPE:
                self.state = self.STATE_PLAYING
            elif key == pygame.K_r:
                self.start_new_game(self.level_mgr.current_level_num)

        elif self.state in [self.STATE_LEADERBOARD, self.STATE_INSTRUCTIONS, self.STATE_VISUALIZER]:
            if key == pygame.K_ESCAPE:
                self.state = self.STATE_MENU

    def _handle_mouse_click(self, mouse_pos: tuple):
        """Route mouse clicks to active UI buttons."""
        if self.state == self.STATE_MENU:
            buttons = self.ui.draw_main_menu(self.screen, mouse_pos)
            for label, rect in buttons:
                if rect.collidepoint(mouse_pos):
                    if label == "START GAME":
                        self.start_new_game(1)
                    elif label == "LEADERBOARD":
                        self.state = self.STATE_LEADERBOARD
                    elif label == "HOW TO PLAY":
                        self.state = self.STATE_INSTRUCTIONS
                    elif label == "EXIT":
                        self.running = False

        elif self.state == self.STATE_PAUSED:
            buttons = self.ui.draw_pause_menu(self.screen, mouse_pos)
            for label, rect in buttons:
                if rect.collidepoint(mouse_pos):
                    if label == "RESUME":
                        self.state = self.STATE_PLAYING
                    elif label == "RESTART LEVEL":
                        self.start_new_game(self.level_mgr.current_level_num)
                    elif label == "MAIN MENU":
                        self.state = self.STATE_MENU

        elif self.state == self.STATE_GAME_OVER:
            buttons = self.ui.draw_game_over(
                self.screen, self.player.score, self.level_mgr.distance_in_level,
                self.level_mgr.current_level_num, self.game_over_reason, mouse_pos
            )
            for label, rect in buttons:
                if rect.collidepoint(mouse_pos):
                    if label == "RESTART":
                        self.start_new_game(self.level_mgr.current_level_num)
                    elif label == "MAIN MENU":
                        self.state = self.STATE_MENU

        elif self.state == self.STATE_VICTORY:
            buttons = self.ui.draw_victory(self.screen, self.player.score, self.level_mgr, mouse_pos)
            for label, rect in buttons:
                if rect.collidepoint(mouse_pos):
                    if label == "NEXT LEVEL":
                        if self.level_mgr.advance_level():
                            self.start_new_game(self.level_mgr.current_level_num)
                    elif label == "RESTART GAME":
                        self.start_new_game(1)
                    elif label == "MAIN MENU":
                        self.state = self.STATE_MENU

        elif self.state == self.STATE_LEADERBOARD:
            buttons = self.ui.draw_leaderboard(self.screen, mouse_pos)
            for label, rect in buttons:
                if rect.collidepoint(mouse_pos):
                    if label == "BACK":
                        self.state = self.STATE_MENU
                    elif label == "TOGGLE_SORT":
                        self.ui.toggle_leaderboard_sort()

        elif self.state == self.STATE_INSTRUCTIONS:
            buttons = self.ui.draw_instructions(self.screen, mouse_pos)
            for label, rect in buttons:
                if rect.collidepoint(mouse_pos) and label == "BACK":
                    self.state = self.STATE_MENU

        elif self.state == self.STATE_VISUALIZER:
            result = self.visualizer.handle_click(mouse_pos)
            if result == "back":
                self.state = self.STATE_MENU

    def _update(self, dt: float):
        """Update game physics, collisions, and animations."""
        if self.state == self.STATE_PLAYING:
            keys = pygame.key.get_pressed()

            # 1. Update Player Controls & Movement
            self.player.update(keys)

            # 2. Update Highway Road & Items
            self.road.update(self.player.speed, self.level_mgr.distance_in_level)

            # 3. Update Autonomous Traffic & Queues
            self.traffic_mgr.update(self.player.speed, self.level_mgr.current_level_num)

            # 4. Collisions
            self.collision_sys.check_traffic_collisions(self.player, self.traffic_mgr)
            self.collision_sys.check_item_collisions(self.player, self.road)
            self.collision_sys.check_checkpoint_crossings(self.player, self.road)
            self.collision_sys.update_particles()

            # 5. Check Health Game Over
            if self.player.health <= 0:
                self.game_over_reason = "Vehicle Critical Failure! Too many traffic collisions."
                self.ui.record_score("Player", self.player.score, self.level_mgr.current_level_num)
                self.state = self.STATE_GAME_OVER
                return

            # 6. Update Level Progress & Objectives
            level_status = self.level_mgr.update(dt, self.player.speed)
            if level_status == "time_out":
                self.game_over_reason = "Time Expired! Failed to reach landmark in time."
                self.ui.record_score("Player", self.player.score, self.level_mgr.current_level_num)
                self.state = self.STATE_GAME_OVER
            elif level_status in ["victory_level", "victory_game"]:
                # Award time bonus
                time_bonus = int(self.level_mgr.time_remaining * 10)
                self.player.score += time_bonus + 500
                sound_fx.play("victory")
                self.ui.record_score("Player", self.player.score, self.level_mgr.current_level_num)
                self.state = self.STATE_VICTORY

        elif self.state == self.STATE_VISUALIZER:
            self.visualizer.update()

    def _render(self):
        """Render active state display."""
        mouse_pos = pygame.mouse.get_pos()

        if self.state == self.STATE_MENU:
            self.ui.draw_main_menu(self.screen, mouse_pos)

        elif self.state == self.STATE_PLAYING:
            # 1. Road Background & Markings
            self.road.draw(self.screen)

            # 2. Collision Sparks
            self.collision_sys.draw_particles(self.screen)

            # 3. Autonomous Traffic
            self.traffic_mgr.draw(self.screen)

            # 4. Player Vehicle
            self.player.draw(self.screen)

            # 5. Academic HUD & Status
            self.ui.draw_hud(
                self.screen, self.player, self.level_mgr,
                self.city_nav, self.traffic_mgr, self.show_fullscreen_map
            )

        elif self.state == self.STATE_PAUSED:
            # Render game scene behind translucent pause overlay
            self.road.draw(self.screen)
            self.traffic_mgr.draw(self.screen)
            self.player.draw(self.screen)
            self.ui.draw_hud(
                self.screen, self.player, self.level_mgr,
                self.city_nav, self.traffic_mgr, False
            )
            self.ui.draw_pause_menu(self.screen, mouse_pos)

        elif self.state == self.STATE_GAME_OVER:
            self.ui.draw_game_over(
                self.screen, self.player.score, self.level_mgr.distance_in_level,
                self.level_mgr.current_level_num, self.game_over_reason, mouse_pos
            )

        elif self.state == self.STATE_VICTORY:
            self.ui.draw_victory(self.screen, self.player.score, self.level_mgr, mouse_pos)

        elif self.state == self.STATE_VISUALIZER:
            self.visualizer.draw(self.screen)

        elif self.state == self.STATE_LEADERBOARD:
            self.ui.draw_leaderboard(self.screen, mouse_pos)

        elif self.state == self.STATE_INSTRUCTIONS:
            self.ui.draw_instructions(self.screen, mouse_pos)

        pygame.display.flip()


def main():
    """Application launcher."""
    headless_mode = "--headless" in sys.argv
    game = DSATrafficRacerGame(headless=headless_mode)
    if "--test-run" in sys.argv:
        # Run 60 frames in headless mode for automated validation
        print("Starting 60-frame headless verification loop...")
        game.start_new_game(1)
        for _ in range(60):
            game._update(1.0 / 60.0)
            game._render()
        print("60-frame headless verification completed successfully.")
        return 0

    game.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
