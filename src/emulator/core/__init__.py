"""
Emulator core module - Interface for connecting to external emulators
"""
import os
import subprocess
import threading
from abc import ABC, abstractmethod


class Emulator(ABC):
    """Abstract base class for all emulators"""

    def __init__(self, name: str, executable: str):
        self.name = name
        self.executable = executable
        self.process = None
        self.running = False

    @abstractmethod
    def start(self, game_path: str):
        """Start the emulator with a game"""
        pass

    @abstractmethod
    def stop(self):
        """Stop the emulator"""
        pass

    @abstractmethod
    def get_status(self) -> bool:
        """Check if emulator is running"""
        pass

    @abstractmethod
    def get_log(self) -> str:
        """Get emulator logs"""
        pass


class NESEmulator(Emulator):
    """NES emulator using RetroArch or Nestopia"""

    def __init__(self):
        # Try RetroArch first, then Nestopia
        executables = ['retroarch', 'nestopia', 'nestopia-fb', 'nesine']
        for exe in executables:
            if os.path.exists(exe):
                super().__init__('NES', exe)
                return
        # Default path
        super().__init__('NES', 'retroarch')

    def start(self, game_path: str):
        """Launch NES game"""
        # Launch RetroArch with NES core
        cmd = [
            self.executable,
            '-c', f'/config/retroarch/es_emulationstation.yml',
            '-L', 'nestopia',
            '-f', game_path
        ]
        self.process = subprocess.Popen(cmd)
        self.running = True

    def stop(self):
        """Stop NES emulation"""
        if self.process:
            self.process.terminate()
            self.process = None
            self.running = False

    def get_status(self) -> bool:
        return self.running

    def get_log(self) -> str:
        return "NES Emulator Log"


class DolphinEmulator(Emulator):
    """Dolphin emulator for GameCube, Wii, and Wii U"""

    def __init__(self, instance_name: str):
        self.instance_name = instance_name
        self.instances = [
            'GC-1',  # GameCube Instance 1
            'GC-2',  # GameCube Instance 2
            'Wii-1', # Wii Instance 1
            'Wii-2', # Wii Instance 2
            'WiiU-1',# Wii U Instance 1
        ]
        self.game_type = None

        # Try to find Dolphin
        executable = '/usr/bin/dolphin'
        if not os.path.exists(executable):
            executable = 'dolphin-qt'

        super().__init__(f'Dolphin {self.instance_name}', executable)

    def set_game_type(self, game_type: str):
        """Set game type for Dolphin"""
        self.game_type = game_type
        # Map game type to Dolphin folder
        self.game_type_mapping = {
            'gamecube': '/games/gamecube',
            'wii': '/games/wii',
            'wiiu': '/games/wiiu',
        }

    def start(self, game_path: str):
        """Launch Dolphin with specific game"""
        dolphin_path = self.executable

        # Platform-specific flags
        if self.game_type == 'gamecube':
            args = ['-g', 'gamecube']
        elif self.game_type == 'wii':
            args = ['-g', 'wii']
        elif self.game_type == 'wiiu':
            args = ['-g', 'wiiu']
        else:
            args = []

        cmd = [dolphin_path] + args + [game_path]

        self.process = subprocess.Popen(cmd)
        self.running = True

    def stop(self):
        """Stop Dolphin instance"""
        if self.process:
            self.process.terminate()
            self.process = None
            self.running = False

    def get_status(self) -> bool:
        return self.running

    def get_log(self) -> str:
        return "Dolphin Emulator Log"


class EmulatorManager:
    """Manages multiple emulator instances"""

    def __init__(self):
        self.emulators = {}
        self.emulator_types = {
            'nes': NESEmulator(),
            'gamecube': DolphinEmulator('GC'),
            'wii': DolphinEmulator('Wii'),
            'wiiu': DolphinEmulator('WiiU'),
        }

        # Create instance pool
        self._create_instance_pool()

    def _create_instance_pool(self):
        """Create multiple Dolphin instances if needed"""
        # Create second GameCube instance
        gc2 = DolphinEmulator('GC-2')
        gc2.set_game_type('gamecube')
        self.emulators['gamecube-2'] = gc2

        # Create second Wii instance
        wii2 = DolphinEmulator('Wii-2')
        wii2.set_game_type('wii')
        self.emulators['wii-2'] = wii2

        # Create Wii U instance
        wiiu = DolphinEmulator('WiiU')
        wiiu.set_game_type('wiiu')
        self.emulators['wiiu'] = wiiu

    def get_emulator(self, platform: str, instance: str = None):
        """Get an emulator instance"""
        if platform not in self.emulator_types:
            raise ValueError(f"Unknown platform: {platform}")

        if instance:
            key = f"{platform}-{instance}"
            return self.emulators.get(key)
        else:
            return self.emulator_types[platform]

    def launch(self, platform: str, game_path: str):
        """Launch a game on specified platform"""
        emulator = self.get_emulator(platform)
        emulator.start(game_path)
        return emulator

    def stop_all(self):
        """Stop all running emulators"""
        for emulator in self.emulators.values():
            emulator.stop()

    def get_running_count(self) -> int:
        """Get count of running emulators"""
        return sum(1 for e in self.emulators.values() if e.running)
