"""
Functions for logging and other small actions within the console:
- `Console.get_args()`
- `Console.user()`
- `Console.is_admin()`
- `Console.pause_exit()`
- `Console.cls()`
- `Console.log()`
- `Console.debug()`
- `Console.info()`
- `Console.done()`
- `Console.warn()`
- `Console.fail()`
- `Console.exit()`
- `Console.confirm()`
- `Console.restricted_input()`
- `Console.pwd_input()`\n
------------------------------------------------------------------------------------------------------
You can also use special formatting codes directly inside the log message to change their appearance.
For more detailed information about formatting codes, see the the `xx_format_codes` description.
"""

from ._consts_ import DEFAULT, CHARS
from .xx_format_codes import FormatCodes
from .xx_string import String
from .xx_color import *

from contextlib import suppress
import pyperclip as _pyperclip
import keyboard as _keyboard
import getpass as _getpass
import shutil as _shutil
import mouse as _mouse
import sys as _sys
import os as _os


class Console:

    @staticmethod
    def get_args(find_args: dict) -> dict[str, dict[str, any]]:
        args = _sys.argv[1:]
        results = {}
        for arg_key, arg_group in find_args.items():
            value = None
            exists = False
            for arg in arg_group:
                if arg in args:
                    exists = True
                    arg_index = args.index(arg)
                    if arg_index + 1 < len(args) and not args[arg_index + 1].startswith("-"):
                        value = String.to_type(args[arg_index + 1])
                    break
            results[arg_key] = {"exists": exists, "value": value}
        return results

    def w() -> int:
        return getattr(_shutil.get_terminal_size(), "columns", 80)

    def h() -> int:
        return getattr(_shutil.get_terminal_size(), "lines", 24)

    def wh() -> tuple[int, int]:
        return Console.w(), Console.h()

    def user() -> str:
        return _os.getenv("USER") or _os.getenv("USERNAME") or _getpass.getuser()

    @staticmethod
    def pause_exit(
        pause: bool = False,
        exit: bool = False,
        prompt: object = "",
        exit_code: int = 0,
        reset_ansi: bool = False,
    ) -> None:
        """Will print the `last_prompt` and then pause the program if `pause` is set
        to `True` and after the pause, exit the program if `exit` is set to `True`."""
        print(prompt, end="", flush=True)
        if reset_ansi:
            FormatCodes.print("[_]", end="")
        if pause:
            _keyboard.read_event()
        if exit:
            _sys.exit(exit_code)

    def cls() -> None:
        """Will clear the console in addition to completely resetting the ANSI formats."""
        if _shutil.which("cls"):
            _os.system("cls")
        elif _shutil.which("clear"):
            _os.system("clear")
        print("\033[0m", end="", flush=True)

    @staticmethod
    def log(
        title: str,
        prompt: object = "",
        start: str = "",
        end: str = "\n",
        title_bg_color: hexa | rgba = None,
        default_color: hexa | rgba = None,
    ) -> None:
        """Will print a formatted log message:
        - `title` -⠀the title of the log message (e.g. `DEBUG`, `WARN`, `FAIL`, etc.)
        - `prompt` -⠀the log message
        - `start` -⠀something to print before the log is printed
        - `end` -⠀something to print after the log is printed (e.g. `\\n\\n`)
        - `title_bg_color` -⠀the background color of the `title`
        - `default_color` -⠀the default text color of the `prompt`\n
        --------------------------------------------------------------------------------
        The log message supports special formatting codes. For more detailed
        information about formatting codes, see `xx_format_codes` class description."""
        title_color = "_color" if not title_bg_color else Color.text_color_for_on_bg(title_bg_color)
        if title:
            FormatCodes.print(
                f'{start}  [bold][{title_color}]{f"[BG:{title_bg_color}]" if title_bg_color else ""} {title.upper()}: [_]\t{f"[{default_color}]" if default_color else ""}{str(prompt)}[_]',
                default_color=default_color,
                end=end,
            )
        else:
            FormatCodes.print(
                f'{start}  {f"[{default_color}]" if default_color else ""}{str(prompt)}[_]',
                default_color=default_color,
                end=end,
            )

    @staticmethod
    def debug(
        prompt: object = "Point in program reached.",
        active: bool = True,
        start: str = "\n",
        end: str = "\n\n",
        title_bg_color: hexa | rgba = DEFAULT.color["yellow"],
        default_color: hexa | rgba = DEFAULT.text_color,
        pause: bool = False,
        exit: bool = False,
    ) -> None:
        """A preset for `log()`: `DEBUG` log message with the options to pause
        at the message and exit the program after the message was printed."""
        if active:
            Console.log("DEBUG", prompt, start, end, title_bg_color, default_color)
            Console.pause_exit(pause, exit)

    @staticmethod
    def info(
        prompt: object = "Program running.",
        start: str = "\n",
        end: str = "\n\n",
        title_bg_color: hexa | rgba = DEFAULT.color["blue"],
        default_color: hexa | rgba = DEFAULT.text_color,
        pause: bool = False,
        exit: bool = False,
    ) -> None:
        """A preset for `log()`: `INFO` log message with the options to pause
        at the message and exit the program after the message was printed."""
        Console.log("INFO", prompt, start, end, title_bg_color, default_color)
        Console.pause_exit(pause, exit)

    @staticmethod
    def done(
        prompt: object = "Program finished.",
        start: str = "\n",
        end: str = "\n\n",
        title_bg_color: hexa | rgba = DEFAULT.color["teal"],
        default_color: hexa | rgba = DEFAULT.text_color,
        pause: bool = False,
        exit: bool = False,
    ) -> None:
        """A preset for `log()`: `DONE` log message with the options to pause
        at the message and exit the program after the message was printed."""
        Console.log("DONE", prompt, start, end, title_bg_color, default_color)
        Console.pause_exit(pause, exit)

    @staticmethod
    def warn(
        prompt: object = "Important message.",
        start: str = "\n",
        end: str = "\n\n",
        title_bg_color: hexa | rgba = DEFAULT.color["orange"],
        default_color: hexa | rgba = DEFAULT.text_color,
        pause: bool = False,
        exit: bool = False,
    ) -> None:
        """A preset for `log()`: `WARN` log message with the options to pause
        at the message and exit the program after the message was printed."""
        Console.log("WARN", prompt, start, end, title_bg_color, default_color)
        Console.pause_exit(pause, exit)

    @staticmethod
    def fail(
        prompt: object = "Program error.",
        start: str = "\n",
        end: str = "\n\n",
        title_bg_color: hexa | rgba = DEFAULT.color["red"],
        default_color: hexa | rgba = DEFAULT.text_color,
        pause: bool = False,
        exit: bool = True,
        reset_ansi=True,
    ) -> None:
        """A preset for `log()`: `FAIL` log message with the options to pause
        at the message and exit the program after the message was printed."""
        Console.log("FAIL", prompt, start, end, title_bg_color, default_color)
        Console.pause_exit(pause, exit, reset_ansi=reset_ansi)

    @staticmethod
    def exit(
        prompt: object = "Program ended.",
        start: str = "\n",
        end: str = "\n\n",
        title_bg_color: hexa | rgba = DEFAULT.color["magenta"],
        default_color: hexa | rgba = DEFAULT.text_color,
        pause: bool = False,
        exit: bool = True,
        reset_ansi=True,
    ) -> None:
        """A preset for `log()`: `EXIT` log message with the options to pause
        at the message and exit the program after the message was printed."""
        Console.log("EXIT", prompt, start, end, title_bg_color, default_color)
        Console.pause_exit(pause, exit, reset_ansi=reset_ansi)

    @staticmethod
    def confirm(
        prompt: object = "Do you want to continue?",
        start="\n",
        end="\n",
        default_color: hexa | rgba = DEFAULT.color["cyan"],
        default_is_yes: bool = True,
    ) -> bool:
        """Ask a yes/no question.\n
        -------------------------------------------------------------------------------
        The question can be formatted with special formatting codes. For more detailed
        information about formatting codes, see the `xx_format_codes` description."""
        confirmed = input(
            FormatCodes.to_ansi(
                f'{start}  {str(prompt)} [_|dim](({"Y" if default_is_yes else "y"}/{"n" if default_is_yes else "N"}):  )',
                default_color,
            )
        ).strip().lower() in (("", "y", "yes") if default_is_yes else ("y", "yes"))
        if end:
            Console.log("", end, end="")
        return confirmed

    @staticmethod
    def restricted_input(
        prompt: object = "",
        allowed_chars: str = CHARS.all,
        min_len: int = None,
        max_len: int = None,
        mask_char: str = None,
        reset_ansi: bool = True,
    ) -> str | None:
        """Acts like a standard Python `input()` with the advantage, that you can specify:
        - what text characters the user is allowed to type and
        - the minimum and/or maximum length of the users input
        - optional mask character (hide user input, e.g. for passwords)
        - reset the ANSI formatting codes after the user continues\n
        -----------------------------------------------------------------------------------
        The input can be formatted with special formatting codes. For more detailed
        information about formatting codes, see the `xx_format_codes` description."""
        FormatCodes.print(prompt, end="", flush=True)
        result = ""
        select_all = False
        last_line_count = 1
        last_console_width = 0

        def update_display(console_width: int) -> None:
            nonlocal select_all, last_line_count, last_console_width
            lines = String.split_count(
                str(prompt) + (mask_char * len(result) if mask_char else result),
                console_width,
            )
            line_count = len(lines)
            if (line_count > 1 or line_count < last_line_count) and not last_line_count == 1:
                if last_console_width > console_width:
                    line_count *= 2
                for _ in range(
                    line_count
                    if line_count < last_line_count and not line_count > last_line_count
                    else (line_count - 2 if line_count > last_line_count else line_count - 1)
                ):
                    _sys.stdout.write("\033[2K\r\033[A")
            prompt_len = len(str(prompt)) if prompt else 0
            prompt_str, input_str = lines[0][:prompt_len], (
                lines[0][prompt_len:] if len(lines) == 1 else "\n".join([lines[0][prompt_len:]] + lines[1:])
            )  # SEPARATE THE PROMPT AND THE INPUT
            _sys.stdout.write(
                "\033[2K\r" + FormatCodes.to_ansi(prompt_str) + ("\033[7m" if select_all else "") + input_str + "\033[27m"
            )
            last_line_count, last_console_width = line_count, console_width

        def handle_enter():
            if min_len is not None and len(result) < min_len:
                return False
            FormatCodes.print("[_]" if reset_ansi else "", flush=True)
            return True

        def handle_backspace_delete():
            nonlocal result, select_all
            if select_all:
                result, select_all = "", False
            elif result and event.name == "backspace":
                result = result[:-1]
            update_display(Console.w())

        def handle_paste():
            nonlocal result, select_all
            if select_all:
                result, select_all = "", False
            filtered_text = "".join(char for char in _pyperclip.paste() if allowed_chars == CHARS.all or char in allowed_chars)
            if max_len is None or len(result) + len(filtered_text) <= max_len:
                result += filtered_text
                update_display(Console.w())

        def handle_select_all():
            nonlocal select_all
            select_all = True
            update_display(Console.w())

        def handle_copy():
            nonlocal select_all
            with suppress(KeyboardInterrupt):
                select_all = False
                update_display(Console.w())
                _pyperclip.copy(result)

        def handle_character_input():
            nonlocal result
            if (allowed_chars == CHARS.all or event.name in allowed_chars) and (max_len is None or len(result) < max_len):
                result += event.name
                update_display(Console.w())

        while True:
            event = _keyboard.read_event()
            if event.event_type == "down":
                if event.name == "enter" and handle_enter():
                    return result.rstrip("\n")
                elif event.name in ("backspace", "delete", "entf"):
                    handle_backspace_delete()
                elif (event.name == "v" and _keyboard.is_pressed("ctrl")) or _mouse.is_pressed("right"):
                    handle_paste()
                elif event.name == "a" and _keyboard.is_pressed("ctrl"):
                    handle_select_all()
                elif event.name == "c" and _keyboard.is_pressed("ctrl") and select_all:
                    handle_copy()
                elif event.name == "esc":
                    return None
                elif event.name == "space":
                    handle_character_input()
                elif len(event.name) == 1:
                    handle_character_input()
                else:
                    select_all = False
                    update_display(Console.w())

    @staticmethod
    def pwd_input(
        prompt: object = "Password: ",
        allowed_chars: str = CHARS.standard_ascii,
        min_len: int = None,
        max_len: int = None,
        _reset_ansi: bool = True,
    ) -> str:
        """Password input (preset for `Console.restricted_input()`)
        that always masks the entered characters with asterisks."""
        return Console.restricted_input(prompt, allowed_chars, min_len, max_len, "*", _reset_ansi)
