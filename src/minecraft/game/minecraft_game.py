"""
Minecraft game manager - orchestrates game state
"""
import pygame
from src.minecraft.game.player_controller import MinecraftPlayer


class MinecraftGame:
    """Manages Minecraft game state and rendering"""

    def __init__(self):
        self.player = MinecraftPlayer()
        self.camera = pygame.Vector2(0, 0)
        self.block_map = {}  # Simple 2D block map
        self.rendered = False

    def update(self):
        """Update game state"""
        self.player.update()

    def draw(self, surface):
        """Draw the game to surface"""
        # Clear surface
        surface.fill((0, 60, 60))  # Default sky color

        # Draw player
        # self.draw_player(surface)

        # Draw blocks
        # self.draw_blocks(surface)

        # Draw FPS counter
        fps = self.get_fps()
        font = pygame.font.Font(None, 36)
        text = font.render(f'FPS: {fps}', True, (255, 255, 255))
        text_rect = text.get_rect(left=10, top=10)
        surface.blit(text, text_rect)

        self.rendered = True

    def get_fps(self):
        """Get current FPS"""
        clock = pygame.time.Clock()
        return clock.get_fps()

    def handle_input(self, input_handler):
        """Handle game input"""
        keys = input_handler.get_pressed_keys()
        buttons = input_handler.get_button_states('controller_1')

        # Handle movement
        if keys.get(pygame.K_w) or keys.get(pygame.K_UP) or buttons.get('UP'):
            self.player.player_move('north')
        elif keys.get(pygame.K_s) or keys.get(pygame.K_DOWN) or buttons.get('DOWN'):
            self.player.player_move('south')
        elif keys.get(pygame.K_a) or keys.get(pygame.K_LEFT) or buttons.get('LEFT'):
            self.player.player_move('west')
        elif keys.get(pygame.K_d) or keys.get(pygame.K_RIGHT) or buttons.get('RIGHT'):
            self.player.player_move('east')

        # Handle actions
        if keys.get(pygame.K_SPACE) or buttons.get('CROSS') or buttons.get('A'):
            self.player.player_jump()

        if keys.get(pygame.K_LEFT_SHIFT):
            self.player.player_sneak()
        else:
            self.player.is_sneaking = False

        if keys.get(pygame.K_RIGHT_SHIFT):
            self.player.player_sprint()
        else:
            self.player.is_sprinting = False
