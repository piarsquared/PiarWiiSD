from colorama import init, Fore, Style
import os

try:
    from core.sd_detection import detect_sd_cards
except ImportError:
    print(f"{Fore.RED}Error: core.sd_detection module not found.{Style.RESET_ALL}")
    detect_sd_cards = lambda: []

try:
    from gui.main_gui import launch_gui
except Exception as e:
    launch_gui = lambda sd_cards: print("GUI could not be launched.")


script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "assets", "piarpurple.json")

init(autoreset=True)

def main():
    banner = Fore.MAGENTA + r"""
   ___    _               _      __   _    _    ____   ___ 
  / _ \  (_) ___ _  ____ | | /| / /  (_)  (_)  / __/  / _ \
 / ___/ / / / _ `/ / __/ | |/ |/ /  / /  / /  _\ \   / // / 
/_/    /_/  \_,_/ /_/    |__/|__/  /_/  /_/  /___/  /____/ 
                                                           """ + Style.RESET_ALL

    print(banner)
    print(Style.BRIGHT + Fore.MAGENTA + "PiarWiiSD v1.0.0 by Piarsquared :3\n" + Style.RESET_ALL) # If you're reading this, I hope you have a great day! :D

    sd_cards = detect_sd_cards()
    launch_gui(sd_cards)

if __name__ == "__main__":
    main()