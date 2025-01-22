"""This module contains the pinput function for displaying styled input prompts."""

import sys
from .styles import style

def pinput(prompt: str,
           customprefix: str=">>",
           prefixstyle: str="",
           autoquestion: bool=True,
           lfbefore: bool=True) -> str:
    """Display a styled input prompt with a custom prefix.

    Args:
        prompt (str): The input prompt message.
        customprefix (str): A custom prefix for the input prompt
        prefixstyle (str): The style to apply to the prefix with colourup.style
        autoquestion (bool): Whether to automatically change the prefix if a question mark is found at the end of the prompt.
        lfbefore (bool): Whether to add a line feed (\n) before the prompt.

    Returns:
        str: The user's input.
    """

    # To check if the prefix has been overriden, to not override it again.
    if autoquestion and prompt[-1] == "?" and customprefix == ">>":
        customprefix = "?>"

    sys.stdout.write(f"{"\n" if lfbefore else ""}{prompt}{style.RESET}\n{prefixstyle}{customprefix}{style.RESET} ")

    sys.stdout.flush()
    return sys.stdin.readline().strip()
