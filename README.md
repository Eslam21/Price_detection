Here’s a README description based on the provided code:

---

# Price Detection with SpaCy

This project demonstrates a Python-based approach for detecting and processing price-related information from text using SpaCy, a popular natural language processing library. The code extracts price entities, converts them to numerical values, and constructs queries based on the extracted prices. It handles various price formats and applies filtering based on detected synonyms indicating price ranges.

## Features

- **Price Detection**: Identifies price entities within text using a custom SpaCy model.
- **Text-to-Number Conversion**: Converts textual representations of numbers (e.g., "eighty-eight") to integers using the `text2int` library.
- **Synonym Handling**: Detects and processes synonyms for price ranges (e.g., "below", "above") to adjust query parameters.
- **Range Filtering**: Constructs queries to filter results based on extracted price ranges.

## Installation

Ensure you have Python and SpaCy installed. You will also need the `text2int` library for converting text to numbers. Install the necessary packages using:

```bash
pip install spacy text2int
python -m spacy download en_core_web_md
```

Make sure to have the SpaCy model for price detection loaded from the `price_model/` directory.

## Usage

1. **Load the Model**: Load the pre-trained SpaCy model for price detection.

   ```python
   import spacy
   from text2int import text_to_int
   from text2int.utils import (
       get_surrounding_words, 
       find_synonym_category, 
       convert_price, 
       remove_empty_lists_recursive
   )

   # Load the price detection model
   price_model = spacy.load("price_model/")
   ```

2. **Define Examples**: Provide a list of text examples containing price information.

   ```python
   examples = [
       "I'm searching for a gift within 88 $",
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
   ```

3. **Process Examples**: Iterate through the list of examples, process each with the SpaCy model, and generate queries based on detected prices.

   ```python
   for example in examples:
       print(example)
       
       # Process the example with the price_model to get a SpaCy document object
       doc = price_model(example)
       
       # Extract and convert 'PRICE' entities from the document to a list of prices
       prices = [convert_price(ent.text) for ent in doc.ents if ent.label_ == 'PRICE']
       prices = remove_empty_lists_recursive(prices)
       print("Prices are", prices)
       
       # Generate a query based on the number of extracted prices
       if len(prices) == 0 or prices[0] is None:
           query = {}
       elif len(prices) == 1:
           prev_following_words = get_surrounding_words(doc, num_words=4)
           result = find_synonym_category(prev_following_words)
           query = {
               "must": [
                   {"range": {"price": {result: prices[0]}}},
               ]
           }
       elif len(prices) == 2:
           sorted_price = sorted(prices)
           query = {
               "must": [
                   {"range": {"price": {"lte": sorted_price[1]}}},
                   {"range": {"price": {"gte": sorted_price[0]}}}
               ]
           }
       
       print(query)
       print("------------------\n")
   ```
