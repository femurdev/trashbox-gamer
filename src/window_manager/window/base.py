"""
Base class for all windows - provides common functionality
"""
import pygame


class BaseWindow:
    def __init__(self, width=1920, height=1080, title="Game Interface"):
        self.width = width
        self.height = height
        self.title = title
        self.running = True
        self.surface = pygame.display.set_mode((self.width, self.height))

        pygame.init()
        pygame.display.set_caption(title)

    def set_surface(self, surface):
        """Set the render surface"""
        self.surface = surface

    def update(self):
        """Update window state - to be overridden"""
        pass

    def draw(self):
        """Draw window content - to be overridden"""
        pass

    def close(self):
        """Close and clean up the window"""
        self.running = False
        if self.surface:
            pygame.display.quit()
        pygame.quit()
