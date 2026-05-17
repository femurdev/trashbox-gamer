"""
Handles input from keyboard and PS4 controllers
Provides unified input abstraction across all devices
"""
import pygame
import sdl2.ext


class InputHandler:
    def __init__(self):
        self.key_state = {key: False for key in pygame.key.get_pressed()}
        self.button_state = {}
        self.controllers = {}
        self.joystick_count = 0

        # Map controller joystick indices to logical controller names
        self.controller_map = {
            0: 'controller_1',  # Minecraft player
            1: 'controller_2',  # Emulator 1 (Dolphin)
            2: 'controller_3',  # Emulator 2 (Dolphin)
        }

        # Initialize controller mapping
        self._init_controllers()

    def _init_controllers(self):
        """Initialize and map all connected controllers"""
        # Wait for joystick events
        event = pygame.event.wait(timeout=2.0)
        if event.type == pygame.JOYDEVICEADDED:
            pygame.joystick.Joystick(event.axis).init()

        self.joystick_count = pygame.joystick.get_count()

        # Create controller instances
        for i in range(self.joystick_count):
            try:
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                controller_name = self.controller_map.get(i, f'controller_{i}')
                self.controllers[controller_name] = {
                    'joystick': joystick,
                    'name': joystick.get_name()
                }
            except Exception:
                continue

    def _get_button_mapping(self, controller_name):
        """Get button mappings for a controller"""
        mappings = {
            'UP': 0,      # D-pad up
            'DOWN': 1,    # D-pad down
            'LEFT': 2,    # D-pad left
            'RIGHT': 3,   # D-pad right
            'CROSS': 4,   # X button (select)
            'CIRCLE': 5,  # O button
            'TRIANGLE': 6, # Y button
            'SQUARE': 7,  # B button
            'L1': 8,      # L1
            'R1': 9,      # R1
            'L2': 10,     # L2
            'R2': 11,     # R2
            'L3': 12,     # L3
            'R3': 13,     # R3
            'SHARE': 14,  # Share button
            'OPTIONS': 15, # Options button
        }
        return mappings

    def get_button(self, controller_name, button_name):
        """Get state of a specific button"""
        controller = self.controllers.get(controller_name)
        if not controller:
            return False

        mappings = self._get_button_mapping(controller_name)
        if button_name not in mappings:
            return False

        joystick = controller['joystick']
        button_index = mappings[button_name]
        return joystick.get_button(button_index)

    def get_button_states(self, controller_name=None):
        """Get states of all buttons for a controller or all controllers"""
        states = {}

        if controller_name:
            states[controller_name] = {}
            if controller_name in self.controllers:
                joystick = self.controllers[controller_name]['joystick']
                mappings = self._get_button_mapping(controller_name)
                for btn_name, btn_index in mappings.items():
                    states[controller_name][btn_name] = joystick.get_button(btn_index)
        else:
            for name, controller_data in self.controllers.items():
                states[name] = {}
                joystick = controller_data['joystick']
                mappings = self._get_button_mapping(name)
                for btn_name, btn_index in mappings.items():
                    states[name][btn_name] = joystick.get_button(btn_index)

        return states

    def get_pressed_keys(self):
        """Get current state of all pressed keys"""
        return self.key_state.copy()

    def _get_joystick_state(self, controller_name):
        """Get state of all buttons and axes for a joystick"""
        controller = self.controllers.get(controller_name)
        if not controller:
            return None

        joystick = controller['joystick']
        state = {
            'buttons': {
                'UP': False,
                'DOWN': False,
                'LEFT': False,
                'RIGHT': False,
                'CROSS': False,
                'CIRCLE': False,
                'TRIANGLE': False,
                'SQUARE': False,
                'L1': False,
                'R1': False,
                'L2': False,
                'R2': False,
                'L3': False,
                'R3': False,
            },
            'axes': {}
        }

        # Read button states
        for btn_name, btn_index in self._get_button_mapping(controller_name).items():
            state['buttons'][btn_name] = joystick.get_button(btn_index)

        # Read axes
        for i, axis in enumerate(joystick.get_axis()):
            state['axes'][f'axis_{i}'] = axis

        return state

    def poll_events(self):
        """Poll events and update input state"""
        # Handle joystick events
        while pygame.event.poll().type in (pygame.NOEVENT,):
            pass

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            self.key_state[event.key] = True
        elif event.type == pygame.KEYUP:
            self.key_state[event.key] = False
        elif event.type == pygame.JOYBUTTONDOWN:
            # Initialize new joystick if needed
            if event.axis not in self.controllers:
                try:
                    new_joystick = pygame.joystick.Joystick(event.axis)
                    new_joystick.init()
                    controller_name = self.controller_map.get(
                        event.axis, f'controller_{event.axis}'
                    )
                    self.controllers[controller_name] = {
                        'joystick': new_joystick,
                        'name': new_joystick.get_name()
                    }
                except Exception:
                    pass
        elif event.type == pygame.JOYBUTTONUP:
            pass

        return True

    def get_all_input_state(self):
        """Get combined input state from all devices"""
        input_state = {
            'keys': self.key_state.copy(),
            'controllers': {}
        }

        for controller_name in self.controllers:
            input_state['controllers'][controller_name] = self._get_joystick_state(
                controller_name
            )

        return input_state
