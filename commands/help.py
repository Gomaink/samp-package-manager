import colorama, sys

def print_help():
    colorama.init()

    print(f"\nUsage: spm [command]\n\
    Package commands:\n\
    \t{colorama.Fore.CYAN}package install <package_name>{colorama.Style.RESET_ALL} - Install a package\n\
    \t{colorama.Fore.CYAN}package remove <package_name>{colorama.Style.RESET_ALL} - Remove a package\n\
    \t{colorama.Fore.CYAN}package list{colorama.Style.RESET_ALL} - List of installed packages\n\
    Gamemode commands:\n\
    \t{colorama.Fore.CYAN}gamemode run{colorama.Style.RESET_ALL} - Execute a gamemode (samp-server)\n\
    \t{colorama.Fore.CYAN}gamemode stop{colorama.Style.RESET_ALL} - Stop a gamemode (samp-server)\n\
    \t{colorama.Fore.CYAN}gamemode build{colorama.Style.RESET_ALL} - Build a gamemode (compile)\n\
    \t{colorama.Fore.CYAN}gamemode restart{colorama.Style.RESET_ALL} - Restart a gamemode (gmx)\n\
    {colorama.Fore.CYAN}spm help{colorama.Style.RESET_ALL} open this menu.")
    colorama.deinit()

def main(args):
    print_help()

if __name__ == "__main__":
    main(sys.argv[1:])