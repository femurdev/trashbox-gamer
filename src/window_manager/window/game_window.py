"""
Game window for Minecraft or emulator instances
Handles rendering and game loop for active gameplay
"""
import pygame
from src.window_manager.window.base import BaseWindow


class GameWindow(BaseWindow):
    def __init__(self, width=1920, height=1080, title="Game", game_type="minecraft"):
        super().__init__(width, height, title)
        self.game_type = game_type  # 'minecraft', 'nes', 'gamecube', 'wii', 'wiiu'
        self.active_game = None

        # Fullscreen options
        self.is_fullscreen = False
        self.fullscreen_mode = pygame.FULLSCREEN_FULLSCREEN

        # Create display surface
        pygame.display.set_mode(
            (width, height),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self.surface = pygame.display.set_mode(
            (width, height),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )

    def set_fullscreen(self, is_fullscreen: bool = True):
        """Enable or disable fullscreen mode"""
        if is_fullscreen:
            self.surface = pygame.display.set_mode(
                (0, 0),
                pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            )
        else:
            self.surface = pygame.display.set_mode(
                (self.width, self.height),
                pygame.HWSURFACE | pygame.DOUBLEBUF
            )
        self.is_fullscreen = is_fullscreen

    def update(self):
        """Update game state"""
        if self.active_game:
            self.active_game.update()

    def draw(self):
        """Draw game content"""
        # Clear surface
        self.surface.fill((0, 0, 0))

        # Draw active game
        if self.active_game:
            self.active_game.draw(self.surface)

        # Show surface
        pygame.display.flip()

    def set_active_game(self, game):
        """Set the active game instance"""
        self.active_game = game

    def handle_resize(self):
        """Handle window resize events"""
        current_size = self.surface.get_size()
        new_size = pygame.display.get_surface().get_size()

        if current_size != new_size:
            # Handle resize appropriately
            pass
