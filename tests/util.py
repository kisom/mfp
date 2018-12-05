import pytest

from mfp import util


def test_trim_zeroes():
    for i in range(8):
        lst = [0] * i
        trimmed = util.trim(lst)
        assert len(trimmed) == 0


def test_trim_only_zeroes():
    for i in range(8):
        lst = [1] * i
        trimmed = util.trim(lst)
        assert len(trimmed) == len(lst)


def test_trim_trailing():
    lst = [1, 0, 0, 1, 0]
    trimmed = util.trim(lst)
    assert len(trimmed) == 4
    assert trimmed == lst[:4]
