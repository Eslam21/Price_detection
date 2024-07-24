import spacy
from text2int import text_to_int
from text2int.utils import (
                            get_surrounding_words, 
                            find_synonym_category, 
                            convert_price, 
                            remove_empty_lists_recursive 
                            )

# load the price detection model 
price_model = spacy.load("price_model/")


examples = [
    "I'm searching for a gift within 88 $ ",
    "It is available for four hundred and seventy-five ¥.",
    "The total cost is twenty-five EGP.",
    "I need a gift for my dad, something related to gardening and costs around one hundred and fifty $.",
    "This costs between five hundred and fifty-nine EGP and seven hundred and four EGP.",
    "I want to give my mom something cool. She likes cooking and I have a budget of eight hundred and seventy-nine ¥.",
    "I am looking for a present for my brother. He is 88 years old and likes computer games. please below 50.8 euros",
    "He enjoys playing games with friends.",
    "I want a birthday gift for my father. He is 64 years old. I have 100 in my bank account.",
    "Gifts between 30 and 100 dollars.",
    "hello",
    "I want it to cost 88",
    "kjhdjkfhskjf",
    "dff874f",
    "/89",
    "Looking for something under 120 dollars.",
    "Budget is 250 USD.",
    "Price range: 10-15 GBP.",
    "The item should cost around 1000 JPY.",
    "Searching for items priced between 45 and 75 AUD.",
    "Want something for about 200 CAD.",
    "Max price I can spend is 60 EUR.",
    "Finding gifts under 300 INR.",
    "Looking for gifts that cost between twenty and fifty dollars.",
    "I'm on a tight budget, so I need something under fifty pounds.",
    "", "     "
]

# Iterate through each example in the list of examples
for example in examples:
    # Print the current example for debugging purposes
    print(example)
    
    # Process the example with the price_model to get a spaCy document object
    doc = price_model(example)
    
    # Extract and convert 'PRICE' entities from the document to a list of prices
    prices = [convert_price(ent.text) for ent in doc.ents if ent.label_ == 'PRICE']
    # sometimes a list of prices returns [100, []] beacuse it got a price and a non price word as price by mistake, so empty nested lists is removed
    prices= remove_empty_lists_recursive(prices) 
    print("Prices are", prices)

    # Generate a query based on the number of extracted prices
    if len(prices) == 0 or prices[0]==None:
        # No prices found, so set the query to an empty dictionary
        query = {}

    elif len(prices) == 1:
        # Only one price found
        # Get 4 words surrounding the detected price to check if it has keywords for lte or gte
        prev_following_words = get_surrounding_words(doc, num_words=4)
        # Find a synonym category(lte, gte) based on the surrounding words
        result = find_synonym_category(prev_following_words)

        # Create a query that filters results to match the single price
        query = {
            "must": [
                {"range": {"price": {result: prices[0]}}},
            ]
        }

    elif len(prices) == 2:
        # Two prices found
        # Sort the prices to ensure correct range ordering
        sorted_price = sorted(prices)
        # Create a query that filters results within the range of the two prices
        query = {
            "must": [
                {"range": {"price": {"lte": sorted_price[1]}}},
                {"range": {"price": {"gte": sorted_price[0]}}}
            ]
        }

    # Print the generated query for debugging purposes
    print(query)
    print("------------------\n")

