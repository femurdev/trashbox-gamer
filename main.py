"""
Main entry point for the Trashbox Gamer application
Run with: python main.py
"""
from src.window_manager import MainGame


def main():
    """Main entry point"""
    game = MainGame()
    game.switch_window("menu")
    game.run()


if __name__ == "__main__":
    main()
