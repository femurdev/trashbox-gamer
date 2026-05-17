# Setup Guide

This guide will help you set up your Raspberry Pi 5 for the Trashbox Gamer project.

## Hardware Requirements

### Raspberry Pi 5
- 8GB or 16GB RAM (recommended: 16GB with M.2 upgrade)
- SD Card or NVMe M.2 SSD
- HDMI display
- 3x DualShock 4 / DualSense controllers
- Power supply: 30W+ with 5.1A output

### Controllers
- PS4 DualShock 4 (x3) or PS5 DualSense
- Optional: USB adapter for wired connection
- Ensure all controllers are charged

## Software Setup

### 1. Raspberry Pi OS Installation

```bash
# Download Raspberry Pi Imager
# Flash Raspberry Pi OS 64-bit Lite (no desktop) to SD/M.2

# Write to SD card
# Insert SD card and write
```

### 2. System Updates

```bash
sudo apt update
sudo apt upgrade -y
```

### 3. Install Python and Pygame

```bash
# Install Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip

# Install pygame
pip3 install pygame pillow
```

### 4. Install Emulators

#### Dolphin Emulator

```bash
# Install Dolphin
sudo apt install dolphin-emu

# Or download from https://dolphin-emu.org/
# Extract to /opt/dolphin
```

#### RetroArch

```bash
sudo apt install retroarch retroarch-libs

# Install cores:
sudo apt install libretro-nestopia
sudo apt install libretro-snes9x
```

#### Nestopia

```bash
sudo apt install nestopia
```

### 5. Install Pygame Dependencies

```bash
pip3 install pygame pillow numpy
```

## Controller Setup

### 1. Pair Controllers

For each controller:

```bash
# Put controller in pairing mode (hold PS + Share)

# On Raspberry Pi, pair via Bluetooth
bluetoothctl
> power on
> scan on
# Pair controller when shown
> pair <MAC_ADDRESS>
> trust <MAC_ADDRESS>
> exit
```

### 2. Test Controllers

```bash
# Install joystick utilities
sudo apt install joystick

# Test each controller
sudo joystick
```

### 3. Configure Joysticks

Create `/etc/udev/rules.d/60-joystick.rules`:

```
# Map PS4 controllers
ACTION=="add", KERNEL=="js*", SUBSYSTEM=="input", ENV{ID_INPUT_JOYSTICK}?"1":
```

### 4. Set Up Controller Mappings

Edit `config/control_mappings.json`:

```json
{
  "minecraft": {
    "controller_1": {
      "up": "UP",
      "down": "DOWN",
      "left": "LEFT",
      "right": "RIGHT",
      "jump": "CROSS"
    }
  }
}
```

## Game Setup

### Minecraft Setup

#### Option 1: Lightweight Minecraft

Use `minetest` instead of full Minecraft:

```bash
sudo apt install minetest
```

Or use a Pi-friendly Minecraft port:
- `minemod`
- Custom Java builds optimized for Pi

#### Option 2: Full Minecraft

```bash
# Download Minecraft Launcher
# Install Java
sudo apt install openjdk-17-jdk

# Configure Java for Pi
# Use ARM64 version of Minecraft
```

### GameCube/Wii Game Setup

#### 1. Prepare Game Files

- Copy .iso files to `/games/gamecube`
- Copy Wii .wbfs files to `/games/wii`

#### 2. Configure Dolphin

Edit `~/.config/dolphin-emu/Settings.ini`:

```
[General]
Backend=Vulkan
Renderer=Vulkan
```

### NES Game Setup

#### 1. Download ROMs

Place .nes files in `/games/nes`

#### 2. Configure RetroArch

Create `~/.config/retroarch/config/retroarch-es.yml`

```yaml
core_path: nestopia
```

## Configuration Files

### 1. Control Mappings

`config/control_mappings.json`:

```json
{
  "minecraft": {
    "controller_1": {
      "dpad": {
        "up": 0,
        "down": 1,
        "left": 2,
        "right": 3
      },
      "buttons": {
        "CROSS": 4,
        "CIRCLE": 5,
        "TRIANGLE": 6,
        "SQUARE": 7
      }
    }
  }
}
```

### 2. Emulator Settings

`config/emulator_settings.json`:

```json
{
  "dolphin": {
    "GC": {
      "controller_count": 4,
      "graphics": "medium"
    },
    "Wii": {
      "controller_count": 2,
      "graphics": "low"
    }
  }
}
```

## Running the Application

### First Time Setup

```bash
# Install the application
pip3 install -e .

# Or run directly
cd /path/to/trashbox-gamer-pygame-interface
python3 main.py
```

### Launch Emulators

```bash
# Launch NES
retroarch -L nestopia /games/nes/game.nes

# Launch GameCube
dolphin -g gamecube /games/gamecube/game.iso

# Launch Wii
dolphin -g wii /games/wii/game.wbfs
```

### Running Minecraft

```bash
# For minetest
minetest

# For Java Minecraft
java -Xmx2G -jar minecraft.jar
```

## Troubleshooting

### Controllers Not Working

```bash
# Check joystick detection
ls /dev/input/js*

# Reboot system
sudo reboot
```

### Emulator Crashing

```bash
# Check dolphin logs
cat ~/.config/dolphin-emu/logs/dolphin-emu.log

# Increase Vulkan backend settings
```

### Performance Issues

```bash
# Check RAM usage
free -h

# Adjust Java heap size
java -Xmx1G -jar minecraft.jar
```

## Optimization Tips

### 1. Graphics Settings

- Use Vulkan backend for Dolphin
- Lower resolution for emulators
- Use 60 FPS limit

### 2. Memory Management

```bash
# Set swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 3. Network Optimization

```bash
# Enable multicast DNS for local games
sudo apt install avahi-daemon
```

## Next Steps

1. Test all controllers
2. Add all your games
3. Configure controller mappings
4. Optimize graphics settings
5. Test multiplayer setup
6. Explore additional features

For more information, see the architecture documentation.
