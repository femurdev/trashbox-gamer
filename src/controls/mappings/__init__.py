"""
Controller mapping configuration
"""
import json
import os

CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ControlMapping:
    """Handles controller mappings and configurations"""

    def __init__(self):
        self.config_file = os.path.join(
            CONFIG_DIR, 'config', 'control_mappings.json'
        )
        self.load_config()

    def load_config(self):
        """Load control mappings from config file"""
        if not os.path.exists(self.config_file):
            self.default_config = {
                "minecraft": {
                    "keyboard": {
                        "up": "w",
                        "down": "s",
                        "left": "a",
                        "right": "d",
                        "jump": "space",
                        "sneak": "left_shift",
                        "sprint": "right_shift",
                    },
                    "controller_1": {
                        "up": "UP",
                        "down": "DOWN",
                        "left": "LEFT",
                        "right": "RIGHT",
                        "jump": "CROSS",
                        "sneak": "CIRCLE",
                        "sprint": "TRIANGLE",
                    }
                },
                "emulator": {
                    "controller_2": {
                        "dpad": {
                            "up": 0,
                            "down": 1,
                            "left": 2,
                            "right": 3,
                        },
                        "buttons": {
                            "A": 4,
                            "B": 5,
                            "X": 6,
                            "Y": 7,
                            "L1": 8,
                            "R1": 9,
                            "L2": 10,
                            "R2": 11,
                        }
                    },
                    "controller_3": {
                        "dpad": {
                            "up": 0,
                            "down": 1,
                            "left": 2,
                            "right": 3,
                        },
                        "buttons": {
                            "A": 4,
                            "B": 5,
                            "X": 6,
                            "Y": 7,
                            "L1": 8,
                            "R1": 9,
                            "L2": 10,
                            "R2": 11,
                        }
                    }
                }
            }
            self.save_config()

    def save_config(self):
        """Save current mappings to config file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.default_config, f, indent=2)

    def get_mapping(self, game: str, controller: str, input_type: str):
        """Get mapping for specific game, controller, and input type"""
        game_config = self.default_config.get(game, {})
        controller_config = game_config.get(controller, {})

        if input_type == 'keyboard':
            return controller_config.get('keyboard', {})
        elif input_type == 'controller':
            return controller_config.get('controller', {})
        return {}

    def set_mapping(self, game: str, controller: str, input_type: str, mapping: dict):
        """Set new mapping"""
        if game not in self.default_config:
            self.default_config[game] = {}

        if controller not in self.default_config[game]:
            self.default_config[game][controller] = {}

        self.default_config[game][controller][input_type] = mapping
        self.save_config()
