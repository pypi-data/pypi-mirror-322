from . import fg
from . import bg
from . import style

# Colorama to make ANSI escape codes work on Windows
import colorama

colorama.init()

__all__ = [
    fg,
    bg,
    style,
]
