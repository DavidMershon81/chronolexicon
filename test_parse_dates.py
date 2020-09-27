import re

def main():
    formatted_dates = [ "before 12th century{ds||1|a|}", "14th century{ds||1||}", "1519{ds||1|a|}", "1526", "1949",
    "15th century{ds||1||}", "circa 1842", "1st century", "2nd century", "3rd century", "4th century", "dog", "23 cat" ]

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