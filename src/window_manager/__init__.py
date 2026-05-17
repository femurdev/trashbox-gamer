"""
Main application entry point - Manages the Pygame window and orchestrates all components
"""
import sys
import pygame
from src.window_manager.window.game_window import GameWindow
from src.window_manager.window.menu_window import MenuWindow
from src.controls.input_handler import InputHandler

class MainGame:
    def __init__(self):
        pygame.init()

        # Initialize input handler for all controllers
        self.input_handler = InputHandler()

        # Create main window (menu or game)
        self.main_window = None
        self.active_window = None

        # Track active game/emulation
        self.current_game = None
        self.is_running = False

        # Set up event handling
        self.setup_events()

    def setup_events(self):
        """Set up pygame event handling"""
        pygame.event.set_grab(False)
        pygame.display.set_caption("Trashbox Gamer - Multi-Platform Gaming Interface")

    def switch_window(self, window_type: str, **kwargs):
        """Switch between menu and game windows"""
        if window_type == "menu":
            self.main_window = MenuWindow(**kwargs)
            self.active_window = self.main_window
            pygame.display.set_caption("Trashbox Gamer - Main Menu")
            self._handle_menu_input()
        elif window_type == "game":
            self.main_window = GameWindow(**kwargs)
            self.active_window = self.main_window
            pygame.display.set_caption(f"Trashbox Gamer - {kwargs.get('title', 'Game')}")
            self.current_game = kwargs.get('game_id')
            self.is_running = True
            self._handle_game_input()
        elif window_type == "emulator":
            self.main_window = GameWindow(type="emulator", **kwargs)
            self.active_window = self.main_window
            pygame.display.set_caption(f"Trashbox Gamer - {kwargs.get('title', 'Emulator')}")
            self.current_game = kwargs.get('game_id')
            self.is_running = True
            self._handle_game_input()

    def _handle_menu_input(self):
        """Handle menu input for navigation"""
        keys = self.input_handler.get_pressed_keys()

        # Example menu navigation
        if keys.get(pygame.K_UP) or self.input_handler.get_button('UP'):
            # Navigate up
            print("Navigate up")
        elif keys.get(pygame.K_DOWN) or self.input_handler.get_button('DOWN'):
            # Navigate down
            print("Navigate down")
        elif keys.get(pygame.K_LEFT) or self.input_handler.get_button('LEFT'):
            # Navigate left
            print("Navigate left")
        elif keys.get(pygame.K_RIGHT) or self.input_handler.get_button('RIGHT'):
            # Navigate right
            print("Navigate right")
        elif keys.get(pygame.K_RETURN) or self.input_handler.get_button('A') or self.input_handler.get_button('X'):
            # Select
            print("Select")
        elif keys.get(pygame.K_ESCAPE):
            # Close or quit
            self.quit()

    def _handle_game_input(self):
        """Handle game input with controller support"""
        keys = self.input_handler.get_pressed_keys()
        buttons = self.input_handler.get_button_states()

        # Get cross-platform input (keyboard + 3 controllers)
        # This abstraction allows the same game logic to work with:
        # - Keyboard (WSAD/Arrows for Minecraft)
        # - Controller 1 (Controller 1 for game)
        # - Controller 2 (Emulator 1 for Dolphin)
        # - Controller 3 (Emulator 2 for Dolphin)

        if self.current_game == "minecraft":
            self._handle_minecraft_input(keys, buttons)
        else:
            self._handle_emulator_input(keys, buttons)

    def _handle_minecraft_input(self, keys, buttons):
        """Handle Minecraft-specific input"""
        # Minecraft controls mapped to keyboard AND controller
        # Player 1 (Minecraft) - uses controller 1 or keyboard
        if keys.get(pygame.K_w) or keys.get(pygame.K_UP) or buttons.get('UP'):
            self.current_game.player_move('north')
        elif keys.get(pygame.K_s) or keys.get(pygame.K_DOWN) or buttons.get('DOWN'):
            self.current_game.player_move('south')
        elif keys.get(pygame.K_a) or keys.get(pygame.K_LEFT) or buttons.get('LEFT'):
            self.current_game.player_move('west')
        elif keys.get(pygame.K_d) or keys.get(pygame.K_RIGHT) or buttons.get('RIGHT'):
            self.current_game.player_move('east')

        # Jump
        if keys.get(pygame.K_SPACE) or buttons.get('CROSS') or buttons.get('A'):
            self.current_game.player_jump()

    def _handle_emulator_input(self, keys, buttons):
        """Handle emulator input (Dolphin for Wii/Wii U/GameCube)"""
        # Each controller gets mapped to a specific emulator instance
        # Controller 2 -> Dolphin Instance 1
        # Controller 3 -> Dolphin Instance 2
        # Controller 1 -> Reserved for Minecraft
        pass

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                # Handle window switching events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # Right click - cycle windows
                        print("Right-click: Cycle through games/emulators")

            # Update windows
            if self.active_window:
                self.active_window.update()

            # Control FPS
            clock.tick(60)

            # Draw window
            if self.active_window:
                self.active_window.draw()

            pygame.display.flip()

        self.quit()

    def quit(self):
        """Quit the application cleanly"""
        if self.active_window:
            self.active_window.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MainGame()
    game.switch_window("menu")
    game.run()
