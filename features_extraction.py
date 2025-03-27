def extract_features(url):
    """
    Extracts lexical features from a URL and returns them as a dictionary:
    - URL length
    - Special character count
    - Digit count
    """

    url_length = len(url)

    special_chars = ['.', '-', '@', '/', '?', '=', '_']
    special_char_count = sum(url.count(char) for char in special_chars)

    digit_count = sum(c.isdigit() for c in url)

    return {
        "url_length": url_length,
        "special_char_count": special_char_count,
        "digit_count": digit_count
    }


