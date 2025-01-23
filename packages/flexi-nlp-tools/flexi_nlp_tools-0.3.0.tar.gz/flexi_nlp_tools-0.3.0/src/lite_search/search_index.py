from typing import Dict
from dataclasses import dataclass
from pathlib import Path

import dill

from flexi_dict import FlexiDict
from flexi_dict.search_engine.correction import SymbolInsertion
from flexi_dict.search_engine import SearchEngine


@dataclass
class SearchIndex(Dict[int, 'FlexiDict']):

    def __getitem__(self, key: int) -> 'FlexiDict':
        if key not in self:
            search_engine = SearchEngine(symbol_insertion=SymbolInsertion(price=.01))
            self[key] = FlexiDict(search_engine=search_engine)
        return super().__getitem__(key)


def save_search_index(search_index: SearchIndex, dirname: str):
    dirname = Path(dirname)
    dirname.mkdir(exist_ok=True)

    for k, v in search_index.items():
        with open(dirname / f'{k}.bin', "wb") as f:
            dill.dump(file=f, obj=v.trie, recurse=True)


def load_search_index(dirname: str) -> SearchIndex:
    dirname = Path(dirname)
    if not dirname.exists():
        raise FileNotFoundError(f'Directory "{dirname}" does not exist')
    filenames = sorted(dirname.glob('*.bin'), key=lambda x: x.stem)

    search_index = SearchIndex()

    search_engine = SearchEngine(symbol_insertion=SymbolInsertion(price=.01))
    for filename in filenames:
        flexi_dict = FlexiDict(search_engine=search_engine)
        flexi_dict.load_trie(filename)
        key = int(filename.stem)
        search_index[key] = flexi_dict

    return search_index
