from typing import Dict, Sequence, List, Tuple, Callable, Optional, Union
from itertools import product, chain
import re
import logging

from .tokenizer import tokenize, detokenize
from .config import MIN_START_TOKEN_LENGTH
from .phonetic_translit import latin_to_cyrillic_phonetic
from .search_index import SearchIndex


logger = logging.getLogger(__name__)


def build_search_index(
        data: List[Tuple[Union[int, str], str]],
        min_start_token_length: int = MIN_START_TOKEN_LENGTH,
        transliterate_latin: bool = False,
        callback: Optional[Callable] = None,
        should_stop: Optional[Callable] = None,
        callback_step: int = 10000
) -> SearchIndex:
    search_index = SearchIndex()
    update_search_index(
        search_index=search_index,
        data=data,
        min_start_token_length=min_start_token_length,
        transliterate_latin=transliterate_latin,
        callback=callback,
        should_stop=should_stop,
        callback_step=callback_step)
    return search_index


def update_search_index(
        search_index: SearchIndex,
        data: List[Tuple[int, str]],
        min_start_token_length: int = MIN_START_TOKEN_LENGTH,
        transliterate_latin: bool = False,
        callback: Optional[Callable] = None,
        should_stop: Optional[Callable] = None,
        callback_step: int = 10000
):

    for i, (idx, key) in enumerate(data):
        if i % callback_step == 0:
            if callback:
                callback(i / len(data))
            if should_stop and should_stop():
                break
        queries = __generate_queries(key, min_start_token_length, transliterate_latin)

        for rate, queries_data in queries.items():
            for query in queries_data:
                search_index[rate][query] = idx


def __generate_queries(
        key: str,
        min_start_token_length: int,
        transliterate_latin: bool
) -> Dict[int, Sequence[str]]:

    queries = dict()
    queries[0] = [key.lower(), ]

    tokens, seps = tokenize(key)

    if transliterate_latin:
        tokens_groups = [__get_latin_translit(token) for token in tokens]
        _queries = [detokenize(_tokens, seps) for _tokens in product(*tokens_groups)]
        queries[1] = [query for query in _queries if query != key]
    else:
        tokens_groups = [[token, ] for token in tokens]
    logger.debug(f'For key: "{key}" generated {len(tokens_groups)} tokens_groups: {tokens_groups}')

    queries[2] = []
    for i in range(1, len(tokens_groups)+1):
        alt_tokens_groups = chain(tokens_groups[i:], tokens_groups[:i])
        alt_seps = list(chain(seps[i:], [' ', ], seps[:i-1]))
        new_queries = [detokenize(_tokens, alt_seps) for _tokens in product(*alt_tokens_groups) if len(tokens[0]) >= min_start_token_length]
        queries[2].extend(new_queries)

    return queries


def __get_latin_translit(token: str) -> Sequence[str]:
    alias = [token, ]

    if re.match('[a-z ]+', token):
        alias.extend(latin_to_cyrillic_phonetic(token))

    return alias
