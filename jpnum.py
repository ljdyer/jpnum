#!/usr/bin/env python3
"""
Author : Laurence Dyer <ljdyer@gmail.com>
Date   : 15/09/2021
Purpose: Convert between arabic and Japanese kanji numbers
"""

import argparse, re, sys

kanji_1to9: str = "一二三四五六七八九"
kanji_2to9: str = "二三四五六七八九"
kanji_powers_of_ten: list = [("", True), ("十", False), ("百", False), ("千", False), ("万", True)]
kanji_all: str = kanji_1to9 + ''.join(k for (k, _) in kanji_powers_of_ten)

is_valid_kanji_number_regex = f'^(?:[{kanji_1to9}]万)?(?:[{kanji_2to9}]?千)?(?:[{kanji_2to9}]?百)?(?:[{kanji_2to9}]?十)?(?:[{kanji_1to9}]?)$'


# daiji_1to9 = "壱弐参四五六七八九"
# daiji_powers_of_10 = "拾百千万"

# --------------------------------------------------
class UserInputError(Exception):
    pass


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Convert between arabic and Japanese kanji numbers',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('pos',
                        metavar='str',
                        help='The input: an arabic number or a kanji number, up to 99,999.')

    # parser.add_argument('-d',
    #                     '--daiji',
    #                     help='Convert from western to Japanese "daiji" scripts used for banking. Will convert to standard Japanese kanji if this option is not selected.',
    #                     action='store_true')

    return parser.parse_args()


# --------------------------------------------------
def single_arabic_to_kanji(value: str, position: int) -> str:
    """Convert a (value, position) pair to a kanji string"""
    
    value = int(value)
    kanji, include_if_one = kanji_powers_of_ten[position]
    if value == 0:
        return ''
    elif value == 1 and not include_if_one:
        return kanji
    else:
        return kanji_1to9[value-1] + kanji
        

# --------------------------------------------------
def arabic_to_kanji(a: str) -> str:
    """Convert an arabic number a kanji number"""

    parts: list = [single_arabic_to_kanji(a[len(a)-i-1], i)
        for i in reversed(range(0, len(a)))]
    k: str = ''.join(parts)
    return k
    

# --------------------------------------------------
def single_kanji_to_arabic(k: str) -> int:
    """Convert a single kanji character to an integer
    Return 1 if input is an empty string"""

    # Exploits fact that string.index('') returns 0
    return kanji_1to9.index(k) + 1


# --------------------------------------------------
def kanji_to_arabic(k: str) -> str:
    """Convert a kanji number to an arabic number"""
    total = 0

    # Ones
    regex = f'([{kanji_1to9}])$'
    if match := re.search(regex, k):
        total += single_kanji_to_arabic(match.group(1))

    # Remaining powers of ten
    for i in range(1,5):
        regex = f'([{kanji_1to9}]?){kanji_powers_of_ten[i][0]}'
        if match := re.search(regex, k):
            total += single_kanji_to_arabic(match.group(1)) * pow(10, i)

    return str(total)


# --------------------------------------------------
def check_arabic(a: str) -> bool:

    if int(a) > 99999:
        raise UserInputError('Number is too large. I can only convert numbers up to 99,999.')
    else:
        return True


# --------------------------------------------------
def check_kanji(k: str) -> bool:

    if not re.search(is_valid_kanji_number_regex, k):
        raise UserInputError(f'Input is not a valid kanji number, or is too large. I can only convert well-formed kanji numbers up to 99,999 (九万九千九百九十九).')
    else: 
        return True


# --------------------------------------------------
def convert_arabic(a: str) -> str:

    if check_arabic(a):
        return arabic_to_kanji(a)


# --------------------------------------------------
def convert_kanji(k: str) -> str:

    if check_kanji(k):
        return kanji_to_arabic(k)


# --------------------------------------------------
def has_kanji(s: str) -> bool:

    if re.search(f'[{kanji_all}]', s):
        return True
    else:
        return False


# --------------------------------------------------
def convert(input) -> str:

    s = str(input)
    
    if re.search(r'^\d*$', s):  # Regex declared as raw string because Python 3 interprets string literals as Unicode strings
        return convert_arabic(s)
    elif re.search(f'^[{kanji_all}]+$', s):
        return convert_kanji(s)
    else:
        raise UserInputError(f'Input contains invalid characters. Input must either be an arabic number containing digits 0-9 (no commas), or a kanji number containing only the following characters: {kanji_all}.')

# --------------------------------------------------
def main():
    """Main program"""
    args = get_args()
    input = str(args.pos)

    sys.stdout.reconfigure(encoding='utf-8')

    output = convert(str(input))
    print(output,end='')


# --------------------------------------------------
if __name__ == '__main__':
    try:
        main()
    except UserInputError as e:
        sys.exit("UserInputError: " + str(e))