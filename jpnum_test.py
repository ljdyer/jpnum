#!/usr/bin/env python3
"""tests for jpnum.py"""

import os
import re
from jpnum import *
from subprocess import getstatusoutput, run

prg = 'jpnum.py'

# check 10,000
test_pairs = [('5', "五"), ('11', '十一'), ('104', '百四'), ('3073', '三千七十三'), ('16578', '一万六千五百七十八')]
invalid_inputs = ['二十s三','ten', '10000000', '九九万九千九百九十九']


# --------------------------------------------------
def get_stderr_stdout(input):

    result = run(['python', prg, input], encoding="utf-8", universal_newlines=False, capture_output=True)
    err = result.stderr
    out = result.stdout
    return err, out


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{prg} {flag}')
        assert rv == 0
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_arabic_to_kanji():
    """arabic to kanji test pairs"""

    for (input, output) in test_pairs:
        err, out = get_stderr_stdout(input)
        assert err == ''
        assert out == output


# --------------------------------------------------
def test_kanji_to_arabic():
    """"kanji to arabic test pairs"""

    for (output, input) in test_pairs:      
        err, out = get_stderr_stdout(input)
        assert err == ''
        assert out == output


# --------------------------------------------------
def test_one_to_one_mapping():
    """test that no two arabic numbers yield the same kanji number"""

    kanji = [arabic_to_kanji(str(i)) for i in range(1,100000)]
    assert len(kanji) == len(set(kanji))


# --------------------------------------------------
def test_involution():
    """test that the convert function is an involution (is its own inverse)"""

    for i in range(1,100000):
        assert convert(convert(i)) == str(i)


# --------------------------------------------------
def test_value_error():
    """test for value errors for invalid input values"""

    for input in invalid_inputs:
        err, _ = get_stderr_stdout(input)
        assert re.search("ValueError", err, re.IGNORECASE)