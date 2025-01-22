"""This module contains the code for the title function."""

import sys
from .styles import style

def title(text: str,
          borderchar: str = "=",
          borderlen: int = 10,
          lfbefore=True,
          stylebefore: str="",
          styleafter: str="",
          spacesbetween: int=1) -> None:
    """Create a centered text with decorative borders.

    Args:
        text (str): The text to display.
        borderchar (str): The character used for the border.
        borderlen (int): The length of the border.
        lfBefore (bool): Whether to add a line feed (\n) before the title.
        styleBefore (str): The style to apply to the title before the border. Will reset automatically after the first border segment.
        styleAfter (str): The style to apply to the title after the border. Will reset automatically after the last border segment.
        spacesbetween (int): The amout of spaces to add between the title and the border. 0 for none.

    Returns:
        None
    """
    border = f"{borderchar * borderlen}"
    sys.stdout.write(f"{"\n" if lfbefore else ""}{stylebefore}{border}{style.RESET if stylebefore else ""}{" "*spacesbetween}{text}{" "*spacesbetween}{styleafter}{border}{style.RESET if styleafter else ""}\n")
