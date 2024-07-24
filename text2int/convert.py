from .distance import get_closest_word

def text_to_int(textnum:str)-> int:
    """
    Converts a textual representation of a number into its integer form.

    Args:
        textnum (str): The number in word form (e.g., 'two million twenty three thousand and forty nine').

    Returns:
        int: The integer representation of the number.

    Raises:
        ValueError: If the input is not a string.
        Exception: If an illegal word (not recognized as a number word) is found in the input.

    Example:
        >>> text_to_int('two million twenty three thousand and forty nine')
        2023049

        >>> text_to_int('thre')
        3
    """
    numwords = {
        'and': (1, 0), 'zero': (1, 0), 'one': (1, 1), 'two': (1, 2), 'three': (1, 3), 'four': (1, 4),
        'five': (1, 5), 'six': (1, 6), 'seven': (1, 7), 'eight': (1, 8), 'nine': (1, 9), 'ten': (1, 10), 'eleven': (1, 11),
        'twelve': (1, 12), 'thirteen': (1, 13), 'fourteen': (1, 14), 'fifteen': (1, 15), 'sixteen': (1, 16), 'seventeen': (1, 17),
        'eighteen': (1, 18), 'nineteen': (1, 19), 'twenty': (1, 20), 'thirty': (1, 30), 'forty': (1, 40), 'fifty': (1, 50),
        'sixty': (1, 60), 'seventy': (1, 70), 'eighty': (1, 80), 'ninety': (1, 90), 'hundred': (100, 0), 'thousand': (1000, 0),
        'million': (1000000, 0)
    }

    if len(textnum)== 0:
        print("(text_to_int) empty text")
        return []

    elif type(textnum) is not str:
        raise ValueError("(text_to_int) Input is not a string! Please enter a valid number word (e.g., 'two million twenty three thousand and forty nine')")

    splitted_textnum = textnum.replace('-', ' ').lower().strip().split()   # Convert to lowercase and replace hyphens

    # Correct typos in split words
    clean_textnum = [get_closest_word(word, list(numwords.keys())) for word in splitted_textnum]

    current = result = 0
    for word in clean_textnum:
        if word not in numwords:
            return []
        
        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
