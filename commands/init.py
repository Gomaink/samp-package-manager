import os
import json
import colorama

def create_dependencies_folder():
    if not os.path.exists("dependencies"):
        os.makedirs("dependencies")

def create_pawn_json():
    data = {
        "dependencies": [],
        "dependencies_files": {}
    }
    with open("pawn.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

def init():
    if os.path.exists("dependencies") or os.path.exists("pawn.json"):
        print(f"{colorama.Fore.RED}The project has already been started. The 'pawn.json' file and/or the 'dependencies' folder already exist.{colorama.Style.RESET_ALL}")
        return

    create_dependencies_folder()
    create_pawn_json()
    print(f"{colorama.Fore.GREEN}Project launched successfully! The file 'pawn.json' and the folder 'dependencies' were created.{colorama.Style.RESET_ALL}")

if __name__ == "__main__":
    init()
