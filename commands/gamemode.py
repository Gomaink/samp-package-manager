import sys
import colorama

def gamemode_run():
    pass

def gamemode_build():
    pass

def gamemode_restart():
    pass

def gamemode_stop():
    pass

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
    elif action == "restart":
        gamemode_restart()
    elif action == "stop":
        gamemode_stop()
    else:
        print(f"{colorama.Fore.RED}Invalid command. Use spm help for more informations.{colorama.Style.RESET_ALL}")

if __name__ == "__main__":
    main(sys.argv[1:])
