import os
import json
import colorama
import requests
import zipfile
import shutil
from .package import package_install
from alive_progress import alive_bar

#Utils
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

def download_compiler_files():
    colorama.init()

    release_url = "https://github.com/pawn-lang/compiler/releases/download/v3.10.10/"
    filename = get_compiler_by_platform()
    url = release_url + filename
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        filepath = os.path.join("compiler", filename)
        with open(filepath, "wb") as file:
            total_size = int(response.headers.get('content-length'))
            with alive_bar(total_size, title=f"Downloading {filename}", bar="blocks", spinner="dots_waves2") as bar:
                for data in response.iter_content(chunk_size=8192):
                    bar(len(data))
                    file.write(data)
        print(f"{colorama.Fore.MAGENTA}Package: {filename} installed successfully.{colorama.Style.RESET_ALL}")

        extract_path = os.path.join("compiler", "extracted")
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(extract_path)

        for root, _, files in os.walk(extract_path):
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join("compiler", file)
                os.rename(src_file, dest_file)

        shutil.rmtree(extract_path)

    else:
        print(f"{colorama.Fore.RED}Failed to download: {filename}{colorama.Style.RESET_ALL}")
    colorama.deinit()

def get_compiler_by_platform():
    import platform
    system = platform.system()
    machine = platform.machine()
    
    if system == "Windows":
        return "pawnc-3.10.10-windows.zip"
    elif system == "Linux":
        return "pawnc-3.10.10-linux.gz"
    elif system == "Darwin" and machine == "x86_64":
        return "pawnc-3.10.10-macos.zip"
    else:
        return None

#Main funcs
def init():
    if os.path.exists("dependencies") or os.path.exists("pawn.json"):
        print(f"{colorama.Fore.RED}The project has already been started. The 'pawn.json' file and/or the 'dependencies' folder already exist.{colorama.Style.RESET_ALL}")
        return

    create_dependencies_folder()
    create_pawn_json()
    print("Installing standard library...")
    package_install("pawn-lang/samp-stdlib")

    print("Installing compiler files...")
    os.makedirs("compiler", exist_ok=True)
    download_compiler_files()

    print(f"{colorama.Fore.GREEN}Project launched successfully! The file 'pawn.json', folder 'dependencies', and 'compiler' folder were created.{colorama.Style.RESET_ALL}")

if __name__ == "__main__":
    init()
