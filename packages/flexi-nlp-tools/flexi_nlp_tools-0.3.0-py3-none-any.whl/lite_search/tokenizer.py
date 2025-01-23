from typing import Tuple, Sequence

from .phonetic_translit.tokenizer.patterns import TOKEN_PATTERN


def tokenize(name: str) -> Tuple[Sequence[str], Sequence[str]]:
    """
    Retokenize tokens to string.

    ::Parameters::

    :param str name: input string

    :return Tuple[Sequence[str], Sequence[str]]: list of tokens and list of separators

    ::Example::

    >>> tokens, seps = tokenize('лосось/сьомга с/м 1-2кг')
    >>> tokens
    ... # ['лосось', '/', 'сьомга', 'с', '/', 'м', '1', '-', '2', 'кг']
    >>> seps
    ... # ['', '', ' ', '', '', ' ', '', '', '']

    """
    if not name.islower():
        name = name.lower()

    tokenized = [(m.group(), m.span()) for m in TOKEN_PATTERN.finditer(name)]

    tokens = [text for text, span in tokenized]
    seps = [name[tokenized[i][1][1]: tokenized[i+1][1][0]] for i in range(len(tokenized)-1)]

    return tokens, seps


def detokenize(tokens: Sequence[str], seps: Sequence[str]) -> str:
    """
    Retokenize tokens to string.

    ::Parameters::

    :param Sequence[str] tokens: list of tokens
    :param Sequence[str] seps: list of separators

    :return str: output string

    ::Example::

    >>> tokens = ['лосось', '/', 'сьомга', 'с', '/', 'м', '1', '-', '2кг']
    >>> seps = ['', '', ' ', '', '', ' ', '', '']
    >>> detokenize(tokens, seps)
    ... # 'лосось/сьомга с/м 1-2кг'

    """
    name = ''.join([(seps[i-1] if i else '') + tokens[i] for i in range(len(tokens))])

    return name
