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

    def bullet_list(title: str, points: list):
        print(f"\n< {title.upper()} > ")
        for point in points:
            print(f"  {Fore.YELLOW}~>{Fore.RESET} {point.strip()}")

        if len(points) == 0:
            print(f"  {Fore.RED}~> (blank)")


def clear():
    os.system("cls || clear")

def get_input(prompt: str, validator: Callable) -> str:
    prompt = f"\n {Fore.MAGENTA}?{Fore.RESET} {prompt} {Fore.MAGENTA}~{Fore.RESET} "

    while True:
        user = input(prompt)

        if validator(user):
            return user
        else:
            print(f" {Fore.RED}╰ ! {Fore.RESET}Invalid response.")

