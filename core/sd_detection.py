import os
import platform
import subprocess
from colorama import init, Fore
init(autoreset = True)

currentOS = platform.system()

EXPECTED_WII_DIRS = ["apps", "private", "wads"]

def detect_sd_cards():
    sd_cards = []

    if currentOS != "Windows":
        print("Only Windows SD card detection is supported right now.")
        return sd_cards

    import json

    powershell_script = """
    Get-WmiObject Win32_DiskDrive | ForEach-Object {
        $drive = $_
        $partitions = ($drive | Get-WmiObject -Query "ASSOCIATORS OF {Win32_DiskDrive.DeviceID='$($drive.DeviceID)'} WHERE AssocClass = Win32_DiskDriveToDiskPartition")
        foreach ($partition in $partitions) {
            $logical = ($partition | Get-WmiObject -Query "ASSOCIATORS OF {Win32_DiskPartition.DeviceID='$($partition.DeviceID)'} WHERE AssocClass = Win32_LogicalDiskToPartition")
            foreach ($l in $logical) {
                [PSCustomObject]@{
                    DriveLetter = $l.DeviceID
                    Caption     = $drive.Caption
                    MediaType   = $drive.MediaType
                    Interface   = $drive.InterfaceType
                }
            }
        }
    } | ConvertTo-Json
    """
    output = run_powershell_command(powershell_script)

    if output:
        try:
            entries = json.loads(output)
            if isinstance(entries, dict):
                entries = [entries]
            for entry in entries:
                caption = entry.get("Caption", "").lower()
                media_type = entry.get("MediaType", "").lower()
                if any(keyword in caption for keyword in ["sd", "secure digital"]) or \
                   any(keyword in media_type for keyword in ["sd", "secure digital"]):
                    drive_letter = entry.get("DriveLetter")
                    if drive_letter:
                        sd_cards.append(drive_letter)
        except Exception as e:
            print(Fore.RED + f"Failed to parse PowerShell output: {e}")

    return sd_cards


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

def get_volume_label(drive_letter):
    command = f"Get-Volume -DriveLetter {drive_letter[0]} | Select-Object -ExpandProperty FileSystemLabel"
    return run_powershell_command(command)

def is_wii_formatted(path):
    existing = os.listdir(path)
    for folder in EXPECTED_WII_DIRS:
        if folder in existing:
            return True
    return False

def create_wii_folders(path):
    for folder in EXPECTED_WII_DIRS:
        full_path = os.path.join(path, folder)
        try:
            os.makedirs(full_path, exist_ok=True)
            print(f"Created: {full_path}")
        except Exception as e:
            print(f"Failed to create {folder}: {e}")

def check_and_setup_card(drive_path):
    print(f"\nChecking structure on {drive_path}...")
    if is_wii_formatted(drive_path):
        print("SD card already contains expected Wii folders.")
    else:
        print(Fore.YELLOW + "SD card does not appear to be Wii-formatted.")
        user_input = print("Would you like to create the default Wii folder structure? (y/n): ").strip().lower()
        if user_input == 'y':
            create_wii_folders(drive_path)
            print(Fore.GREEN + "SD card is now Wii-ready!")
        else:
            print("Skipping setup for this drive.")

    # SD card setup complete.

if __name__ == "__main__":
    cards = detect_sd_cards()
    if cards:
        for card in cards:
            print(f"Found: {card}")
            label = get_volume_label(card)
            if label:
                print(f"Label: {label}")
                check_and_setup_card(card)
    else:
        print(Fore.RED + "No SD cards detected... is your SD card inserted?")