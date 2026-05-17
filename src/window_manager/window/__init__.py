"""
Package for window management
"""
from src.window_manager.window.base import BaseWindow
from src.window_manager.window.game_window import GameWindow
from src.window_manager.window.menu_window import MenuWindow

__all__ = ['BaseWindow', 'GameWindow', 'MenuWindow']
