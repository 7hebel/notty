from typing import Callable, Self, Any, Literal
from colorama import init, Back, Fore

from core.path import Path

init(autoreset=True)


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

    def __enter__(self) -> Self:
        if ProcessCallback.processes == 0:
            print("\n")

        ProcessCallback.processes += 1
        print(f"{ProcessCallback._indent()}╭─> {Fore.BLUE}( {Fore.RESET}{self.name.strip()} {Fore.BLUE})")
        print(f"{ProcessCallback._indent()}{Fore.LIGHTBLACK_EX}:")
        return self

    def __exit__(self, ex_type: type, ex_value: Exception, ex_tb: Any) -> Literal[True]:
        print(f"{ProcessCallback._indent()}{Fore.LIGHTBLACK_EX}:")
        print(f"{ProcessCallback._indent()}├─> {Fore.RED}{self._error} {Fore.YELLOW}{self._warn} {Fore.GREEN}{self._success} {Fore.RESET}{self._info}")

        if ex_type is not None:
            print(f"{ProcessCallback._indent()}╰─> {Fore.RED}FAIL: {Fore.RESET}({str(ex_type)[8:-2]}) {Fore.RED}{ex_value}")
    
        else:
            print(f"{ProcessCallback._indent()}╰─> {Fore.BLUE}{self.success_message}")
        
        print(ProcessCallback._exit_indent())
        ProcessCallback.processes -= 1
        return True

    def error(self, value: str) -> None:
        print(f"{ProcessCallback._indent()}{Fore.RED}• {value}")
        self._error += 1

    def warn(self, value: str) -> None:
        print(f"{ProcessCallback._indent()}{Fore.YELLOW}• {value}")
        self._warn += 1

    def info(self, value: str) -> None:
        print(f"{ProcessCallback._indent()}• {value}")
        self._info += 1

    def success(self, value: str) -> None:
        print(f"{ProcessCallback._indent()}{Fore.GREEN}• {value}")
        self._success += 1


# -- OUTPUT --

display_error: Callable[[str], None] = lambda message: print(f"[{Fore.WHITE}{Back.RED} ERROR {Fore.RESET}{Back.RESET}] {Fore.RED}{message}")
display_warning: Callable[[str], None] = lambda message: print(f"[{Fore.BLACK}{Back.YELLOW} WARNING {Fore.RESET}{Back.RESET}] {Fore.YELLOW}{message}")
display_info: Callable[[str], None] = lambda message: print(f"[{Fore.BLACK}{Back.BLUE} INFO {Fore.RESET}{Back.RESET}] {message}")
display_success: Callable[[str], None] = lambda message: print(f"[{Fore.BLACK}{Back.GREEN} SUCCESS {Fore.RESET}{Back.RESET}] {message}")

def display_key_value(title: str, dictionary: dict[str, str]) -> None:
    print(f"\n{Fore.CYAN}{{ {Fore.RESET}{title} {Fore.CYAN}}} ")
    for key, value in dictionary.items():
        print(f"  • {Fore.CYAN}{key}{Fore.BLUE}:{Fore.RESET} {value}")

def display_bullet_list(title: str, points: list[str]) -> None:
    print(f"\n{Fore.CYAN}< {Fore.RESET}{title} {Fore.CYAN}> ")
    for point in points:
        print(f"  {Fore.YELLOW}•{Fore.RESET} {point.strip()}")

    if len(points) == 0:
        print(f"  {Fore.RED}• (blank)")

def display_file_content(path: Path) -> None:
    with open(str(path)) as file:
        lines = file.readlines()
    
    lineno_space = 2 + len(str(len(lines)))

    for index, line_content in enumerate(lines):
        lineno = str(index+1).rjust(lineno_space)
        line = f"{Fore.CYAN}{lineno}{Fore.LIGHTBLACK_EX} | {Fore.RESET}{line_content.rstrip()}"
        print(line)



# -- INPUT --

def get_input_with_validation(prompt: str, validator: Callable[[str], bool]) -> str:
    prompt = f"\n {Fore.MAGENTA}?{Fore.RESET} {prompt} {Fore.MAGENTA}~{Fore.RESET} "

    while True:
        user = input(prompt)

        if not validator(user):
            print(f" {Fore.RED}╰ ! {Fore.RESET}Invalid response.")
            continue

        return user

def get_boolean_response(prompt: str) -> bool:
    true = ["yes", "y", "1", "t", "true"]
    false = ["no", "n", "0", "f", "false"]
    prompt = f"\n {Fore.GREEN}T{Fore.RED}f {Fore.RESET}{prompt} {Fore.MAGENTA}?{Fore.RESET} "

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
        