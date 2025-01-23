import re

from .constants import COMBINEUK
from .patterns import PHONEME_STRUCTURE_PATTERN


def _preprocess_cyrillic(s: str) -> str:
    """
    Preprocess Cyrillic text by replacing specific patterns.

    Args:
        s (str): Input string in Cyrillic script.

    Returns:
        str: Preprocessed string with applied replacements.
    """
    for pattern, replacement in COMBINEUK.items():
        s = re.sub(pattern, replacement, s)

    return s


def _preprocess_phoneme(phoneme: str) -> str:
    """
    Preprocess a phoneme by removing stress markers.

    Stress markers (0, 1, or 2) are ignored during transliteration. The function
    extracts the base phoneme using a regular expression.

    Args:
        phoneme (str): The input phoneme in ARPAbet format.

    Returns:
        str: The phoneme without the stress marker.
    """
    match = PHONEME_STRUCTURE_PATTERN.match(phoneme)
    if match:
        return match.group(1)

    return phoneme
