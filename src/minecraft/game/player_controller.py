"""
Minecraft player controller - handles player movement and actions
"""
import pygame


class MinecraftPlayer:
    """Minecraft player controller"""

    def __init__(self):
        self.position = pygame.Vector2(0, 0)
        self.is_sneaking = False
        self.is_sprinting = False
        self.facing = 'north'

    def player_move(self, direction: str):
        """Move player in specified direction"""
        movements = {
            'north': (0, -1),
            'south': (0, 1),
            'east': (1, 0),
            'west': (-1, 0),
        }

        if direction in movements:
            delta = movements[direction]
            # Simple movement logic - actual movement would need world collision
            self.position += pygame.Vector2(delta)
            self.facing = direction

    def player_jump(self):
        """Make player jump"""
        # Jump logic would interact with physics engine
        pass

    def player_sneak(self):
        """Make player sneak/crouch"""
        self.is_sneaking = True

    def player_sprint(self):
        """Make player sprint"""
        self.is_sprinting = True

    def player_interact(self):
        """Player interact with blocks"""
        # Mining, placing, etc.
        pass
