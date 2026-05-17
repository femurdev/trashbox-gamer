# How to Implement the Pygame Window Manager

The window manager is the heart of this system. Here's how it works and how you can extend it.

## Core Concept

The window manager uses pygame to create a single main window that can display:
1. A main menu (when no game is running)
2. An active game window (Minecraft)
3. An emulator window (NES, GameCube, Wii, Wii U)

All three share the same pygame window, but only one is visible at a time.

## Implementation Details

### 1. Main Window Loop

The main loop (in `src/window_manager/__init__.py`):

```python
def run(self):
    """Main game loop"""
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Update active window
        if self.active_window:
            self.active_window.update()
            
        # Control FPS
        clock.tick(60)
            
        # Draw window
        if self.active_window:
            self.active_window.draw()
            
        pygame.display.flip()
```

### 2. Switching Between Windows

Use the `switch_window()` method:

```python
# Show menu
game.switch_window("menu")

# Launch Minecraft
game.switch_window("game", title="Minecraft", game_id="minecraft")
game.active_window.set_active_game(minecraft_game)

# Launch emulator
game.switch_window("emulator", title="Zelda OoT", game_id="gamecube")
```

### 3. Input Handling

The window manager routes input based on the current game:

```python
def _handle_game_input(self):
    """Handle game input with controller support"""
    keys = self.input_handler.get_pressed_keys()
    buttons = self.input_handler.get_button_states()
    
    if self.current_game == "minecraft":
        self._handle_minecraft_input(keys, buttons)
    else:
        self._handle_emulator_input(keys, buttons)
```

### 4. Controller Mapping

Each controller gets mapped to specific actions:

```python
# Controller 1 - Minecraft
buttons['UP']    # Player moves north
buttons['DOWN']  # Player moves south
buttons['CROSS'] # Jump

# Controller 2 - Emulator 1
# Mapped to Dolphin controller 1

# Controller 3 - Emulator 2
# Mapped to Dolphin controller 2
```

## Customizing the Menu

To add more menu items:

```python
class CustomMenuWindow(MenuWindow):
    def __init__(self, width=1920, height=1080):
        super().__init__(width, height)
        
        # Add your menu items
        self.menu_items = [
            "Minecraft",
            "NES Games",
            "GameCube Games",
            "Wii Games",
            "Wii U Games",
            "Settings",
            "Quit",
        ]
```

## Creating a New Game Window

```python
class MyGameWindow(GameWindow):
    def __init__(self, width=1920, height=1080):
        super().__init__(width, height, title="My Game")
        
    def update(self):
        # Your game logic here
        pass
        
    def draw(self):
        # Your rendering here
        pass
```

## Running Multiple Games Simultaneously

The current implementation runs only one game at a time. To run multiple games simultaneously:

1. **Option 1**: Use separate pygame displays
   ```python
   # Main display
   pygame.display.set_mode((1920, 1080))
   
   # Secondary display (if available)
   pygame.display.set_mode((1920, 1080), pygame.OPENGL)
   ```

2. **Option 2**: Use threading for background emulators
   ```python
   import threading
   
   def run_emulator(platform, game_path):
       emulator = DolphinEmulator(platform)
       emulator.start(game_path)
       # Keep running in background
       
   thread = threading.Thread(target=run_emulator, args=("wii", game_path))
   thread.daemon = True
   thread.start()
   ```

3. **Option 3**: Use the Dolphin built-in multi-instance support
   - Configure Dolphin to use multiple controller instances
   - Each instance gets its own controller mapping

## Fullscreen vs Windowed Mode

The window manager supports both modes:

```python
window = GameWindow()
window.set_fullscreen(True)  # Default

# Toggle fullscreen
window.set_fullscreen(False)
```

On Raspberry Pi, fullscreen is recommended for:
- Better performance
- Immersive experience
- Using the full display resolution

## Testing Your Setup

```bash
# Test controllers
python -c "import pygame; pygame.init(); print('Controllers:', pygame.joystick.get_count())"

# Test input handling
python -c "from src.controls import InputHandler; h = InputHandler(); print(h.get_button_states())"
```

## Common Issues

### 1. Controllers Not Detected

Add a delay after init:

```python
joystick.init()
pygame.joystick.Joystick(i).set_init()
time.sleep(0.1)  # Give time to initialize
```

### 2. Emulator Not Starting

Check if the emulator binary exists:

```bash
which dolphin
which retroarch
```

### 3. Performance Issues

- Lower pygame framerate (30 FPS instead of 60)
- Use lower resolution
- Disable fullscreen for testing

## Next Steps

1. Add texture rendering for Minecraft
2. Implement save/load for game states
3. Add settings UI for controller configuration
4. Create a settings window for adjusting emulator options
