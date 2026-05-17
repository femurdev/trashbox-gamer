# Architecture Documentation

## How the Pygame Window Manager Works

### Overview

The window manager acts as a central orchestrator that:
1. Initializes pygame and input handling
2. Creates and manages game windows
3. Routes input to the correct application
4. Handles window switching between menu and games

### Key Components

#### 1. MainGame (src/window_manager/__init__.py)

The main orchestrator class that:
- Initializes pygame and controllers
- Manages the current active window
- Handles input routing
- Switches between menu and game windows

```python
game = MainGame()
game.switch_window("menu")  # Start with menu
game.run()                  # Main loop
```

#### 2. Window Types

**MenuWindow**
- Displays game selection menu
- Handles navigation input
- Launches games/emulators on selection

**GameWindow**
- Manages fullscreen/windowed mode
- Renders game content
- Handles window resize events

**EmulatorWindow**
- Launches external emulators
- Manages emulator processes
- Handles emulator-specific input

#### 3. Input Handling

The `InputHandler` provides unified input across all devices:
- Keyboard: pygame.key.get_pressed()
- Controllers: pygame.joystick interface
- Normalized button names (UP, DOWN, LEFT, RIGHT, A, B, X, Y)

### Input Flow

```
User Input
    ↓
InputHandler.poll_events()
    ↓
Keys & Button States
    ↓
MainGame._handle_game_input()
    ↓
Routing to:
    - _handle_minecraft_input()   → MinecraftGame
    - _handle_emulator_input()    → EmulatorManager
```

### Emulator Integration

The emulator system uses subprocess to launch external emulators:

```python
emulator = DolphinEmulator('GC')
emulator.start(game_path)  # Launches Dolphin with game
emulator.stop()            # Close when done
```

This approach:
- Avoids complex API integrations
- Maintains compatibility with existing emulator installations
- Allows users to use their preferred emulator configurations

### Performance Considerations

1. **Window Creation**: Use HWSURFACE for hardware acceleration
2. **FPS Control**: Limit to 60 FPS to save resources
3. **Input Polling**: Use pygame.event.poll() for efficiency
4. **Window Switching**: Free running emulators when not needed

## Multi-Player Setup

### Controller Assignment

| Controller | Assignment | Purpose |
|------------|------------|---------|
| Controller 1 | Minecraft | Player 1 (WSAD + Jump) |
| Controller 2 | Dolphin 1 | GameCube/Wii Emulator |
| Controller 3 | Dolphin 2 | GameCube/Wii Emulator |

### Network Play

For LAN multiplayer:
1. Configure each controller's MAC address
2. Assign controllers to specific players/emulators
3. Use UDP networking for synchronization

## Configuration

### Control Mappings

Edit `config/control_mappings.json` to customize controls:

```json
{
  "minecraft": {
    "controller_1": {
      "up": "UP",
      "down": "DOWN",
      "jump": "CROSS"
    }
  }
}
```

### Emulator Settings

Each emulator can be configured with:
- Graphics settings
- Controller mappings
- Performance tweaks
- Save game locations

## File Structure

```
trashbox-gamer-pygame-interface/
├── main.py
├── setup.py
├── config/
│   └── control_mappings.json
├── assets/
├── src/
│   ├── window_manager/
│   │   ├── window/
│   │   │   ├── base.py
│   │   │   ├── game_window.py
│   │   │   └── menu_window.py
│   │   └── __init__.py
│   ├── minecraft/
│   │   ├── game/
│   │   │   ├── player_controller.py
│   │   │   └── minecraft_game.py
│   │   └── world/
│   └── emulator/
│       └── core/
│           └── __init__.py
└── docs/
```

## Extending the System

### Adding New Emulators

1. Create a new class extending `Emulator`
2. Implement the required methods
3. Add to the manager
4. Test thoroughly

### Adding New Games

For games that don't use external emulators:
1. Create a new game class in `src/minecraft/game/`
2. Implement `update()` and `draw()` methods
3. Register with the window manager

### Custom Menus

Create custom menu windows by extending `MenuWindow`:

```python
class CustomMenu(MenuWindow):
    def __init__(self):
        super().__init__()
        # Customize menu items
        
    def draw(self):
        # Custom rendering
        pass
```
