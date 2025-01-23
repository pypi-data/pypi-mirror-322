from typing import Optional, Dict, Tuple, List


def validate_symbols(symbols: List[str]):
    invalid_symbols = [symbol for symbol in symbols if len(symbol) != 1]
    if invalid_symbols:
        raise ValueError(
            f"Invalid keys in `symbol_weights`: {invalid_symbols}. "
            "All keys must be single-character symbols (e.g., 'a', 'b', 'c')."
        )


def validate_scores(scores: List[float]):
    invalid_scores = [score for score in scores if not (0.0 <= score <= 1.0)]
    if invalid_scores:
        raise ValueError(
            f"Invalid weights in `symbol_weights`: {invalid_scores}. "
            "All weights must be floats in the range [0, 1]."
        )


def validate_symbol_weights(symbol_weights: Optional[Dict[str, float]]) -> None:
    """
    Validates the symbol weights dictionary.

    Ensures that all keys in the `symbol_weights` dictionary are single-character strings
    and that all weights are in the range [0, 1].

    Args:
        symbol_weights (Optional[Dict[str, float]]): A dictionary where keys are symbols (strings of length 1)
            and values are weights (floats in the range [0, 1]).

    Raises:
        ValueError: If any key is not a single-character string.
        ValueError: If any weight is not a float in the range [0, 1].
    """
    if symbol_weights is None:
        return

    validate_symbols(list(symbol_weights.keys()))
    validate_scores(list(symbol_weights.values()))


def validate_symbols_distances(symbol_distances: Optional[Dict[Tuple[str, str], float]]) -> None:
    if symbol_distances is None:
        return
    x, y = zip(*symbol_distances.keys())
    validate_symbols(x)
    validate_symbols(y)
    validate_scores(list(symbol_distances.values()))

