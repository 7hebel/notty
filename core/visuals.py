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

    def key_value(title: str, dictionary: dict):
        print(f"\n{Fore.CYAN}{{ {Fore.RESET}{title} {Fore.CYAN}}} ")
        for key, value in dictionary.items():
            print(f"  • {Fore.CYAN}{key}{Fore.BLUE}:{Fore.RESET} {value}")

    def bullet_list(title: str, points: list):
        print(f"\n{Fore.CYAN}< {Fore.RESET}{title} {Fore.CYAN}> ")
        for point in points:
            print(f"  {Fore.YELLOW}•{Fore.RESET} {point.strip()}")

        if len(points) == 0:
            print(f"  {Fore.RED}• (blank)")


class ProcessCallback:
    processes = 0

    @staticmethod
    def _indent() -> str:
        return f"{Fore.LIGHTBLACK_EX}│ {Fore.RESET}" * (ProcessCallback.processes-1)

    @staticmethod
    def _exit_indent() -> str:
        if ProcessCallback.processes > 1:
            return "│ " * (ProcessCallback.processes-2) + f"{Fore.LIGHTBLACK_EX}: "
        else:
            return ""

    def __init__(self, process_name: str, success_message: str = "End of process.") -> None:
        self.name = process_name
        self.success_message = success_message
        self._error = 0
        self._warn = 0
        self._info = 0
        self._success = 0

    def __enter__(self):
        if ProcessCallback.processes == 0:
            print("\n")

        ProcessCallback.processes += 1
        print(f"{ProcessCallback._indent()}╭─> {Fore.BLUE}( {Fore.RESET}{self.name.strip()} {Fore.BLUE})")
        print(f"{ProcessCallback._indent()}{Fore.LIGHTBLACK_EX}:")
        return self

    def __exit__(self, ex_type, ex_value, ex_tb):
        print(f"{ProcessCallback._indent()}{Fore.LIGHTBLACK_EX}:")
        print(f"{ProcessCallback._indent()}├─> {Fore.RED}{self._error} {Fore.YELLOW}{self._warn} {Fore.GREEN}{self._success} {Fore.RESET}{self._info}")

        if ex_type is not None:
            print(f"{ProcessCallback._indent()}╰─> {Fore.RED}FAIL: {Fore.RESET}({str(ex_type)[8:-2]}) {Fore.RED}{ex_value}")
    
        else:
            print(f"{ProcessCallback._indent()}╰─> {Fore.BLUE}{self.success_message}")
        
        print(ProcessCallback._exit_indent())
        ProcessCallback.processes -= 1
        return True

    def error(self, value):
        print(f"{ProcessCallback._indent()}{Fore.RED}• {value}")
        self._error += 1

    def warn(self, value):
        print(f"{ProcessCallback._indent()}{Fore.YELLOW}• {value}")
        self._warn += 1

    def info(self, value):
        print(f"{ProcessCallback._indent()}• {value}")
        self._info += 1

    def success(self, value):
        print(f"{ProcessCallback._indent()}{Fore.GREEN}• {value}")
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
    prompt = f"\n {Fore.GREEN}T{Fore.LIGHTBLACK_EX}/{Fore.RED}f {Fore.RESET}{prompt} {Fore.MAGENTA}?{Fore.RESET} "

    while True:
        user = input(prompt).lower()

        if user in true:
            return True
        if user in false:
            return False
        
        print(f" {Fore.RED}╰ ! {Fore.RESET}Invalid response.")

def get_multiline_input(prompt: str) -> str:
    print(f"\n {Fore.MAGENTA}# {Fore.RESET}{prompt} {Fore.MAGENTA}~> {Fore.RESET}")

    line_prompt = f"   {Fore.MAGENTA}>{Fore.RESET} "
    last_line = None
    data = ""

    while True:
        try:
            new_data = input(line_prompt)
        except KeyboardInterrupt:
            return data

        if new_data.strip() == "" and last_line == "":
            return data
        
        data += new_data+"\n"
        last_line = new_data
        