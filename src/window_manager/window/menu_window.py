"""
Main menu window - displays game selection, system info, and settings
"""
import pygame
import os
from src.window_manager.window.base import BaseWindow


class MenuWindow(BaseWindow):
    def __init__(self, width=1920, height=1080):
        super().__init__(width, height, title="Trashbox Gamer - Main Menu")

        # Menu items
        self.menu_items = [
            "Minecraft",
            "NES Games",
            "GameCube Games",
            "Wii Games",
            "Wii U Games",
            "Settings",
            "Quit",
        ]

        # Current selection
        self.selection = 0
        self.selected_color = (0, 255, 0)  # Green
        self.hover_color = (100, 200, 255)  # Blue

        # Create menu surface
        self.menu_surface = pygame.Surface((width, height))

        # Load fonts
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)

    def update(self):
        """Update menu state and handle input"""
        keys = pygame.key.get_pressed()

        # Navigation
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.selection -= 1
            if self.selection < 0:
                self.selection = len(self.menu_items) - 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.selection += 1
            if self.selection >= len(self.menu_items):
                self.selection = 0
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # Optional: Show info/preview
            pass
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # Optional: Launch preview
            pass
        elif keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            # Select item
            self._handle_selection()
        elif keys[pygame.K_ESCAPE]:
            # Close menu
            return False

        return True

    def _handle_selection(self):
        """Handle menu item selection"""
        item = self.menu_items[self.selection]

        actions = {
            "Minecraft": lambda: print("Launching Minecraft..."),
            "NES Games": lambda: print("Launching NES emulator..."),
            "GameCube Games": lambda: print("Launching GameCube emulator..."),
            "Wii Games": lambda: print("Launching Wii emulator..."),
            "Wii U Games": lambda: print("Launching Wii U emulator..."),
            "Settings": lambda: print("Opening settings..."),
            "Quit": lambda: False,
        }

        action = actions.get(item)
        if action:
            return action()
        return True

    def draw(self):
        """Draw the menu"""
        # Clear background
        self.menu_surface.fill((20, 20, 30))

        # Draw title
        title = self.font_large.render(
            "TRASHBOX GAMER",
            True,
            (255, 255, 255)
        )
        title_rect = title.get_rect(
            center=(self.width // 2, 80)
        )
        self.menu_surface.blit(title, title_rect)

        # Draw subtitle
        subtitle = self.font_small.render(
                    "Multi-Platform Gaming Interface",
                    True,
                    (255, 255, 255)
                )
        subtitle_rect = subtitle.get_rect(
            center=(self.width // 2, 130)
        )
        self.menu_surface.blit(subtitle, subtitle_rect)

        # Draw menu items
        item_height = 60
        y_offset = 180

        for i, item in enumerate(self.menu_items):
            color = self.selected_color if i == self.selection else (180, 180, 220)

            text = self.font_small.render(item, True, color)
            text_rect = text.get_rect(
                x=50,
                y=y_offset + i * item_height
            )
            self.menu_surface.blit(text, text_rect)

            # Draw selection indicator
            if i == self.selection:
                indicator = self.font_small.render(">", True, self.selected_color)
                indicator_rect = indicator.get_rect(
                    x=20,
                    y=y_offset + i * item_height + 12
                )
                self.menu_surface.blit(indicator, indicator_rect)

        # Draw system info
        info = self.font_small.render(
                    f"Controllers: {pygame.joystick.get_count()}",
                    True,
                    (255, 255, 255)
                )
        info_rect = info.get_rect(
            x=50,
            y=self.height - 40
        )
        self.menu_surface.blit(info, info_rect)

        # Copy to display
        self.surface.blit(self.menu_surface, (0, 0))
        pygame.display.flip()
