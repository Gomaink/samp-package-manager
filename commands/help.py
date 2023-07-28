import colorama, sys

def print_help():
    colorama.init()

    print(f"\nUsage: spm [command]\n\
    Main commands:\n\
    \t{colorama.Fore.CYAN}init{colorama.Style.RESET_ALL} - Creates the required files\n\
    \t{colorama.Fore.CYAN}help{colorama.Style.RESET_ALL} - Open this menu\n\
    Package commands:\n\
    \t{colorama.Fore.CYAN}package install <package_name>{colorama.Style.RESET_ALL} - Install a package\n\
    \t{colorama.Fore.CYAN}package remove <package_name>{colorama.Style.RESET_ALL} - Remove a package\n\
    \t{colorama.Fore.CYAN}package list{colorama.Style.RESET_ALL} - List of installed packages\n\
    Gamemode commands:\n\
    \t{colorama.Fore.CYAN}gamemode run{colorama.Style.RESET_ALL} - Execute a gamemode (samp-server)\n\
    \t{colorama.Fore.CYAN}gamemode build{colorama.Style.RESET_ALL} - Build a gamemode (compile)\n")
    colorama.deinit()

def main(args):
    print_help()

if __name__ == "__main__":
    main(sys.argv[1:])