import os
import platform
import subprocess
import json
from colorama import init, Fore

# Initialize colorama for cross-platform colored output
init(autoreset=True)

EXPECTED_WII_DIRS = ["apps", "private", "wads"]

def run_powershell_command(command):
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"PowerShell Error: {e.stderr}")
        return None

def detect_sd_cards():
    """Detects and returns a list of SD card drive letters on Windows."""
    if platform.system() != "Windows":
        print("Only Windows SD card detection is supported right now.")
        return []
    sd_cards = []
    powershell_script = """
    Get-Volume | Where-Object DriveType -eq 'Removable' | Select-Object DriveLetter, FileSystemLabel, DriveType | ConvertTo-Json
    """
    output = run_powershell_command(powershell_script)

    if output:
        try:
            entries = json.loads(output)
            if not isinstance(entries, list):
                entries = [entries]
            
            for entry in entries:
                drive_letter = entry.get("DriveLetter")
                if drive_letter:
                    sd_cards.append(f"{drive_letter}:\\")
        except json.JSONDecodeError as e:
            print(Fore.RED + f"Failed to parse PowerShell output: {e}")

    return sd_cards

def is_wii_formatted(path):
    """Checks if the given path contains the expected Wii directories."""
    for folder in EXPECTED_WII_DIRS:
        full_path = os.path.join(path, folder)
        if not os.path.isdir(full_path):
            return False
    return True

def create_wii_folders(path):
    """Creates the standard Wii folder structure at the specified path."""
    print(Fore.YELLOW + "Creating Wii folder structure...")
    for folder in EXPECTED_WII_DIRS:
        full_path = os.path.join(path, folder)
        try:
            os.makedirs(full_path, exist_ok=True)
            print(Fore.GREEN + f"Created: {full_path}")
        except Exception as e:
            print(Fore.RED + f"Failed to create {folder}: {e}")

def check_and_setup_card(drive_path):
    """Prompts the user to set up a Wii SD card if needed."""
    print(f"\nChecking structure on {drive_path}...")
    
    if not os.path.exists(drive_path):
        print(Fore.RED + f"Drive path {drive_path} does not exist. Skipping.")
        return

    if is_wii_formatted(drive_path):
        print(Fore.GREEN + "SD card already contains the expected Wii folder structure.")
    else:
        print(Fore.YELLOW + "SD card does not appear to be Wii-formatted.")
        user_input = input("Would you like to create the default Wii folder structure? (y/n): ").strip().lower()
        if user_input == 'y':
            create_wii_folders(drive_path)
            print(Fore.GREEN + "SD card is now Wii-ready!")
        else:
            print("Skipping setup for this drive.")

if __name__ == "__main__":
    cards = detect_sd_cards()
    if cards:
        print(Fore.CYAN + "SD cards detected:")
        for card_path in cards:
            print(f"- {card_path}")
            check_and_setup_card(card_path)
    else:
        print(Fore.RED + "No removable drives detected. Is your SD card inserted?")