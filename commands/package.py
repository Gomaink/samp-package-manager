import os
import sys
import requests
import colorama
import json
from alive_progress import alive_bar

#Utils
def is_project_initialized():
    return os.path.exists("pawn.json") and os.path.exists("dependencies")

def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        return True
    return False

#Json funcs
def load_pawn_json():
    pawn_json_file = "pawn.json"

    if not os.path.exists(pawn_json_file):
        return {"dependencies": [], "dependencies_files": {}}

    with open(pawn_json_file, 'r') as file:
        return json.load(file)

def save_pawn_json(data):
    pawn_json_file = "pawn.json"
    with open(pawn_json_file, 'w') as file:
        json.dump(data, file, indent=4)

def update_pawn_json(package_name, downloaded_files):
    with open("pawn.json", "r") as json_file:
        data = json.load(json_file)

    data["dependencies"].append(package_name)
    data["dependencies_files"][package_name] = downloaded_files

    with open("pawn.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

#Package funcs
def is_valid_package_name(package_name):
    return '/' in package_name

def get_package_files(package_name):
    data = load_pawn_json()
    dependencies_files = data.get("dependencies_files", {})
    return dependencies_files.get(package_name, [])

def remove_package_files(package_files):
    for filename in package_files:
        filepath = os.path.join("dependencies", filename)
        if os.path.exists(filepath):
            os.remove(filepath)

def is_package_installed(package_name):
    if not is_project_initialized():
        return False

    with open("pawn.json", "r") as json_file:
        data = json.load(json_file)

    return package_name in data["dependencies"]


#Main funcs
def package_install(package_name):
    colorama.init()

    try:
        if not is_project_initialized():
            print(f"{colorama.Fore.RED}The project has not yet started. Run 'spm init' to launch it.{colorama.Style.RESET_ALL}")
            return

        if is_package_installed(package_name):
            print(f"{colorama.Fore.RED}Package {package_name} is already installed.{colorama.Style.RESET_ALL}")
            return

        user, repo = package_name.split('/')
        url = f"https://api.github.com/repos/{user}/{repo}/contents"

        response = requests.get(url)
        if response.status_code == 200:
            files = response.json()
            downloaded_files = []
            with alive_bar(len(files), title=f"Downloading {package_name}", bar="blocks", spinner="dots_waves2") as bar:
                for file in files:
                    if file.get('name', '').endswith('.inc'):
                        download_url = file['download_url']
                        filename = os.path.basename(download_url)
                        filepath = os.path.join("dependencies", filename)
                        if download_file(download_url, filepath):
                            downloaded_files.append(filename)
                        else:
                            print(f"{colorama.Fore.RED}Failed to download file: {filename}{colorama.Style.RESET_ALL}")
                    bar()
            update_pawn_json(package_name, downloaded_files)
            print(f"{colorama.Fore.MAGENTA}Package {package_name} installed successfully.{colorama.Style.RESET_ALL}")

        else:
            print(f"{colorama.Fore.RED}Repository not found.{colorama.Style.RESET_ALL}")

    except ValueError:
        print(f"{colorama.Fore.RED}Invalid repository path. Use the format 'user/repository'.{colorama.Style.RESET_ALL}")

    colorama.deinit()

def package_remove(package_name):
    colorama.init()

    if not is_project_initialized():
        print(f"{colorama.Fore.RED}The project has not yet started. Run 'python app.py init' to launch it.{colorama.Style.RESET_ALL}")
        return

    data = load_pawn_json()
    dependencies = data.get("dependencies", [])
    package_files = get_package_files(package_name)

    if package_name and package_name in dependencies:
        if package_files:
            remove_package_files(package_files)

        dependencies.remove(package_name)
        del data["dependencies_files"][package_name]
        save_pawn_json(data)

        print(f"{colorama.Fore.MAGENTA}Package {package_name} removed successfully.{colorama.Style.RESET_ALL}")
    elif package_files:
        remove_package_files(package_files)
        print(f"{colorama.Fore.GREEN}File(s) {', '.join(package_files)} removed successfully.{colorama.Style.RESET_ALL}")
    else:
        print(f"{colorama.Fore.RED}Package or file {package_name} not found.{colorama.Style.RESET_ALL}")

    colorama.deinit()

def package_list():
    colorama.init()

    if not is_project_initialized():
        print(f"{colorama.Fore.RED}The project has not yet started. Run 'python app.py init' to launch it.{colorama.Style.RESET_ALL}")
        return

    data = load_pawn_json()
    dependencies = data.get("dependencies", [])
    dependencies_files = data.get("dependencies_files", {})

    if len(dependencies) == 0:
        print(f"{colorama.Fore.RED}No packages installed.{colorama.Style.RESET_ALL}")
    else:
        print("\nInstalled packages:")
        for package_name in dependencies:
            print(f"{colorama.Fore.YELLOW}- {package_name}{colorama.Style.RESET_ALL}")
            package_files = dependencies_files.get(package_name, [])
            if package_files:
                for filename in package_files:
                    print(f"  - {filename}")

    colorama.deinit()

def main(args):
    if len(args) < 1:
        print("Usage: spm package <command>")
        print("Commands: install, remove, list")
        return

    action = args[0]
    if action == "install":
        if len(args) < 2:
            print("Usage: spm package install <package_name>")
            return
        package_install(args[1])
    elif action == "remove":
        if len(args) < 2:
            print("Usage: spm package remove <package_name>")
            return
        package_remove(args[1])
    elif action == "list":
        package_list()
    else:
        print(f"{colorama.Fore.RED}Invalid command. Use spm help for more informations.{colorama.Style.RESET_ALL}")

if __name__ == "__main__":
    main(sys.argv[1:])
