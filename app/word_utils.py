import os
import requests
import re
#from flask import Flask, request
from collections import namedtuple

DatedWord = namedtuple("DatedWord", "word_lower first_use was_parsed")
DatedWordPunctuationPair = namedtuple("WordPunctuationPair", "word punctuation first_use_info")


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


def separate_words_and_punctuation(text):
    #This should extract a list of tuples with a length of 2
    #each tuple will have the word in index 0 and the non-word content(spaces, punctuation) at index 1
    #if a string of digits (e.g. 25, 327) is present, this will be recognized as a word,
    #but I can filter this out later, instead of doing a dictionary lookup.
    return regex_find_all_matches(text, r"([\w|'*]+)(\W*)")


def regex_find_one_match(text, search_pattern):
    matches = regex_find_all_matches(text, search_pattern)
    if len(matches) > 0:
        return matches[0]
    else:
        return None


def regex_find_all_matches(text, pattern):
    pattern = re.compile(pattern)
    return pattern.findall(text)