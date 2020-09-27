import re
from collections import namedtuple


def main():
    #test_parse_formatted_dates()
    #test_tuple()
    test_named_tuple()


def test_named_tuple():
    DatedWord = namedtuple("DatedWord", "first_use was_parsed")
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
        message = f"formatted_date:{fd}"

        four_digit_date = regex_find(fd, r"\d{4}")
        if four_digit_date: 
            message += f" | four_digit_date: {four_digit_date}"

        century_date = regex_find(fd, r"(\d{1,2})(th|st|rd|nd)( century)")
        if century_date: 
            is_before = regex_find(fd, r"before")
            message += f" | century_date: {century_date[0]}"
            if is_before:
                message += "(before)"

        print(message)


def regex_find(formatted_date, search_pattern):
    pattern = re.compile(search_pattern)
    matches = pattern.findall(formatted_date)
    if len(matches) > 0:
        return matches[0]
    else:
        return None

main()