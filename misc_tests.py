from regex_helper import regex_find_all_matches
from word_age_info import parse_formatted_date, DatedWord
from word_separator import separate_words_and_punctuation

def main():
    test_parse_formatted_dates()


def test_named_tuple():
    test_success_word = DatedWord(first_use="1926", was_parsed=True)
    test_fail_word = DatedWord(first_use=None, was_parsed=False)
    print("test_named_tuple...")
    print(f"test_success_word first_use: {test_success_word.first_use} | was_parsed: {test_success_word.was_parsed}")
    print(f"test_fail_word first_use: {test_fail_word.first_use} | was_parsed: {test_fail_word.was_parsed}")


def test_parse_formatted_dates():
    formatted_dates = ( "before 12th century{ds||1|a|}", "14th century{ds||1||}", "1519{ds||1|a|}", "1526", "1949",
    "15th century{ds||1||}", "circa 1842", "1st century", "2nd century", "3rd century", "4th century", "dog", "23 cat" )

    print("printing formatted dates...")
    for fd in formatted_dates:
        parsed_date = parse_formatted_date(fd, "N/A - test word")
        message = f"formatted_date:{fd} parsed date:{parsed_date}"
        print(message)


def test_separate_words_from_text(sample_text):
    print(f"sample_text: {sample_text}")
    print("separated tuples:")
    words = separate_words_and_punctuation(sample_text)

    for word in words:
        print(f"word:[{word[0]}] punctuation:[{word[1]}]")


main()