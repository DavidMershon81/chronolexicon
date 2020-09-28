import re
from collections import namedtuple

DatedWord = namedtuple("DatedWord", "first_use was_parsed")

def main():
    test_separate_words()
    #test_parse_formatted_dates()


def test_separate_words():
    #This should extract a list of tuples with a length of 2
    #each tuple will have the word in index 0 and the non-word content(spaces, punctuation) at index 1
    #if a string of digits (e.g. 25, 327) is present, this will be recognized as a word,
    #but I can filter this out later, instead of doing a dictionary lookup.

    print("running test_separate_words...")
    sample_text = "Couldn't a 25 sentence, with wan'a'wana'wn and   Rodriguez-Rodriguez weren't it? For 327 dogs... Don't knock it! Or Mor#(**Too()ps? I thought so!"
    print(f"sample_text: {sample_text}")
    print("separated tuples:")
    words = regex_find_all_matches(sample_text, r"([\w|'*]+)(\W+)")
    for word in words:
        print(f"word:[{word[0]}] punctuation:[{word[1]}]")
    

def test_named_tuple():
    test_success_word = DatedWord(first_use="1926", was_parsed=True)
    test_fail_word = DatedWord(first_use=None, was_parsed=False)
    print("test_named_tuple...")
    print(f"test_success_word first_use: {test_success_word.first_use} | was_parsed: {test_success_word.was_parsed}")
    print(f"test_fail_word first_use: {test_fail_word.first_use} | was_parsed: {test_fail_word.was_parsed}")


def test_tuple():
    tuple_test = ("dog", 3.724, ("meep", "meep2"), "cat", 257, True, "bear")
    for word in tuple_test:
        print(word)
    
    is_true = tuple_test[5]
    print(f"testing tuple indexing - is_true: {is_true}")


def test_parse_formatted_dates():
    formatted_dates = ( "before 12th century{ds||1|a|}", "14th century{ds||1||}", "1519{ds||1|a|}", "1526", "1949",
    "15th century{ds||1||}", "circa 1842", "1st century", "2nd century", "3rd century", "4th century", "dog", "23 cat" )

    print("printing formatted dates...")
    for fd in formatted_dates:
        parsed_date = parse_formatted_date(fd)
        message = f"formatted_date:{fd} parsed date:{parsed_date}"
        print(message)


def parse_formatted_date(formatted_date):
    #print(f"parsing formatted_date:{formatted_date}...")

    four_digit_date = regex_find_one_match(formatted_date, r"\d{4}")
    century_date_raw = regex_find_one_match(formatted_date, r"(\d{1,2})(th|st|rd|nd)( century)")

    if four_digit_date: 
        #print(f"found four_digit_date: {four_digit_date}")
        return DatedWord(first_use=int(four_digit_date), was_parsed=True)
    elif century_date_raw:
        is_before = regex_find_one_match(formatted_date, r"before")
        first_use_century = int(century_date_raw[0]) - 1
        if is_before:
            first_use_century -= 1
        century_first_use_date = first_use_century * 100 + 50
        return DatedWord(first_use=century_first_use_date, was_parsed=True)
        #DatedWord(first_use=None, was_parsed=False)
    else:
        return DatedWord(first_use=None, was_parsed=False)


def regex_find_one_match(text, search_pattern):
    matches = regex_find_all_matches(text, search_pattern)
    if len(matches) > 0:
        return matches[0]
    else:
        return None


def regex_find_all_matches(text, pattern):
    pattern = re.compile(pattern)
    return pattern.findall(text)


main()