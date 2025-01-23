"""
Functions for transliteration from Latin to Cyrillic based on phonetic sounds.
"""
import logging
from typing import List
from itertools import product

from transliterate import translit

from .tokenizer import tokenize, detokenize
from .g2p_loader import get_g2p_model
from .preprocessor import _preprocess_cyrillic, _preprocess_phoneme
from .constants import PHONEME2UK


logger = logging.getLogger(__name__)


def latin_to_cyrillic_phonetic(s: str) -> List[str]:
    """
    Transliterates a Latin string into Cyrillic based on phonetic sounds.

    Args:
        s (str): Input string in Latin script.

    Returns:
        List[str]: A list of possible phonetic transliteration variants.

    Examples:
        >>> latin_to_cyrillic_phonetic('coca')
        ['кока']
        >>> latin_to_cyrillic_phonetic('cola')
        ['кола']
        >>> latin_to_cyrillic_phonetic('YARO Veggie cheese')
        ['єро веджі чіз', 'єро ваджі чіз', 'яро веджі чіз', 'яро ваджі чіз']
        >>> latin_to_cyrillic_phonetic('borjomi')
        ['бауроджія', 'боуроджія']
        >>> latin_to_cyrillic_phonetic('columbia')
        ['каламбія']
        >>> latin_to_cyrillic_phonetic('HOKKAIDO CLUB')
        ['хокаідо клаб', 'хокайдо клаб']
        >>> latin_to_cyrillic_phonetic('sonatural')
        ['санечел', 'саначел']
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")

    g2p = get_g2p_model()

    tokens, seps = tokenize(s)

    tokens_translit = []
    for token in tokens:
        phonemes = g2p(token) or [token, ]
        uk_letters = [PHONEME2UK.get(_preprocess_phoneme(phoneme), phoneme) for phoneme in phonemes]
        result = [_preprocess_cyrillic(''.join(x)) for x in product(*uk_letters)]
        result.append(translit(token, 'uk').lower())
        result.append(translit(token, 'ru').lower())
        tokens_translit.append(list(set(result)))

    result = [detokenize(tokens, seps) for tokens in product(*tokens_translit)]
    min_len = min(len(x) for x in result)

    print(s, result)
    return [x for x in result if len(x) <= min_len+2]
