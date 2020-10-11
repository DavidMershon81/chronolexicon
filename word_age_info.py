import os
import requests
from flask import Flask, request
from regex_helper import regex_find_one_match
from collections import namedtuple


DatedWord = namedtuple("DatedWord", "word_lower first_use was_parsed")


def search_api_for_word_first_use(word):
    """Find the first use of a word from the lexicon."""
    word_lower = word.lower()
    
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word_lower}?key={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return DatedWord(word_lower=word_lower, first_use=None, was_parsed=False)

    # Parse response
    try:
        return process_dictionary_response(response, word_lower)
    except (KeyError, TypeError, ValueError):
        return DatedWord(word_lower=word_lower, first_use=None, was_parsed=False)


def process_dictionary_response(response, word_lower):
    response_json = response.json()

    if len(response_json) < 1:
        return DatedWord(word_lower=word_lower, first_use=None, was_parsed=False)
    else:
        return parse_formatted_date(response_json[0]["date"], word_lower)
        
    #first_known_use = None

    #for entry in response_json:
        #homophone_first_known_use = parse_formatted_date(entry["date"], word_lower)
        
        #if not first_known_use or homophone_first_known_use.first_use < first_known_use.first_use:
            #first_known_use = homophone_first_known_use
    
    #return first_known_use


def parse_formatted_date(formatted_date, word_lower):
    #print(f"parsing formatted_date:{formatted_date}...")

    four_digit_date = regex_find_one_match(formatted_date, r"\d{4}")
    century_date_raw = regex_find_one_match(formatted_date, r"(\d{1,2})(th|st|rd|nd)( century)")

    if four_digit_date: 
        #print(f"found four_digit_date: {four_digit_date}")
        return DatedWord(word_lower=word_lower, first_use=int(four_digit_date), was_parsed=True)
    elif century_date_raw:
        is_before = regex_find_one_match(formatted_date, r"before")
        first_use_century = int(century_date_raw[0]) - 1
        if is_before:
            first_use_century -= 1
        century_first_use_date = first_use_century * 100 + 50
        return DatedWord(word_lower=word_lower, first_use=century_first_use_date, was_parsed=True)
        #DatedWord(first_use=None, was_parsed=False)
    else:
        return DatedWord(word_lower=word_lower, first_use=None, was_parsed=False)


