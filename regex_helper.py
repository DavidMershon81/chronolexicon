import re

def regex_find_one_match(text, search_pattern):
    matches = regex_find_all_matches(text, search_pattern)
    if len(matches) > 0:
        return matches[0]
    else:
        return None


def regex_find_all_matches(text, pattern):
    pattern = re.compile(pattern)
    return pattern.findall(text)