from typing import Iterable

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Compute the Levenshtein distance between two strings.

    The Levenshtein distance is a measure of the difference between two sequences. It is the minimum number
    of single-character edits (insertions, deletions, or substitutions) required to change one word into the other.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        int: The Levenshtein distance between the two strings. Closest to 0 the better

    Example:
        >>> levenshtein_distance("kitten", "sitting")
        3
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]



def get_closest_word(word: str, possibilities: Iterable[str], threshold: int = 1) -> str:
    """
    Returns the closest match for a given word from the list of possibilities using Levenshtein distance.

    Args:
        word (str): The word to find the closest match for.
        possibilities (Iterable[str]): A list or set of possible words to compare against.
        threshold (int): The maximum allowable Levenshtein distance for a match to be considered close. Default is 2.

    Returns:
        str: The closest matching word from the possibilities if within the threshold; otherwise, the original word.

    Example:
        >>> get_closest_word("appel", ["apple", "applet", "apply"])
        'apple'
    """

    closest_match = min(possibilities, key=lambda x: levenshtein_distance(word, x))
    if levenshtein_distance(word, closest_match) <= threshold:
        return closest_match
    else:
        return word
