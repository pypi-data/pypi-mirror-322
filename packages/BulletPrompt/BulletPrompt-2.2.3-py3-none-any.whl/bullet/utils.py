import sys
import tty
import termios
import shutil
from .charDef import *  # noqa: F403
from . import colors

COLUMNS, _ = shutil.get_terminal_size()  ## Size of console


def is_printable(s: str) -> bool:
    """Determine if a string contains only printable characters.
    Args:
        s: The string to verify.
    Returns:
        bool: `True` if all characters in `s` are printable. `False` if any
            characters in `s` can not be printed.
    """
    # Ref: https://stackoverflow.com/a/50731077
    return not any(repr(ch).startswith(("'\\x", "'\\u")) for ch in s)


def mygetc():
    """Get raw characters from input."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def getchar():
    """Character input parser."""
    c = mygetc()
    if ord(c) in {LINE_BEGIN_KEY, LINE_END_KEY, TAB_KEY, INTERRUPT_KEY, NEWLINE_KEY, BACK_SPACE_KEY}:  # noqa: F405
        return c

    if ord(c) == ESC_KEY:  # noqa: F405
        combo = mygetc()
        if ord(combo) == MOD_KEY_INT:  # noqa: F405
            key = mygetc()
            if MOD_KEY_BEGIN - MOD_KEY_FLAG <= ord(key) <= MOD_KEY_END - MOD_KEY_FLAG:  # noqa: F405
                if ord(mygetc()) == MOD_KEY_DUMMY:  # noqa: F405
                    return chr(ord(key) + MOD_KEY_FLAG)  # noqa: F405
                return UNDEFINED_KEY  # noqa: F405
            if ARROW_KEY_BEGIN - ARROW_KEY_FLAG <= ord(key) <= ARROW_KEY_END - ARROW_KEY_FLAG:  # noqa: F405
                return chr(ord(key) + ARROW_KEY_FLAG)  # noqa: F405
            return UNDEFINED_KEY  # noqa: F405
        return getchar()

    return c if is_printable(c) else UNDEFINED_KEY  # noqa: F405


# Basic command line functions


def moveCursorLeft(n):
    """Move cursor left n columns."""
    forceWrite("\033[{}D".format(n))


def moveCursorRight(n):
    """Move cursor right n columns."""
    forceWrite("\033[{}C".format(n))


def moveCursorUp(n):
    """Move cursor up n rows."""
    forceWrite("\033[{}A".format(n))


def moveCursorDown(n):
    """Move cursor down n rows."""
    forceWrite("\033[{}B".format(n))


def moveCursorHead():
    """Move cursor to the start of line."""
    forceWrite("\r")


def clearLine():
    """Clear content of one line on the console."""
    forceWrite(" " * COLUMNS)
    moveCursorHead()


def clearConsoleUp(n):
    """Clear n console rows (bottom up)."""
    for _ in range(n):
        clearLine()
        moveCursorUp(1)


def clearConsoleDown(n):
    """Clear n console rows (top down)."""
    for _ in range(n):
        clearLine()
        moveCursorDown(1)
    moveCursorUp(n)


def forceWrite(s, end=""):
    """Dump everthing in the buffer to the console."""
    sys.stdout.write(s + end)
    sys.stdout.flush()


def cprint(
    s: str,
    color: str = colors.foreground["default"],
    on: str = colors.background["default"],
    end: str = "\n",
):
    """Colored print function.
    Args:
        s: The string to be printed.
        color: The color of the string.
        on: The color of the background.
        end: Last character appended.
    Returns:
        None
    """
    forceWrite(on + color + s + colors.RESET, end=end)
