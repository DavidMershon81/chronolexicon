import os
import requests
from flask import Flask, request


def find_word_age(word):
    """Find the first use of a word from the lexicon."""
    word_lower = word.lower()
    
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word_lower}?key={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        word_age = process_dictionary_response(response)
        #return response.text
        return word_age
            #"name": raw_dictionary_api_json["companyName"]
    except (KeyError, TypeError, ValueError):
        return None


def process_dictionary_response(response):
    response_json = response.json()
    number_of_entries = len(response_json)

    result = []
    result.append(f"there are {number_of_entries} entries for this word.")

    for entry in response_json:
        first_known_use = "unknown"
        
        if "date" in entry:
            first_known_use = entry["date"]

        definition = entry["shortdef"][0]
        result.append(f"first_known_use: {first_known_use} defintion: {definition}")

    return result
