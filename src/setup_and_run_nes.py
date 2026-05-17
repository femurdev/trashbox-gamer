import os
import subprocess
import urllib.request
import zipfile

# Constants
ROM_URL = "https://archive.org/download/nes-roms-public-domain/nes-roms-public-domain.zip"
ROM_DIR = "/home/pi/nes_games"
RETROARCH_CONFIG = "/home/pi/.config/retroarch/retroarch.cfg"

def download_roms():
    """Download and extract NES ROMs."""
    print("Downloading NES ROMs...")
    os.makedirs(ROM_DIR, exist_ok=True)
    zip_path = os.path.join(ROM_DIR, "nes_roms.zip")

    # Download the ROMs
    urllib.request.urlretrieve(ROM_URL, zip_path)
    print("Download complete.")

    # Extract the ROMs
    print("Extracting ROMs...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(ROM_DIR)
    os.remove(zip_path)
    print(f"ROMs extracted to {ROM_DIR}")

def install_retroarch():
    """Install RetroArch if not already installed."""
    print("Checking for RetroArch...")
    if subprocess.call(["which", "retroarch"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        print("RetroArch not found. Installing...")
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "install", "-y", "retroarch", "libretro-nestopia"])
        print("RetroArch installed.")
    else:
        print("RetroArch is already installed.")

def configure_retroarch():
    """Set up RetroArch for NES emulation."""
    print("Configuring RetroArch...")
    os.makedirs(os.path.dirname(RETROARCH_CONFIG), exist_ok=True)
    with open(RETROARCH_CONFIG, "w") as config_file:
        config_file.write("""
video_driver = "gl"
audio_driver = "alsa"
input_driver = "udev"
core_updater_buildbot_url = "http://buildbot.libretro.com/nightly/linux/armhf/latest/"
        """)
    print("RetroArch configured.")

def run_game():
    """Run a selected NES game."""
    print("Available NES games:")
    games = [f for f in os.listdir(ROM_DIR) if f.endswith(".nes")]
    for i, game in enumerate(games):
        print(f"{i + 1}. {game}")

    choice = int(input("Select a game to play (number): ")) - 1
    if 0 <= choice < len(games):
        game_path = os.path.join(ROM_DIR, games[choice])
        print(f"Launching {games[choice]}...")
        subprocess.run(["retroarch", "-L", "/usr/lib/libretro/nestopia_libretro.so", game_path])
    else:
        print("Invalid choice.")

def main():
    """Main function."""
    download_roms()
    install_retroarch()
    configure_retroarch()
    run_game()

if __name__ == "__main__":
    main()
