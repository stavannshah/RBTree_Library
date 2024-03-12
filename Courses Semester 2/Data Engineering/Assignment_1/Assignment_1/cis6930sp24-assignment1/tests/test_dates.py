import pytest

from assignment1.main import censor_dates

testdata = [
    ("Birthday is 6/8/2021, my birthday is on November, 16th, 1997", "Birthday is ████████, my birthday is on ████████████████████", 2),
]

@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = censor_dates(input)
    assert actual_text == expected_text
    assert len(word_list) == expected_count