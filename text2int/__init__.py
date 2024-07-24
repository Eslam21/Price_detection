"""
This package provides utilities for text processing, including conversion of numbers represented as string such to integers
and string similarity calculations using Levenshtein distance.
"""

from .convert import text_to_int
from .distance import get_closest_word, levenshtein_distance
from .utils import get_surrounding_words, find_synonym_category, convert_price, get_tokens_and_index, remove_empty_lists_recursive

__all__ = ["text_to_int", 
        "get_closest_word", 
        "levenshtein_distance", 
        "get_surrounding_words", 
        "find_synonym_category", 
        "convert_price", 
        "get_tokens_and_index",
        "remove_empty_lists_recursive"]
