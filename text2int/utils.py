import re
from .convert import text_to_int
from spacy.tokens import Doc


def convert_price(text: str) -> int:
    """
    Converts a text representation of a price into an integer.

    This function checks if the input text is a numeric string (either integer or float).
    If it is, it converts the text to an integer. If the text represents a number in words,
    it uses the `text_to_int` function to convert it.

    Args:
        text (str): The text representation of the price.

    Returns:
        int: The numeric representation of the price.

    Raises:
        ValueError: If the text cannot be converted to a number.
    """
    # Check if the text is a number in string format (either integer or float)
    if re.match(r'^\d+(\.\d+)?$', text):
        print("(convert_price) numeric number found")
        return int(float(text))
    
    # Otherwise, assume it's a text number and convert using text_to_int
    return text_to_int(text)


def get_tokens_and_index(doc:Doc)-> tuple[int,list]:
    """
    Extracts tokens and identifies the starting index of the 'PRICE' entity from a spaCy document.

    Args:
        doc (spacy.tokens.Doc): A spaCy document object containing tokens and entities.

    Returns:
        tuple: A tuple containing:
            - start_token_index (int): The index of the token where the 'PRICE' entity starts.
            - tokens (list of str): A list of tokens extracted from the document.
    """
    tokens = [token.text for token in doc]
    for ent in doc.ents:
        if ent.label_ == 'PRICE':
            start_token_index = ent.start
    return start_token_index, tokens


def get_surrounding_words(doc: Doc, num_words: int = 4)->list:
    """
    Extracts surrounding words around a specific token from a SpaCy Doc object.

    This function retrieves a specified number of words before and after the token of interest
    in the provided `Doc` object. The function assumes that the token of interest has already
    been identified and processes the context around it.

    Args:
        doc (Doc): The SpaCy Doc object containing the text and its annotations.
        num_words (int, optional): Number of words to extract before and after the token of interest. Defaults to 5.

    Returns:
        List[str]: A list of strings representing the surrounding words. The list includes words before and after the token of interest,
                excluding the token itself.
    """
    start_index, tokens = get_tokens_and_index(doc)
    start_context_index = max(0, start_index - num_words)
    end_context_index = min(len(tokens), start_index + num_words + 1)
    return tokens[start_context_index:start_index] + tokens[start_index + 1:end_context_index]


def find_synonym_category(words):
    """
    Identifies if any of the given words belong to the 'below' or 'above' synonym categories.

    Args:
        words (List[str]): A list of words to check.
        below_synonyms (List[str]): A list of synonyms indicating 'below' or 'less than'.
        above_synonyms (List[str]): A list of synonyms indicating 'above' or 'greater than'.

    Returns:
        str: A message indicating which category was found first, or a message if no synonyms were found.
    """

    below_synonyms = [
    "under", "less than", "beneath", "within", "not more than", "up to a maximum of",
    "lower than", "up to", "at most", "no more than", "cheaper than", "priced below",
    "underneath", "within the range of", "maximum", "capped at", "down to", "fewer than",
    "restricted to", "not exceeding", "within a limit of", "under the limit of", "below"
    ]

    above_synonyms = [
    "above", "more than", "greater than", "over", "exceeding", "beyond",
    "higher than", "in excess of", "upwards of", "surpassing", "greater",
    "higher", "exceeds", "above the limit of", "higher in price than",
    "more expensive than", "higher than", "beyond the range of",
    "beyond the limit of", "above and beyond", "beyond the maximum of",
    "exceeding the price of","priced above", "priced over", "over"
    ]


    for word in words:
        if word.lower() in above_synonyms:
            print("(find_synonym_category) gte word is",word)
            return f"gte"
        elif word.lower() in below_synonyms:
            print("(find_synonym_category) lte word is",word)
            return f"lte"
    print("(find_synonym_category) no above or below found, lte is defult")
    return "lte" # if none found by defult return lte



def remove_empty_lists_recursive(lst):
    """
    Recursively removes empty lists from a list, including nested lists.
    sometimes a list of prices returns [100, []] beacuse it got a price and a non price word as price by mistake

    Args:
        lst (list): The input list containing elements which may include empty lists.

    Returns:
        list: A new list with all empty lists removed, including from nested lists.
    """
    # Create a new list to hold non-empty elements
    result = []
    for item in lst:
        if isinstance(item, list):
            # Recursively process nested lists
            cleaned_item = remove_empty_lists_recursive(item)
            # Append item only if it is not an empty list after recursion
            if cleaned_item:  # Only add to result if cleaned_item is not an empty list
                result.append(cleaned_item)
        else:
            result.append(item)
    return result
