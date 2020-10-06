from regex_helper import regex_find_all_matches
from collections import namedtuple

DatedWordPunctuationPair = namedtuple("WordPunctuationPair", "word punctuation first_use_info")

def separate_words_and_punctuation(text):
    #This should extract a list of tuples with a length of 2
    #each tuple will have the word in index 0 and the non-word content(spaces, punctuation) at index 1
    #if a string of digits (e.g. 25, 327) is present, this will be recognized as a word,
    #but I can filter this out later, instead of doing a dictionary lookup.
    return regex_find_all_matches(text, r"([\w|'*]+)(\W*)")

