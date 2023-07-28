import sys
import colorama
import os
import subprocess

#Utils
def is_project_initialized():
    return os.path.exists("pawn.json") and os.path.exists("dependencies")

#Main funcs
def gamemode_run():
    samp_server_path = "samp-server.exe"

    if not os.path.exists(samp_server_path):
        print(f"{colorama.Fore.RED}'samp-server.exe' not found in the current directory.{colorama.Style.RESET_ALL}")
        return

    try:
        subprocess.run(samp_server_path, shell=True)
    except KeyboardInterrupt:
        print(f"{colorama.Fore.RED}The process was interrupted by the user.{colorama.Style.RESET_ALL}")
    except Exception as e:
        print(f"{colorama.Fore.RED}Error while running 'samp-server.exe': {str(e)}{colorama.Style.RESET_ALL}")

def gamemode_build():
    colorama.init()

    if not is_project_initialized():
        print(f"{colorama.Fore.RED}The project has not yet started. Run 'spm init' to launch it.{colorama.Style.RESET_ALL}")
        return

    gamemodes_path = "gamemodes"
    if not os.path.exists(gamemodes_path):
        print(f"{colorama.Fore.RED}Gamemodes folder not found. Create the 'gamemodes' folder and place your gamemode files there.{colorama.Style.RESET_ALL}")
        return

    gamemode_name = input("Enter your gamemode name (without the .pwn extension): ")
    gamemode_file = f"{gamemode_name}.pwn"
    gamemode_input_path = os.path.join(gamemodes_path, gamemode_file)

    if not os.path.exists(gamemode_input_path):
        print(f"{colorama.Fore.RED}File {gamemode_file} not found in gamemodes folder.{colorama.Style.RESET_ALL}")
        return

    includes_path = os.path.abspath("dependencies")
    output_path = os.path.abspath("gamemodes")
    pawncc_path = os.path.abspath("compiler/pawncc")

    gamemode_output_path = os.path.join(output_path, gamemode_file)
    compile_command = f"{pawncc_path} -i{includes_path} -o{gamemode_output_path} {gamemode_input_path}"

    print(f"Compiling the gamemode {gamemode_file}...")
    result = subprocess.run(compile_command, shell=True, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(result.stderr)

    colorama.deinit()

def main(args):
    if len(args) < 1:
        print("Usage: spm gamemode <command>")
        print("Commands: run, build, restart, stop")
        return

    action = args[0]
    if action == "run":
        gamemode_run()
    elif action == "build":
        gamemode_build()
    else:
        print(f"{colorama.Fore.RED}Invalid command. Use spm help for more informations.{colorama.Style.RESET_ALL}")

if __name__ == "__main__":
    main(sys.argv[1:])
