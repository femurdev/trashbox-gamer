"""
Minecraft world manager - handles terrain generation and rendering
"""
import random
from PIL import Image


class MinecraftWorld:
    """Manages Minecraft world generation and rendering"""

    def __init__(self, size_x=64, size_y=64):
        self.size_x = size_x
        self.size_y = size_y
        self.world = {}  # Simple world storage
        self.seed = random.randint(0, 1000000)
        self.generate_world()

    def generate_world(self):
        """Generate the world terrain"""
        # Simple procedural generation
        for x in range(self.size_x):
            for z in range(self.size_y):
                # Generate height based on distance from origin
                distance = ((x - self.size_x // 2) ** 2 +
                          (z - self.size_y // 2) ** 2) ** 0.5
                height = 32 - distance // 4

                # Block types
                block_types = {
                    0: 'stone',
                    16: 'grass',
                    32: 'dirt',
                    64: 'bedrock',
                }

                self.world[(x, z)] = block_types.get(height, 'stone')

    def get_block(self, x, z):
        """Get block at position"""
        key = (x, z)
        return self.world.get(key, 'air')

    def set_block(self, x, z, block_type):
        """Set block at position"""
        self.world[(x, z)] = block_type

    def get_surface_height(self, x, z):
        """Get surface height at position"""
        return self.world.get((x, z), 'air')

    def get_chunk(self, chunk_x, chunk_z):
        """Get chunk data"""
        # Generate chunk coordinates
        x1 = chunk_x * 16
        z1 = chunk_z * 16
        x2 = x1 + 16
        z2 = z1 + 16

        return {
            'blocks': [
                self.get_block(x, z)
                for x in range(x1, x2)
                for z in range(z1, z2)
            ],
            'bounds': (x1, z1, x2, z2)
        }
