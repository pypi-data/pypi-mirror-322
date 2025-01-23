from typing import Tuple, Sequence

from .patterns import TOKEN_PATTERN


def tokenize(name: str) -> Tuple[Sequence[str], Sequence[str]]:
    """
    Retokenize tokens to string.

    ::Parameters::

    :param str name: input string

    :return Tuple[Sequence[str], Sequence[str]]: list of tokens and list of separators

    """
    tokenized = [(m.group(), m.span()) for m in TOKEN_PATTERN.finditer(name)]

    tokens = [text for text, span in tokenized]
    seps = [name[tokenized[i][1][1]: (tokenized[i+1][1][0] if i+1 < len(tokenized) else None)] for i in range(len(tokenized))]

    return tokens, seps


def detokenize(tokens: Sequence[str], seps: Sequence[str]) -> str:
    """
    Retokenize tokens to string.

    ::Parameters::

    :param Sequence[str] tokens: list of tokens
    :param Sequence[str] seps: list of separators

    :return str: output string

    """
    name = ''.join([(seps[i-1] if i else '') + tokens[i] for i in range(len(tokens))])
    if len(seps) == len(tokens):
        name += seps[len(tokens)-1]

    return name
