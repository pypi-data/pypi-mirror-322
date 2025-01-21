"""
Functions to be able to use special (easy) formatting codes directly inside some message (string).\n
These codes, when used within following functions, will change the look of log within the console:
- `FormatCodes.print()` (print a special format-codes containing string)
- `FormatCodes.input()` (input with a special format-codes containing prompt)
- `FormatCodes.to_ansi()` (transform all special format-codes into ANSI codes in a string)\n
--------------------------------------------------------------------------------------------------------------------
How to change the text format and color?\n
Example string with formatting codes:
```string
[bold]This is bold text, [#F08]which is pink now [black|BG:#FF0088] and now it changed`
to black with a pink background. [_]And this is the boring text, where everything is reset.
```
⇾ Instead of writing the formats all separate `[x][y][z]` you can join them like this `[x|y|z]`\n
--------------------------------------------------------------------------------------------------------------------
You can also automatically reset a certain format, behind text like shown in the following example:
```string
This is normal text [b](which is bold now) but now it was automatically reset to normal.
```
This will only reset formats, that have a reset listed below. Colors and BG-colors won't be reset.\n
This is what will happen, if you use it with a color-format:
```string
[cyan]This is cyan text [b](which is bold now.) Now it's not bold any more but still cyan.
```
If you want to ignore the `()` brackets you can put a `\\` or `/` between:
```string
[cyan]This is cyan text [b]/(which is bold now.) And now it is still bold and cyan.
```
⇾ To see these examples in action, you can put them into the `FormatCodes.print()` function.\n
--------------------------------------------------------------------------------------------------------------------
All possible formatting codes:
- HEX colors:  `[#F08]` or `[#FF0088]` (with or without leading #)
- RGB colors:  `[rgb(255, 0, 136)]`
- background colors:  `[BG:#F08]`
- standard cmd colors:
  - `[black]`
  - `[red]`
  - `[green]`
  - `[yellow]`
  - `[blue]`
  - `[magenta]`
  - `[cyan]`
  - `[white]`
- bright cmd colors: `[bright:black]` or `[br:black]`, `[bright:red]` or `[br:red]`, ...
- background cmd colors: `[BG:black]`, `[BG:red]`, ...
- bright background cmd colors: `[BG:bright:black]` or `[BG:br:black]`, `[BG:bright:red]` or `[BG:br:red]`, ...\n
  ⇾ The order of `BG:` and `bright:` or `br:` does not matter.
- text formats:
  - `[bold]` or `[b]`
  - `[dim]`
  - `[italic]` or `[i]`
  - `[underline]` or `[u]`
  - `[inverse]`, `[invert]` or `[in]`
  - `[hidden]`, `[hide]` or `[h]`
  - `[strikethrough]` or `[s]`
  - `[double-underline]` or `[du]`
- specific reset:
  - `[_bold]` or `[_b]`
  - `[_dim]`
  - `[_italic]` or `[_i]`
  - `[_underline]` or `[_u]`
  - `[_inverse]`, `[_invert]` or `[_in]`
  - `[_hidden]`, `[_hide]` or `[_h]`
  - `[_strikethrough]` or `[_s]`
  - `[_double-underline]` or `[_du]`
  - `[_color]` or `[_c]`
  - `[_background]` or `[_bg]`
- total reset:
  - `[_]`
--------------------------------------------------------------------------------------------------------------------
Additional formats when a `default_color` is set:
- `[*]` will reset everything, just like `[_]`, but the text-color will remain in `default_color`
- `[*color]` will reset the text-color, just like `[_color]`, but then also make it `default_color`
- `[default]` will just color the text in `default_color`,
- `[BG:default]` will color the background in `default_color`\n
Unlike the standard cmd colors, the default color can be changed by using the following modifiers:
- `[l]` will lighten the `default_color` text by `brightness_steps`%
- `[ll]` will lighten the `default_color` text by `2 × brightness_steps`%
- `[lll]` will lighten the `default_color` text by `3 × brightness_steps`%
- ... etc. Same thing for darkening:
- `[d]` will darken the `default_color` text by `brightness_steps`%
- `[dd]` will darken the `default_color` text by `2 × brightness_steps`%
- `[ddd]` will darken the `default_color` text by `3 × brightness_steps`%
- ... etc.\n
Per default, you can also use `+` and `-` to get lighter and darker `default_color` versions.
"""

from ._consts_ import ANSI
from .xx_string import String
from .xx_regex import Regex
from .xx_color import *

from functools import lru_cache
import ctypes as _ctypes
import regex as _rx
import sys as _sys
import re as _re

PREFIX = {
    "BG": {"background", "bg"},
    "BR": {"bright", "br"},
}
PREFIXES = {val for values in PREFIX.values() for val in values}
PREFIX_RX = {
    "BG": rf"(?:{'|'.join(PREFIX['BG'])})\s*:",
    "BR": rf"(?:{'|'.join(PREFIX['BR'])})\s*:",
}
COMPILED = {  # PRECOMPILE REGULAR EXPRESSIONS
    "*": _re.compile(r"\[\s*([^]_]*?)\s*\*\s*([^]_]*?)\]"),
    "*color": _re.compile(r"\[\s*([^]_]*?)\s*\*color\s*([^]_]*?)\]"),
    "format": _rx.compile(
        Regex.brackets("[", "]", is_group=True) + r"(?:\s*([/\\]?)\s*" + Regex.brackets("(", ")", is_group=True) + r")?"
    ),
    "bg?_default": _re.compile(r"(?i)((?:" + PREFIX_RX["BG"] + r")?)\s*default"),
    "bg_default": _re.compile(r"(?i)" + PREFIX_RX["BG"] + r"\s*default"),
    "modifier": _re.compile(
        r"(?i)((?:BG\s*:)?)\s*("
        + "|".join([f"{_re.escape(m)}+" for m in ANSI.modifier["lighten"] + ANSI.modifier["darken"]])
        + r")$"
    ),
    "rgb": _re.compile(
        r"(?i)^\s*(" + PREFIX_RX["BG"] + r")?\s*(?:rgb|rgba)?\s*\(?\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)?\s*$"
    ),
    "hex": _re.compile(r"(?i)^\s*(" + PREFIX_RX["BG"] + r")?\s*(?:#|0x)?([0-9A-F]{6}|[0-9A-F]{3})\s*$"),
}


class FormatCodes:

    @staticmethod
    def print(
        *values: object,
        default_color: hexa | rgba = None,
        brightness_steps: int = 20,
        sep: str = " ",
        end: str = "\n",
        flush: bool = True,
    ) -> None:
        """Print a string that can be formatted using special formatting codes.\n
        --------------------------------------------------------------------------
        For exact information about how to use special formatting codes, see the
        `xx_format_codes` module documentation."""
        FormatCodes.__config_console()
        _sys.stdout.write(FormatCodes.to_ansi(sep.join(map(str, values)) + end, default_color, brightness_steps))
        if flush:
            _sys.stdout.flush()

    @staticmethod
    def input(
        prompt: object = "",
        default_color: hexa | rgba = None,
        brightness_steps: int = 20,
        reset_ansi: bool = False,
    ) -> str:
        """An input, which's prompt can be formatted using special formatting codes.\n
        -------------------------------------------------------------------------------
        If `reset_ansi` is true, all ANSI formatting will be reset, after the user has
        confirmed the input and the program continues.\n
        -------------------------------------------------------------------------------
        For exact information about how to use special formatting codes, see the
        `xx_format_codes` module documentation."""
        FormatCodes.__config_console()
        user_input = input(FormatCodes.to_ansi(prompt, default_color, brightness_steps))
        if reset_ansi:
            _sys.stdout.write("\x1b[0m")
        return user_input

    @staticmethod
    def to_ansi(
        string: str, default_color: hexa | rgba = None, brightness_steps: int = 20, _default_start: bool = True
    ) -> str:
        """Convert the special formatting codes inside a string to printable ANSI codes.\n
        -----------------------------------------------------------------------------------
        For exact information about how to use special formatting codes, see the
        `xx_format_codes` module documentation."""
        if Color.is_valid_rgba(default_color, False):
            use_default = True
        elif Color.is_valid_hexa(default_color, False):
            use_default, default_color = True, Color.to_rgba(default_color)
        else:
            use_default = False
        if use_default:
            string = COMPILED["*"].sub(r"[\1_|default\2]", string)  # REPLACE `[…|*|…]` WITH `[…|_|default|…]`
            string = COMPILED["*color"].sub(r"[\1default\2]", string)  # REPLACE `[…|*color|…]` WITH `[…|default|…]`

        def is_valid_color(color: str) -> bool:
            return color in ANSI.color_map or Color.is_valid_rgba(color) or Color.is_valid_hexa(color)

        def replace_keys(match: _re.Match) -> str:
            formats = match.group(1)
            escaped = match.group(2)
            auto_reset_txt = match.group(3)
            if auto_reset_txt and auto_reset_txt.count("[") > 0 and auto_reset_txt.count("]") > 0:
                auto_reset_txt = FormatCodes.to_ansi(auto_reset_txt, default_color, brightness_steps, False)
            if not formats:
                return match.group(0)
            if formats.count("[") > 0 and formats.count("]") > 0:
                formats = FormatCodes.to_ansi(formats, default_color, brightness_steps, False)
            format_keys = [k.strip() for k in formats.split("|") if k.strip()]
            ansi_formats = [
                r if (r := FormatCodes.__get_replacement(k, default_color, brightness_steps)) != k else f"[{k}]"
                for k in format_keys
            ]
            if auto_reset_txt and not escaped:
                reset_keys = []
                for k in format_keys:
                    k_lower = k.lower()
                    k_set = set(k_lower.split(":"))
                    if PREFIX["BG"] & k_set and len(k_set) <= 3:
                        if k_set & PREFIX["BR"]:
                            for i in range(len(k)):
                                if is_valid_color(k[i:]):
                                    reset_keys.extend(["_bg", "_color"])
                                    break
                        else:
                            for i in range(len(k)):
                                if is_valid_color(k[i:]):
                                    reset_keys.append("_bg")
                                    break
                    elif is_valid_color(k) or any(
                        k_lower.startswith(pref_colon := f"{prefix}:") and is_valid_color(k[len(pref_colon) :])
                        for prefix in PREFIX["BR"]
                    ):
                        reset_keys.append("_color")
                    else:
                        reset_keys.append(f"_{k}")
                ansi_resets = [
                    r
                    for k in reset_keys
                    if (r := FormatCodes.__get_replacement(k, default_color, brightness_steps)).startswith(
                        f"{ANSI.char}{ANSI.start}"
                    )
                ]
            else:
                ansi_resets = []
            if not (len(ansi_formats) == 1 and ansi_formats[0].count(f"{ANSI.char}{ANSI.start}") >= 1) and not all(
                f.startswith(f"{ANSI.char}{ANSI.start}") for f in ansi_formats
            ):
                return match.group(0)
            return (
                "".join(ansi_formats)
                + (
                    f"({FormatCodes.to_ansi(auto_reset_txt, default_color, brightness_steps, False)})"
                    if escaped and auto_reset_txt
                    else auto_reset_txt if auto_reset_txt else ""
                )
                + ("" if escaped else "".join(ansi_resets))
            )

        string = "\n".join(COMPILED["format"].sub(replace_keys, line) for line in string.split("\n"))
        return (FormatCodes.__get_default_ansi(default_color) if _default_start else "") + string if use_default else string

    @staticmethod
    def escape_ansi(ansi_string: str, escaped_char: str = ANSI.char_esc) -> str:
        """Makes the string printable with the ANSI formats visible."""
        return ansi_string.replace(ANSI.char, escaped_char)

    @staticmethod
    @lru_cache(maxsize=64)
    def __config_console() -> None:
        """Configure the console to be able to interpret ANSI formatting."""
        _sys.stdout.flush()
        kernel32 = _ctypes.windll.kernel32
        h = kernel32.GetStdHandle(-11)
        mode = _ctypes.c_ulong()
        kernel32.GetConsoleMode(h, _ctypes.byref(mode))
        kernel32.SetConsoleMode(h, mode.value | 0x0004)

    @staticmethod
    def __get_default_ansi(
        default_color: tuple,
        format_key: str = None,
        brightness_steps: int = None,
        _modifiers: tuple[str, str] = (ANSI.modifier["lighten"], ANSI.modifier["darken"]),
    ) -> str | None:
        """Get the `default_color` and lighter/darker versions of it in ANSI format."""
        if not brightness_steps or (format_key and COMPILED["bg?_default"].search(format_key)):
            return (ANSI.seq_bg_color if format_key and COMPILED["bg_default"].search(format_key) else ANSI.seq_color).format(
                *default_color[:3]
            )
        if not (format_key in _modifiers[0] or format_key in _modifiers[1]):
            return None
        match = COMPILED["modifier"].match(format_key)
        if not match:
            return None
        is_bg, modifiers = match.groups()
        adjust = 0
        for mod in _modifiers[0] + _modifiers[1]:
            adjust = String.single_char_repeats(modifiers, mod)
            if adjust and adjust > 0:
                modifiers = mod
                break
        if adjust == 0:
            return None
        elif modifiers in _modifiers[0]:
            new_rgb = Color.adjust_lightness(default_color, (brightness_steps / 100) * adjust)
        elif modifiers in _modifiers[1]:
            new_rgb = Color.adjust_lightness(default_color, -(brightness_steps / 100) * adjust)
        return (ANSI.seq_bg_color if is_bg else ANSI.seq_color).format(*new_rgb[:3])

    @staticmethod
    def __get_replacement(format_key: str, default_color: rgba = None, brightness_steps: int = 20) -> str:
        """Gives you the corresponding ANSI code for the given format key.
        If `default_color` is not `None`, the text color will be `default_color` if all formats
        are reset or you can get lighter or darker version of `default_color` (also as BG)"""
        use_default = default_color and Color.is_valid_rgba(default_color, False)
        _format_key, format_key = format_key, FormatCodes.__normalize_key(format_key)  # NORMALIZE KEY AND SAVE ORIGINAL
        if use_default:
            if new_default_color := FormatCodes.__get_default_ansi(default_color, format_key, brightness_steps):
                return new_default_color
        for map_key in ANSI.codes_map:
            if (isinstance(map_key, tuple) and format_key in map_key) or format_key == map_key:
                return ANSI.seq().format(
                    next(
                        (
                            v
                            for k, v in ANSI.codes_map.items()
                            if format_key == k or (isinstance(k, tuple) and format_key in k)
                        ),
                        None,
                    )
                )
        rgb_match = _re.match(COMPILED["rgb"], format_key)
        hex_match = _re.match(COMPILED["hex"], format_key)
        try:
            if rgb_match:
                is_bg = rgb_match.group(1)
                r, g, b = map(int, rgb_match.groups()[1:])
                if Color.is_valid_rgba((r, g, b)):
                    return ANSI.seq_bg_color.format(r, g, b) if is_bg else ANSI.seq_color.format(r, g, b)
            elif hex_match:
                is_bg = hex_match.group(1)
                rgb = Color.to_rgba(hex_match.group(2))
                return (
                    ANSI.seq_bg_color.format(rgb[0], rgb[1], rgb[2])
                    if is_bg
                    else ANSI.seq_color.format(rgb[0], rgb[1], rgb[2])
                )
        except Exception:
            pass
        return _format_key

    @staticmethod
    @lru_cache(maxsize=64)
    def __normalize_key(format_key: str) -> str:
        """Normalizes the given format key."""
        k_parts = format_key.replace(" ", "").lower().split(":")
        prefix_str = "".join(
            f"{prefix_key.lower()}:"
            for prefix_key, prefix_values in PREFIX.items()
            if any(k_part in prefix_values for k_part in k_parts)
        )
        return prefix_str + ":".join(
            part for part in k_parts if part not in {val for values in PREFIX.values() for val in values}
        )
