import os
import json
import colorama
import requests
import zipfile
from tqdm import tqdm
from zipfile import ZipFile
import shutil
from .package import package_install

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
            with tqdm(total=total_size, desc=f"Downloading {filename}") as pbar:
                for data in response.iter_content(chunk_size=8192):
                    pbar.update(len(data))
                    file.write(data)
        print(f"{colorama.Fore.MAGENTA}Package {filename} installed successfully.{colorama.Style.RESET_ALL}")

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

def download_samp_stdserver():
    url = "https://github.com/samp-package-manager/samp-stdserver/archive/master.zip"
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        current_dir = os.getcwd()
        zip_path = os.path.join(current_dir, "samp-stdserver-main.zip")

        total_size = 0
        chunk_size = 1024
        total_size = int(response.headers.get('content-length', '0'))

        with open(zip_path, "wb") as f:
            with tqdm(total=total_size, desc="Downloading samp-stdserver") as pbar:
                for data in response.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    pbar.update(len(data))

        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(current_dir)

        extracted_dir = os.path.join(current_dir, "samp-stdserver-main")
        files_in_extracted_dir = os.listdir(extracted_dir)

        readme_path = os.path.join(extracted_dir, "README.md")
        if os.path.exists(readme_path):
            os.remove(readme_path)

        for file in files_in_extracted_dir:
            if file != "README.md":
                file_path = os.path.join(extracted_dir, file)
                shutil.move(file_path, current_dir)

        shutil.rmtree(extracted_dir)

        os.remove(zip_path)
        print(f"{colorama.Fore.MAGENTA}Package samp-stdserver installed successfully.{colorama.Style.RESET_ALL}")
    else:
        print("Failed to download samp-stdserver files.")
    
#Main funcs
def init():
    if os.path.exists("dependencies") or os.path.exists("pawn.json"):
        print(f"{colorama.Fore.RED}The project has already been started.{colorama.Style.RESET_ALL}")
        return

    response = input("Do you already have a server structure in the current directory? (y/n): ").lower()
    if response == 'y':
        create_dependencies_folder()
        create_pawn_json()
        print("Installing standard library...")
        package_install("samp-package-manager/samp-stdlib")

        print("Installing compiler files...")
        os.makedirs("compiler", exist_ok=True)
        download_compiler_files()

        print(f"{colorama.Fore.GREEN}Project files successfully created!{colorama.Style.RESET_ALL}")
    elif response == 'n':
        create_dependencies_folder()
        create_pawn_json()
        print("Installing standard server...")
        download_samp_stdserver()
        print("Installing standard library...")
        package_install("samp-package-manager/samp-stdlib")

        print("Installing compiler files...")
        os.makedirs("compiler", exist_ok=True)
        download_compiler_files()

        print(f"{colorama.Fore.GREEN}Project files successfully created!{colorama.Style.RESET_ALL}")
    else:
        init()
        return

if __name__ == "__main__":
    init()
