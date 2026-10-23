"""
ANSI color support with automatic detection and a runtime toggle
"""
import os
import sys

RESET = '\033[0m'

CODES = {
    'black': '30', 'red': '31', 'green': '32', 'yellow': '33',
    'blue': '34', 'magenta': '35', 'cyan': '36', 'white': '37',
    'gray': '90', 'bright_red': '91', 'bright_green': '92',
    'bright_yellow': '93', 'bright_blue': '94', 'bright_magenta': '95',
    'bright_cyan': '96', 'bright_white': '97',
    'bold': '1', 'dim': '2',
}


def _enable_windows_ansi():
    """Turn on ANSI processing in the Windows console; False if unavailable"""
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel32.SetConsoleMode(handle, mode.value | 0x0004))
    except Exception:
        return False


def detect_color_support():
    """Best-effort check that the terminal understands ANSI colors"""
    if os.environ.get('NO_COLOR') is not None:
        return False
    if not sys.stdout.isatty():
        return False
    if os.environ.get('TERM', '') == 'dumb':
        return False
    if sys.platform == 'win32':
        return _enable_windows_ansi()
    return True


_enabled = detect_color_support()


def is_enabled():
    return _enabled


def set_enabled(value):
    global _enabled
    _enabled = bool(value)


def toggle():
    """Flip colors on/off; returns the new state"""
    set_enabled(not _enabled)
    return _enabled


def colorize(text, *styles):
    """Wrap text in ANSI codes (e.g. colorize('x', 'red', 'bold')); plain text if disabled"""
    if not _enabled or not styles or not text:
        return text
    codes = ';'.join(CODES[s] for s in styles)
    return f"\033[{codes}m{text}{RESET}"
