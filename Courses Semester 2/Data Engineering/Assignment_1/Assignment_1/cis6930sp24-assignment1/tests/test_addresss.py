import pytest

from assignment1.main import censor_address

testdata = [
    ("My address is 2200 Classen blvd, apt 10115, Norman, Oklahoma, 73071. My friend address is 2230 Classen blvd, apt 10115, Norman, Oklahoma, 73071", 
    "My address is █████████████████████████████████████████████████████. My friend address is █████████████████████████████████████████████████████", 
    2),
    ("I live in 193 classen blvd, apt 10115, Norman, OK, 73071","I live in ██████████████████████████████████████████████",1),
    ("the address is 1619 George Washington Lane, Norman, OK, 73071","the address is ██████████████████████████████████████████████",1)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = censor_address(input)
    assert actual_text == expected_text
    assert len(word_list) == expected_count