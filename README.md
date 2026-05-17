# Trashbox Gamer - Multi-Platform Gaming Interface

A Raspberry Pi 5 based gaming system that provides:
- 4-way Minecraft (3 controller support, 1 keyboard)
- NES, GameCube, Wii, and Wii U emulation
- PS4 controller support with customizable mappings

## Project Structure

```
trashbox-gamer-pygame-interface/
├── main.py                    # Entry point
├── setup.py                   # Installation script
├── README.md                  # This file
├── config/                    # Configuration files
│   └── control_mappings.json  # Controller mappings
├── assets/                    # Images, sounds, textures
├── src/
│   ├── window_manager/
│   │   ├── window/
│   │   │   ├── base.py         # Base window class
│   │   │   ├── game_window.py  # Game/emulator window
│   │   │   └── menu_window.py  # Main menu window
│   │   └── __init__.py         # Window manager
│   ├── minecraft/
│   │   ├── game/
│   │   │   ├── player_controller.py
│   │   │   └── minecraft_game.py
│   │   └── world/
│   │       └── __init__.py     # World generation
│   ├── emulator/
│   │   └── core/
│   │       └── __init__.py     # Emulator integration
│   └── controls/
│       ├── input_handler.py    # Unified input handling
│       └── mappings/
│           └── __init__.py     # Controller mappings
└── docs/
    ├── architecture/
    ├── setup/
    └── guides/
```

## Features

### 1. Window Management System
- **Main Menu**: Navigate through games and emulators
- **Game Windows**: Fullscreen or windowed mode for games
- **Emulator Integration**: Launch external emulators (Dolphin, RetroArch)

### 2. Controller Support
- **Keyboard**: WASD or Arrow keys for Minecraft
- **3 PS4 Controllers**:
  - Controller 1: Minecraft player
  - Controller 2: Dolphin Emulator Instance 1 (GameCube/Wii)
  - Controller 3: Dolphin Emulator Instance 2 (GameCube/Wii)

### 3. Platform Support
- **NES**: RetroArch with Nestopia core
- **GameCube**: Dolphin emulator (instance 1)
- **Wii**: Dolphin emulator (instance 2)
- **Wii U**: Dolphin emulator (Wii U core)

### 4. Pi-Optimized
- Lightweight rendering
- Adjustable graphics settings
- Optimized for Raspberry Pi 5

## Installation

```bash
# Install dependencies
pip install pygame pillow

# Install Raspberry Pi software
sudo apt-get install dolphin-emu retroarch nestopia

# Set up configuration
python setup.py install
```

## Usage

```bash
python main.py
```

## Development

### Adding New Emulators

1. Create a new emulator class in `src/emulator/core/`
2. Implement `start()`, `stop()`, and `get_status()` methods
3. Add to `EmulatorManager` in `src/emulator/core/__init__.py`

### Adding New Controls

1. Update mappings in `config/control_mappings.json`
2. Use `ControlMapping` class to save/load configurations

## Architecture

### Window Manager
The window manager abstracts away the complexity of managing multiple game instances. It provides:
- A single entry point for all game windows
- Unified input handling across keyboard and controllers
- Menu navigation and game launching

### Input Handler
Provides a unified interface for:
- Keyboard input
- Multiple PS4 controllers
- Cross-platform button names (UP, DOWN, LEFT, RIGHT, A, B, X, Y)

### Emulator Core
Manages external emulator processes:
- Launches games on demand
- Handles process lifecycle
- Provides status checking

## Technical Details

### Performance Optimization
- Use hardware-accelerated surfaces
- Adjust DPI scaling for Pi display
- Limit framerate for background emulators

### Memory Management
- Load only necessary chunks
- Garbage collect unloaded worlds
- Use texture atlases for sprites

### Network Support (Optional)
- Multiplayer Minecraft server
- LAN emulator network play
- Stream gameplay via OBS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License

## Credits

Built for the Raspberry Pi community to enable multiplayer gaming and retro emulation on a Pi 5.
