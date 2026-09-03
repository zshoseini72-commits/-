"""ابزارهای ساده برای خروجی رنگی برنامه."""
from colorama import Fore, Style, init

init(autoreset=True)


def success(message: str) -> None:
    print(Fore.GREEN + message + Style.RESET_ALL)


def error(message: str) -> None:
    print(Fore.RED + message + Style.RESET_ALL)


def warning(message: str) -> None:
    print(Fore.YELLOW + message + Style.RESET_ALL)


def info(message: str) -> None:
    print(Fore.CYAN + message + Style.RESET_ALL)


def title(message: str) -> None:
    print(Fore.BLUE + Style.BRIGHT + message + Style.RESET_ALL)
