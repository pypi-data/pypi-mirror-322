"""ColourUp - Terminal Output Styling Package

A Python package for enhancing terminal output with colors, styles, and
formatted text elements. Provides simple functions to create visually
appealing command-line interfaces.

Key Features:
- ANSI color support (foreground/background)
- Text styling (bold, italic, underline)
- Formatted title bars
- Styled input prompts

Main Functions:
    title()  - Create centered text with decorative borders
    pinput() - Display styled input prompts

Example:
    >>> from colourup import title, pinput
    >>> title("Welcome", "=", 6)
    ====== Welcome ======
    >>> name = pinput("What's your name?", customprompt="Name:")
    What's your name?
    Name:

Requires Python 3.11+
Source: https://github.com/yourusername/colourup
"""

from . import styles
from .title import title
from .pinput import pinput

__all__ = [styles, title, pinput]
