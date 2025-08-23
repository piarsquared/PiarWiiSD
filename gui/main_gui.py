import customtkinter as ctk
import os
from colorama import Fore, Style
from main import json_path
from PIL import Image, ImageTk
from main import script_dir
from core.sd_detection import detect_sd_cards, check_and_setup_card

ICON_PATH = os.path.join(script_dir, "assets", "favicon.ico")

def launch_gui(sd_cards=None):

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme(json_path)
    print(Fore.YELLOW + "Starting PiarWiiSD GUI...")

    app = ctk.CTk()
    app.title("PiarWiiSD")
    app.geometry("1280x720")
    sd_cards_list = [*sd_cards] if sd_cards else []
    dropdown_values = sd_cards_list if sd_cards_list else ["No SD cards detected."]

    if sd_cards_list:
        print(Fore.CYAN + f"Detected SD cards: {', '.join(sd_cards_list)}")
    else:
        print(Fore.RED + "No SD cards detected.")

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    def on_sd_selected(selected_value):
        print(Fore.YELLOW + f"Selected SD card: {selected_value}")
        dialog = FileSystemDialog(app)
        result = dialog.show()

        if result:
            print("User clicked Yes")
        else:
            print("User clicked No or closed the dialog")

    titleText = ctk.CTkLabel(app, text="PiarWiiSD", font=("Arial", 100, "bold", "italic"))
    titleText.grid(row=0, column=0, padx=0, pady=0, sticky="n")

    dropdownMenu = ctk.CTkOptionMenu(
            app,
            values=dropdown_values,
            width=300,
            height=50,
            command=lambda: "fortnite burger"
        )
    dropdownMenu.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

    def refreshButtonCommand():
        if sd_cards:
            print(Fore.CYAN + f"Detected SD cards: {', '.join(sd_cards)}")
            
            if "C:" in sd_cards:
                print(Fore.RED + "C: Drive selected. This might be your system drive.")

        else:
            print(Fore.RED + "Please make sure an SD card is inserted.")
        new_sd_cards = detect_sd_cards()
        sd_cards_list.clear()
        sd_cards_list.extend(new_sd_cards)
        dropdown_values[:] = sd_cards_list if sd_cards_list else ["No SD cards detected."]
        dropdownMenu.configure(values=dropdown_values)
        print(Fore.CYAN + f"Detected SD cards: {', '.join(sd_cards_list)}" if sd_cards_list else Fore.RED + "No SD cards detected.")

    refreshButton = ctk.CTkButton(app, text="Refresh SD List", command=refreshButtonCommand)
    refreshButton.grid(row=0, column=0, padx=20, pady=80, sticky="nw")

    class FileSystemDialog(ctk.CTkToplevel):
        def __init__(self, parent, title="Confirmation", message="Are you sure you would like to setup the SD card?"):
            super().__init__(parent)
            self.title("Dialog")
            self.geometry("500x150")
            self.transient(parent)
            self.grab_set()

            self.result = None

            self.label = ctk.CTkLabel(self, text=message, font=("Arial", 14))
            self.label.pack(pady=20)

            self.button_frame = ctk.CTkFrame(self)
            self.button_frame.pack(pady=10)

            self.yes_button = ctk.CTkButton(self.button_frame, text="Yes", command=self.on_yes)
            self.yes_button.pack(side="left", padx=10)

            self.no_button = ctk.CTkButton(self.button_frame, text="No", command=self.on_no)
            self.no_button.pack(side="right", padx=10)

            self.protocol("WM_DELETE_WINDOW", self.on_no)

        def on_yes(self):
            self.result = True
            self.destroy()

        def on_no(self):
            self.result = False
            self.destroy()

        def show(self):
            self.wait_window(self)
            return self.result

    statusBox = ctk.CTkTextbox(app, width=500, height=200, font=("Arial", 20))
    statusBox.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
    statusBox.insert("0.0", "Welcome to the PiarWiiSD GUI. Status updates will be shown here alongside the CMD line.\n")
    statusBox.configure(state="disabled")

    setupSDCardButton = ctk.CTkButton(app, text="Setup SD Card", command=lambda: on_sd_selected(sd_cards))
    setupSDCardButton.grid(row=0, column=0, padx=20, pady=50, sticky="w")

    def update_status(message):
        statusBox.configure(state="normal")
        statusBox.insert("end", message + "\n")
        statusBox.configure(state="disabled")

    app.iconbitmap(ICON_PATH)

    print(Fore.LIGHTBLUE_EX + "GUI Launched!")
    app.resizable(False, False)
    app.mainloop()