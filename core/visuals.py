from colorama import init, Back, Fore
from typing import Callable
import os

init(autoreset=True)


class Message:
    """ Formatted messages. """

    def unexpected_error(message: str):
        print(f"[{Fore.RED}{Back.WHITE} UNEXPECTED ERROR {Fore.RESET}{Back.RESET}] {Fore.RED}{message}")
        
    def error(message: str):
        print(f"[{Fore.WHITE}{Back.RED} ERROR {Fore.RESET}{Back.RESET}] {Fore.RED}{message}")

    def warning(message: str):
        print(f"[{Fore.BLACK}{Back.YELLOW} WARNING {Fore.RESET}{Back.RESET}] {Fore.YELLOW}{message}")

    def info(message: str):
        print(f"[{Fore.BLACK}{Back.BLUE} INFO {Fore.RESET}{Back.RESET}] {message}")
        
    def success(message: str):
        print(f"[{Fore.BLACK}{Back.GREEN} SUCCESS {Fore.RESET}{Back.RESET}] {message}")

    def custom(title: str, message: str):
        print(f"[{Fore.BLACK}{Back.WHITE} {title} {Fore.RESET}{Back.RESET}] {message}")

    def key_value(key: str, value: str):
        print(f"{Fore.CYAN}{key}{Fore.BLUE}:{Fore.RESET} {value}")

    def bullet_list(title: str, points: list):
        print(f"\n< {title.upper()} > ")
        for point in points:
            print(f"  {Fore.YELLOW}~>{Fore.RESET} {point.strip()}")

        if len(points) == 0:
            print(f"  {Fore.RED}~> (blank)")


class ProcessCallback:
    def __init__(self, process_name: str) -> None:
        self.name = process_name
        self._error = 0
        self._warn = 0
        self._info = 0
        self._success = 0

    def __enter__(self):
        print(f"\n╭─> {Fore.BLUE}( {Fore.RESET}{self.name.strip()} {Fore.BLUE})")
        print(f"{Fore.LIGHTBLACK_EX}:")
        return self

    def __exit__(self, ex_type, ex_value, ex_tb):
        print(f"{Fore.LIGHTBLACK_EX}:")
        print(f"├─> {Fore.RED}{self._error}{Fore.RESET}/{Fore.YELLOW}{self._warn}{Fore.RESET}/{Fore.GREEN}{self._success}{Fore.RESET}/{self._info}")

        if ex_type is not None:
            print(f"╰─> {Fore.RED}Error: {ex_value}")

        else:
            print(f"╰─> {Fore.BLUE}End of process.")

        return True

    def error(self, value):
        print(f"{Fore.RED}• {value}")
        self._error += 1

    def warn(self, value):
        print(f"{Fore.YELLOW}• {value}")
        self._warn += 1

    def info(self, value):
        print(f"• {value}")
        self._info += 1

    def success(self, value):
        print(f"{Fore.GREEN}• {value}")
        self._success += 1


def clear_screen():
    os.system("cls || clear")

def get_input_with_validation(prompt: str, validator: Callable) -> str:
    prompt = f"\n {Fore.MAGENTA}?{Fore.RESET} {prompt} {Fore.MAGENTA}~{Fore.RESET} "

    while True:
        user = input(prompt)

        if validator(user):
            return user
        else:
            print(f" {Fore.RED}╰ ! {Fore.RESET}Invalid response.")

def get_boolean_response(prompt: str) -> bool:
    true = ["yes", "y", "1", "t", "true"]
    false = ["no", "n", "0", "f", "false"]
    prompt = f"\n {Fore.GREEN}T{Fore.LIGHTBLACK_EX}/{Fore.RED}f {Fore.RESET}{prompt} {Fore.MAGENTA}~{Fore.RESET} "

    while True:
        user = input(prompt).lower()

        if user in true:
            return True
        if user in false:
            return False
        
        print(f" {Fore.RED}╰ ! {Fore.RESET}Invalid response.")

