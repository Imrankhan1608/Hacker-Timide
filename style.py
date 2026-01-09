import os
import time
import shutil

# ===== COULEURS =====
BLUE    = "\033[94m"
PURPLE  = "\033[95m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
RED     = "\033[91m"
RESET   = "\033[0m"
BOLD    = "\033[1m"

# ===== NETTOYER L'ÉCRAN =====
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ===== LARGEUR TERMINAL =====
def terminal_width():
    return shutil.get_terminal_size().columns

# ===== BANNIÈRE =====
def banner():
    art = [
        "██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ ████████╗██╗███╗   ███╗██╗██████╗ ███████╗",
        "██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗╚══██╔══╝██║████╗ ████║██║██╔══██╗██╔════╝",
        "███████║███████║██║     █████╔╝ █████╗  ██████╔╝   ██║   ██║██╔████╔██║██║██║  ██║█████╗",
        "██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗   ██║   ██║██║╚██╔╝██║██║██║  ██║██╔══╝",
        "██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║   ██║   ██║██║ ╚═╝ ██║██║██████╔╝███████╗",
        "╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝     ╚═╝╚═╝╚═════╝ ╚══════╝"
    ]

    width = terminal_width()
    clear()
    print("\n" * 2)

    # ASCII principal
    for i, line in enumerate(art):
        color = BLUE if i < 3 else PURPLE
        print(color + line.center(width) + RESET)
        time.sleep(0.04)

    print("\n")
    print("\n")

    # copyright
    copyright_text = f"{CYAN}© imrankhan1608{RESET}"
    print(copyright_text.center(width))

    print("\n" * 2)
